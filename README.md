# Portofolio Analisis Spasial — Hafidha Aulia Setyanida

Situs portofolio satu tautan berisi karya analisis spasial, GIS, dan pengolahan
citra drone. Dibangun sebagai halaman statis (HTML + CSS), tanpa proses build,
siap ditayangkan di GitHub Pages.

## Halaman

- `index.html` — beranda + indeks karya
- `projects/unfpa-garut.html` — Risiko Kematian Ibu & Perubahan Iklim (UNFPA)
- `projects/klhs-teluk-pandan.html` — KLHS RDTR Teluk Pandan (Rekaspasial)
- `projects/drone.html` — Pemetaan Drone & Fotogrametri (RTK/PPK/GCP)
- `projects/deka-insight.html` — Validasi Data Survei (freelance, via cuplikan)
- `projects/coursework-thesis.html` — Skripsi & Tugas Kuliah (akademik)

## Cara menayangkan di GitHub Pages

1. Buat repository baru di GitHub (mis. `portofolio-hafidha`).
2. Unggah seluruh isi folder ini (`index.html`, `style.css`, folder `projects/` dan `assets/`).
3. Buka **Settings → Pages**.
4. Pada **Source**, pilih branch `main` dan folder `/root`, lalu **Save**.
5. Situs tersedia di `https://<username>.github.io/<nama-repo>/`.

## Menambah gambar pada halaman yang masih kosong

Dua halaman punya slot placeholder yang menunggu gambar Anda:

**Deka Insight (freelance):**
- Simpan cuplikan layar ke `assets/deka/`
- Ganti tiap blok `<div class="slot">…</div>` dengan `<img src="../assets/deka/nama.jpg">`
- Pastikan tidak ada nama/alamat/nomor responden yang terlihat (data internal klien)

**Skripsi & Tugas Kuliah (akademik):**
- Simpan gambar ke `assets/akademik/`
- Ganti tiap blok `.slot` dengan `<img src="../assets/akademik/nama.jpg">`

## Atribusi & hak cipta

- **UNFPA Garut** — output magang di UNFPA Indonesia, bersama Kharunnisa Pertiwi.
  Tabel numerik ditampilkan sebagian karena bersifat internal.
- **KLHS Teluk Pandan** — bagian dari proyek Rekaspasial Indonesia. Hak cipta dokumen
  tetap pada Rekaspasial & klien; tabel/matriks ditampilkan sebagian (pra-validasi).
- **Drone** — laporan pemrosesan fotogrametri (Agisoft Metashape).

Struktur:

```
.
├── index.html
├── style.css
├── README.md
├── projects/
│   ├── unfpa-garut.html
│   ├── klhs-teluk-pandan.html
│   ├── drone.html
│   ├── deka-insight.html
│   └── coursework-thesis.html
└── assets/
    ├── klhs/     (7 gambar)
    ├── unfpa/    (8 gambar)
    ├── drone/    (4 gambar)
    ├── deka/     (kosong — untuk cuplikan Anda)
    └── akademik/ (kosong — untuk gambar Anda)
```


## Folder untuk gambar (penting)

Setiap halaman punya folder gambarnya sendiri di dalam `assets/`:

| Halaman | Taruh gambar di | Tautkan dengan |
|---|---|---|
| UNFPA Garut | `assets/unfpa/` | `../assets/unfpa/nama.jpg` |
| KLHS Teluk Pandan | `assets/klhs/` | `../assets/klhs/nama.jpg` |
| Drone | `assets/drone/` | `../assets/drone/nama.jpg` |
| Deka Insight (freelance) | `assets/deka/` | `../assets/deka/nama.jpg` |
| Skripsi & Studio | `assets/akademik/` | `../assets/akademik/nama.jpg` |

**Halaman Skripsi & Studio masih memakai placeholder.** Gambar yang sudah
diekstrak dari file skripsi & studio Anda tersimpan di
`assets/akademik/sumber-gambar/`:

- Peta UNA skripsi: `una_reach.jpg`, `una_betweenness.jpg`, `una_straightness.jpg`,
  `una_closeness.jpg`, `una_nodes.jpg`, `una_volume.jpg`, `tod_context.jpg`
- Gambar rusun studio: `rusun_1.jpg`, `rusun_2.jpg`, `rusun_3.jpg`, `rusun_4.jpg`

Cara memasang: pindahkan gambar yang dipilih dari `sumber-gambar/` ke
`assets/akademik/`, lalu di `projects/coursework-thesis.html` ganti tiap blok
`<div class="slot">…</div>` menjadi `<img src="../assets/akademik/nama.jpg">`
dan tulis judul yang benar.


## Catatan versi ini (placeholder)

Semua gambar di setiap halaman kini berupa **placeholder** — Anda yang menentukan
gambar mana yang dipasang. Gambar mentah yang sudah diekstrak dari dokumen sumber
tersimpan di `assets/<halaman>/sumber-gambar/` (untuk unfpa, klhs, drone, dan akademik).
Pindahkan yang dipilih ke folder induknya lalu ganti blok `.slot` menjadi `<img>`.

Narasi tiap halaman sudah disesuaikan dengan peran sebenarnya:
- UNFPA Garut — dikerjakan penuh (data, analisis, peta, laporan).
- KLHS Teluk Pandan — pemeriksaan data, pengisian matriks KRP, dan narasi (peta oleh tim).
- Drone — diproses sendiri (RTK/PPK/GCP).
- Deka Insight — pemeriksaan isian kuesioner survei (bukan validasi peta).
