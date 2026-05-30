# Tabel Panduan Arsitektur OOXML Versi Lengkap

---

###### Tanggal Riset: 30/05/2026 23:15

## STRUKTUR ROOT (PONDASI)

| Lokasi Berkas         | Tipe   | Deskripsi Fungsi Teknis & Isi Komponen                                                                                                                                       | Kompatibilitas |
| --------------------- | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------- |
| `[Content_Types].xml` | Berkas | Manifes utama yang mendaftarkan seluruh Content-Type (MIME) dari setiap berkas di dalam ZIP. Jika berkas ini dihapus atau tidak valid, Office akan menganggap dokumen rusak. | Semua          |
| `_rels/.rels`         | Berkas | Relasi tingkat root yang menentukan letak bagian utama dokumen seperti `word/document.xml`, `xl/workbook.xml`, atau `ppt/presentation.xml`.                                  | Semua          |
| `docProps/core.xml`   | Berkas | Menyimpan metadata standar (Dublin Core): creator, tanggal dibuat, tanggal modifikasi, judul, dan subjek.                                                                    | Semua          |
| `docProps/app.xml`    | Berkas | Menyimpan properti aplikasi seperti nama aplikasi pembuat, versi, jumlah halaman, kata, karakter, atau slide.                                                                | Semua          |
| `docProps/custom.xml` | Berkas | Menyimpan properti kustom yang dibuat manual oleh pengguna.                                                                                                                  | Semua          |

---

## KOMPONEN ADVANCED GLOBAL

| Lokasi Berkas                             | Tipe   | Deskripsi Fungsi Teknis & Isi Komponen                                                                        | Kompatibilitas |
| ----------------------------------------- | ------ | ------------------------------------------------------------------------------------------------------------- | -------------- |
| `[Trash]/` atau `[Content_Types_Old].xml` | Folder | Direktori sementara yang kadang dibuat editor pihak ketiga atau proses konversi untuk menyimpan instans lama. | Semua          |
| `_images/` atau `customXml/`              | Folder | Menyimpan skema data XML kustom untuk integrasi data korporat atau otomatisasi formulir.                      | Semua          |

---

## EKSTENSIONER & KEAMANAN (VBA & SIGNATURE)

| Lokasi Berkas         | Tipe   | Deskripsi Fungsi Teknis & Isi Komponen                                               | Kompatibilitas      |
| --------------------- | ------ | ------------------------------------------------------------------------------------ | ------------------- |
| `word/vbaProject.bin` | Berkas | Penyimpanan kode VBA/Macro untuk Word.                                               | Semua (Versi Macro) |
| `xl/vbaProject.bin`   | Berkas | Penyimpanan kode VBA/Macro untuk Excel.                                              | Semua (Versi Macro) |
| `ppt/vbaProject.bin`  | Berkas | Penyimpanan kode VBA/Macro untuk PowerPoint.                                         | Semua (Versi Macro) |
| `_xmlsignatures/`     | Folder | Menyimpan digital signature untuk verifikasi integritas dan identitas penandatangan. | Semua               |
| `word/vbaData.xml`    | Berkas | Menyimpan konfigurasi dan event helper untuk proyek VBA.                             | Semua (Versi Macro) |

---

## DIREKTORI KHUSUS MICROSOFT WORD (`word/`)

| Lokasi Berkas                              | Tipe   | Deskripsi Fungsi Teknis & Isi Komponen                                            | Kompatibilitas |
| ------------------------------------------ | ------ | --------------------------------------------------------------------------------- | -------------- |
| `word/document.xml`                        | Berkas | Penampung utama teks, paragraf, tabel, dan objek visual Word.                     | `.docx`        |
| `word/styles.xml`                          | Berkas | Menyimpan aturan style teks dan paragraf.                                         | `.docx`        |
| `word/theme/theme1.xml`                    | Berkas | Menyimpan palet warna, font, dan efek grafis dokumen.                             | `.docx`        |
| `word/fontTable.xml`                       | Berkas | Daftar font yang digunakan beserta fallback font.                                 | `.docx`        |
| `word/webSettings.xml`                     | Berkas | Preferensi tampilan web layout.                                                   | `.docx`        |
| `word/settings.xml`                        | Berkas | Konfigurasi global dokumen seperti proteksi, track changes, zoom, dan mail merge. | `.docx`        |
| `word/header1.xml` / `word/footer1.xml`    | Berkas | Menyimpan konten header dan footer halaman.                                       | `.docx`        |
| `word/footnotes.xml` / `word/endnotes.xml` | Berkas | Menyimpan footnotes dan endnotes.                                                 | `.docx`        |
| `word/comments.xml`                        | Berkas | Menyimpan komentar, ID pembuat, waktu, dan balasan komentar.                      | `.docx`        |
| `word/numbering.xml`                       | Berkas | Mengatur sistem numbering dan multilevel list.                                    | `.docx`        |
| `word/glossary/`                           | Folder | Menyimpan AutoText atau Quick Parts.                                              | `.docx`        |

