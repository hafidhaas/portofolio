# Pemetaan Sebaran Populasi dengan Random Forest

Eksplorasi disagregasi (pemetaan *dasymetric*) sebaran populasi menggunakan
**Random Forest**, dari variabel spasial. Dikembangkan saat magang di
**UNFPA Indonesia**.

Idenya: populasi tidak tersebar merata. Area terbangun cenderung lebih padat
daripada area lain, sehingga area terbangun dan area lainnya **dimodelkan secara
terpisah**, lalu digabung menjadi satu estimasi.

## Masalah yang diselesaikan

Estimasi populasi berbasis batas administrasi sering terlalu kasar. Skrip ini
memperkirakan populasi pada titik-titik sampel dari empat variabel prediktor,
sehingga sebaran estimasi lebih menyerupai pola permukiman nyata.

## Data

Berkas input `RF_Point.csv` dengan kolom:

| Kolom        | Keterangan                                   |
|--------------|----------------------------------------------|
| `Jalan`      | Kedekatan/jarak terhadap jaringan jalan      |
| `Facility`   | Kedekatan/jarak terhadap fasilitas           |
| `DEM`        | Elevasi (Digital Elevation Model)            |
| `LULC`       | Kelas tutupan lahan (kode; `7` = area terbangun) |
| `Population` | Populasi acuan (target)                      |

## Metode

1. **Fitur** — `LULC` di-*one-hot encode*; fitur numerik (`Jalan`, `Facility`,
   `DEM`) distandarkan. Scaler di-*fit* hanya pada data latih untuk mencegah
   kebocoran informasi.
2. **Split train/test** — 70/30, distratifikasi berdasarkan area terbangun/bukan
   agar kedua strata terwakili.
3. **Dua model Random Forest** — satu untuk area terbangun (LULC = 7), satu untuk
   area lainnya, dengan hyperparameter berbeda.
4. **Penggabungan** — prediksi tiap titik memakai model yang sesuai.
5. **Evaluasi** — R² dan MAE dihitung pada **data uji** (held-out), lengkap dengan
   rincian per kelas LULC.

Alur: `Titik Sampel → Encode & Skala → Random Forest (2 model) → Prediksi & Evaluasi`

## Cara menjalankan

```bash
pip install -r requirements.txt
python rf_analysis_weighted.py
```

Letakkan `RF_Point.csv` di folder yang sama. Hasil disimpan ke
`RF_Point_with_predictions_weighted.csv` (menambahkan kolom `Predicted_Pop` dan
`Population_Difference`).

## Parameter yang dapat diubah

Semua di bagian **Konfigurasi** pada `rf_analysis_weighted.py`, antara lain
`TEST_SIZE`, hyperparameter tiap model, dan `BUILT_AREA_FACTOR`.

## Catatan & keterbatasan

Skrip ini adalah **hasil eksplorasi**, bukan model final yang tervalidasi penuh.
Beberapa hal yang perlu diperhatikan bila ingin dikembangkan lebih lanjut:

- **`BUILT_AREA_FACTOR` (default 1.2)** adalah penyesuaian **empiris/heuristik**
  untuk menaikkan estimasi kepadatan area terbangun — bukan hasil kalibrasi
  statistik. Set ke `1.0` untuk menonaktifkannya. Idealnya faktor ini divalidasi
  terhadap data referensi atau ditinggalkan bila model sudah cukup baik.
- Validasi silang (*cross-validation*) belum diterapkan; evaluasi memakai satu
  pembagian train/test.
- Ambang area terbangun disederhanakan menjadi satu kelas (`LULC = 7`).

## Struktur berkas

```
.
├── rf_analysis_weighted.py   # skrip utama
├── requirements.txt
└── README.md
```
