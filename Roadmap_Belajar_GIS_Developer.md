# Roadmap Belajar GIS Developer (Python)

Panduan bertahap membangun skill *sekaligus* mengisi halaman "GIS Developer" di
portofolio. Prinsipnya: **satu tahap = satu proyek kecil = satu repo GitHub**.
Tidak perlu sekaligus. Kualitas kode dan kejelasan README lebih dinilai daripada
kerumitan.

---

## Prasyarat singkat (jika perlu, ~1 minggu)
- Python dasar: variabel, list/dict, fungsi, loop, baca/tulis file.
- Git & GitHub dasar: `clone`, `add`, `commit`, `push`, membuat repo, menulis README.
- Sumber gratis: dokumentasi resmi Python, GeoPandas, dan "Automating GIS Processes"
  (materi kuliah Universitas Helsinki, terbuka untuk umum).

---

## TAHAP 01 — Dasar GeoPandas (2–3 minggu)
**Tujuan:** melakukan ulang satu analisis yang biasa kamu klik di ArcGIS, tapi lewat kode.

Yang dipelajari:
- `geopandas.read_file()` / `to_file()` untuk SHP & GeoJSON
- Filter baris, memilih kolom, `merge`/join atribut
- Menghitung kolom baru, `dissolve`, `buffer`, `sjoin` (spatial join)
- Plot cepat dengan `.plot()`

Latihan konkret:
- Ambil satu SHP kecamatan → filter satu kabupaten → hitung luas → simpan GeoJSON.
- Ulangi "buffer + overlay" yang pernah kamu buat di tugas kuliah, kali ini dengan kode.

Output: notebook `.ipynb` + README singkat. **Belum wajib jadi proyek portofolio.**

---

## TAHAP 02 — Proyek #1: Automasi Indeks Risiko (2–3 minggu)
**Tujuan:** proyek portofolio pertama — domain yang sudah kamu kuasai dari UNFPA.

Bangun skrip `risk_index.py` yang:
1. Membaca layer bahaya (H), kerentanan (V), kapasitas (C).
2. Menormalkan tiap indikator (min–maks 0–1).
3. Menghitung `R = (H * V) / C` per unit wilayah.
4. Mengklasifikasikan (rendah/sedang/tinggi) dan menyimpan GeoJSON + peta PNG.

Struktur repo yang rapi:
```
risk-index-automation/
├── README.md          # masalah → cara pakai → hasil (dengan 1 gambar peta)
├── requirements.txt   # geopandas, matplotlib, dll
├── risk_index.py
├── data/              # contoh data kecil (atau tautan)
└── output/            # peta hasil
```

Setelah selesai: unggah ke GitHub, lalu di halaman "GIS Developer" ubah kartu proyek
ini dari "Sedang dikerjakan" → "Selesai" dan aktifkan tautan GitHub-nya.

---

## TAHAP 03 — Proyek #2: Peta Web Interaktif (2 minggu)
**Tujuan:** menampilkan hasil Tahap 02 sebagai peta yang bisa di-zoom & diklik.

Yang dipelajari:
- `folium.Map`, `GeoJson`, `Choropleth`
- Styling warna berdasarkan kelas risiko, popup atribut
- Menyimpan sebagai `index.html` yang bisa dibuka siapa saja / di GitHub Pages

Output: peta web + README. Ini biasanya jadi "wow factor" untuk recruiter karena
langsung bisa dicoba di browser.

---

## TAHAP 04 — Proyek #3: Raster & Batch Processing (3–4 minggu)
**Tujuan:** menangani data raster dan banyak file sekaligus.

Yang dipelajari:
- `rasterio` untuk baca/tulis raster (mis. data iklim, DEM), `rasterstats` (zonal stats)
- Membuat skrip batch: loop banyak file, konversi format, gabungkan, ekspor
- Menjadikannya skrip CLI sederhana (argumen input/output)

Output: skrip batch + README dengan contoh perintah menjalankannya.

---

## Tahap lanjutan (opsional, saat sudah nyaman)
- **PostGIS** — menyimpan & meng-query data spasial di basis data.
- **API geospasial** — FastAPI/Flask untuk menyajikan hasil analisis.
- **Otomasi/scraping** — manfaatkan pengalaman Playwright-mu untuk mengambil data web
  menjadi dataset siap analisis.
- **Google Earth Engine (Python API)** — analisis citra satelit berskala besar.

---

## Cara mengukur kemajuan
Setiap proyek dianggap "layak portofolio" jika:
- [ ] Ada repo GitHub publik dengan README yang jelas
- [ ] Kode terbagi ke fungsi, ada komentar, ada `requirements.txt`
- [ ] Ada satu gambar hasil (peta/plot) di README
- [ ] Orang lain bisa menjalankannya hanya dengan membaca README

Begitu satu proyek memenuhi ini, masukkan ke halaman "GIS Developer" dan lanjut ke
tahap berikutnya. Portofolio tumbuh pelan tapi jujur.