---

## DIREKTORI KHUSUS MICROSOFT EXCEL (`xl/`)

| Lokasi Berkas          | Tipe   | Deskripsi Fungsi Teknis & Isi Komponen                                                      | Kompatibilitas |
| ---------------------- | ------ | ------------------------------------------------------------------------------------------- | -------------- |
| `xl/workbook.xml`      | Berkas | Manifes internal workbook dan konfigurasi dasar Excel.                                      | `.xlsx`        |
| `xl/styles.xml`        | Berkas | Mengatur visualisasi sel, border, warna, format angka, tanggal, dan conditional formatting. | `.xlsx`        |
| `xl/sharedStrings.xml` | Berkas | Penyimpanan teks unik untuk optimasi ukuran file.                                           | `.xlsx`        |
| `xl/worksheets/`       | Folder | Berisi data tiap sheet (`sheet1.xml`, dll).                                                 | `.xlsx`        |
| `xl/chartsheets/`      | Folder | Sheet khusus yang hanya menampilkan chart penuh.                                            | `.xlsx`        |
| `xl/charts/`           | Folder | Definisi XML grafik dan chart.                                                              | `.xlsx`        |
| `xl/tables/`           | Folder | Properti tabel formal Excel.                                                                | `.xlsx`        |
| `xl/pivotTables/`      | Folder | Metadata dan struktur Pivot Table.                                                          | `.xlsx`        |
| `xl/calcChain.xml`     | Berkas | Daftar urutan kalkulasi formula Excel.                                                      | `.xlsx`        |
| `xl/printerSettings/`  | Folder | Konfigurasi printer dan layout cetak.                                                       | `.xlsx`        |

---

## DIREKTORI KHUSUS MICROSOFT POWERPOINT (`ppt/`)

| Lokasi Berkas                            | Tipe   | Deskripsi Fungsi Teknis & Isi Komponen               | Kompatibilitas |
| ---------------------------------------- | ------ | ---------------------------------------------------- | -------------- |
| `ppt/presentation.xml`                   | Berkas | Struktur utama presentasi dan urutan slide.          | `.pptx`        |
| `ppt/slides/`                            | Folder | Konten masing-masing slide.                          | `.pptx`        |
| `ppt/slideLayouts/`                      | Folder | Template layout slide.                               | `.pptx`        |
| `ppt/slideMasters/`                      | Folder | Master template desain global slide.                 | `.pptx`        |
| `ppt/notesSlides/` / `ppt/notesMasters/` | Folder | Menyimpan speaker notes dan konfigurasi cetak notes. | `.pptx`        |
| `ppt/handoutMasters/`                    | Folder | Layout handout untuk pencetakan presentasi.          | `.pptx`        |
| `ppt/viewProps.xml`                      | Berkas | Preferensi tampilan editor terakhir.                 | `.pptx`        |
| `ppt/tableStyles.xml`                    | Berkas | Template gaya tabel PowerPoint.                      | `.pptx`        |

---

## ASET EKSTERNAL DAN MEDIA

| Lokasi Berkas   | Tipe   | Deskripsi Fungsi Teknis & Isi Komponen                   | Kompatibilitas |
| --------------- | ------ | -------------------------------------------------------- | -------------- |
| `*/media/`      | Folder | Penyimpanan media asli seperti gambar, video, dan audio. | Semua          |
| `*/embeddings/` | Folder | Menyimpan objek dokumen lain yang disematkan.            | Semua          |
| `*/_rels/`      | Folder | Menyimpan relasi internal antar komponen XML.            | Semua          |
