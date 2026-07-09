"""
Pemetaan sebaran populasi berbasis Random Forest (pendekatan berstrata).

Memodelkan populasi dari variabel spasial (kedekatan jalan, fasilitas, elevasi/DEM,
dan tutupan lahan/LULC). Area terbangun (LULC = 7) dan area lainnya dimodelkan
secara terpisah karena pola kepadatannya berbeda, lalu dievaluasi pada data uji
yang tidak dipakai saat pelatihan.

Dikembangkan saat magang di UNFPA Indonesia sebagai eksplorasi disagregasi populasi
(dasymetric mapping). Lihat CATATAN & KETERBATASAN di README.

Input : RF_Point.csv  (kolom: Jalan, Facility, DEM, LULC, Population)
Output: RF_Point_with_predictions_weighted.csv

Penggunaan:
    python rf_analysis_weighted.py
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# ---------------------------------------------------------------------------
# Konfigurasi
# ---------------------------------------------------------------------------
INPUT_CSV = "RF_Point.csv"
OUTPUT_CSV = "RF_Point_with_predictions_weighted.csv"

FEATURES = ["Jalan", "Facility", "DEM", "LULC"]
NUMERIC_FEATURES = ["Jalan", "Facility", "DEM"]
TARGET = "Population"

BUILT_LULC_CLASS = 7        # kode LULC untuk area terbangun
TEST_SIZE = 0.30            # porsi data untuk pengujian
RANDOM_STATE = 42

# Faktor penyesuaian empiris untuk area terbangun. Ini adalah heuristik dari
# tahap eksplorasi (bukan hasil kalibrasi statistik); set ke 1.0 untuk menonaktifkan.
# Lihat bagian keterbatasan pada README.
BUILT_AREA_FACTOR = 1.2

# Hyperparameter tiap model
PARAMS_BUILT = dict(n_estimators=300, max_depth=20, min_samples_split=3,
                    random_state=RANDOM_STATE)
PARAMS_OTHER = dict(n_estimators=200, max_depth=15, min_samples_split=5,
                    random_state=RANDOM_STATE)


# ---------------------------------------------------------------------------
# Fungsi
# ---------------------------------------------------------------------------
def load_data(path):
    """Membaca CSV dan memvalidasi kolom yang dibutuhkan."""
    df = pd.read_csv(path)
    required = set(FEATURES + [TARGET])
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Kolom berikut tidak ditemukan di {path}: {sorted(missing)}")
    return df


def build_features(df):
    """One-hot encode LULC (satu kali, pada seluruh data agar kolom konsisten
    antar-model), sisakan fitur numerik apa adanya untuk diskalakan kemudian."""
    X = df[FEATURES].copy()
    X = pd.get_dummies(X, columns=["LULC"], prefix="LandUse")
    return X


def train_stratified_models(X_train, y_train, built_train):
    """Melatih dua model Random Forest terpisah: satu untuk area terbangun,
    satu untuk area lainnya."""
    rf_built = RandomForestRegressor(**PARAMS_BUILT)
    rf_built.fit(X_train[built_train], y_train[built_train])

    rf_other = RandomForestRegressor(**PARAMS_OTHER)
    rf_other.fit(X_train[~built_train], y_train[~built_train])
    return rf_built, rf_other


def predict(rf_built, rf_other, X, built_mask):
    """Memprediksi memakai model sesuai jenis area, lalu menerapkan faktor
    penyesuaian empiris pada area terbangun."""
    preds = np.zeros(len(X))
    if built_mask.any():
        preds[built_mask] = rf_built.predict(X[built_mask]) * BUILT_AREA_FACTOR
    if (~built_mask).any():
        preds[~built_mask] = rf_other.predict(X[~built_mask])
    return preds


def report_metrics(y_true, y_pred, lulc, title):
    """Mencetak R2 dan MAE keseluruhan serta rincian per kelas LULC."""
    print(f"\n=== {title} ===")
    print(f"R-squared : {r2_score(y_true, y_pred):.4f}")
    print(f"MAE       : {mean_absolute_error(y_true, y_pred):.2f}")

    print("\nRincian per kelas LULC:")
    for cls in sorted(lulc.unique()):
        m = lulc == cls
        if m.sum() < 2:
            continue  # r2_score butuh minimal 2 sampel
        print(
            f"  LULC {cls:>2} | n={m.sum():>4} | "
            f"R2={r2_score(y_true[m], y_pred[m]):.3f} | "
            f"MAE={mean_absolute_error(y_true[m], y_pred[m]):.2f}"
        )


# ---------------------------------------------------------------------------
# Alur utama
# ---------------------------------------------------------------------------
def main():
    data = load_data(INPUT_CSV)
    X = build_features(data)
    y = data[TARGET]
    built = data["LULC"] == BUILT_LULC_CLASS

    # Split train/test — distratifikasi berdasarkan area terbangun/bukan
    # supaya kedua strata terwakili di data latih maupun uji.
    X_train, X_test, y_train, y_test, built_train, built_test = train_test_split(
        X, y, built,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=built,
    )

    # Skala fitur numerik. Scaler DI-FIT hanya pada data latih, lalu diterapkan
    # ke data uji — mencegah kebocoran informasi (data leakage).
    scaler = StandardScaler()
    X_train = X_train.copy()
    X_test = X_test.copy()
    X_train[NUMERIC_FEATURES] = scaler.fit_transform(X_train[NUMERIC_FEATURES])
    X_test[NUMERIC_FEATURES] = scaler.transform(X_test[NUMERIC_FEATURES])

    # Latih dua model pada data latih
    rf_built, rf_other = train_stratified_models(X_train, y_train, built_train)

    # Evaluasi jujur pada data uji yang tidak pernah dilihat model
    y_test_pred = predict(rf_built, rf_other, X_test, built_test.to_numpy())
    report_metrics(
        y_test.to_numpy(),
        y_test_pred,
        data.loc[y_test.index, "LULC"],
        title="Evaluasi pada DATA UJI (held-out)",
    )

    # Prediksi untuk seluruh titik (untuk diekspor & dipetakan)
    X_all = X.copy()
    X_all[NUMERIC_FEATURES] = scaler.transform(X_all[NUMERIC_FEATURES])
    data["Predicted_Pop"] = predict(rf_built, rf_other, X_all, built.to_numpy())
    data["Population_Difference"] = data[TARGET] - data["Predicted_Pop"]

    data.to_csv(OUTPUT_CSV, index=False)
    print(f"\nSelesai. Hasil disimpan ke {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
