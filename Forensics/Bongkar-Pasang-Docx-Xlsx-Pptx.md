# Bongkar-Pasang-Docx-Xlsx-Pptx Dalam Konteks Meta-Data file
---
###### Tanggal Riset: 15/03/2026 23:15
###### Kategori: Digital Forensics / Anti-Forensics

**1. Konsep Dasar: File Dokumen Adalah ZIP**
Banyak pengguna awam menganggap .docx, .xlsx, pptx adalah file biner tunggal. Faktanya, format OOXML (Office Open XML) adalah kumpulan file XML yang dikompresi menjadi satu paket ZIP.

***Langkah Bedah Awal:***
``` bash
# Mengidentifikasi jenis file
file target_file.docx

# Melakukan ekstraksi struktur
unzip target_file.docx -d hasil_bedah/
```
**2. Anatomi Struktur Folder**
Setelah diekstrak, terdapat beberapa folder krusial bagi seorang analis:(didalam .docx. untuk extensi seperti .xlsx dan pptx hanya ada sedikit perubahan)

+ [Content_Types].xml: Daftar semua tipe konten di dalam paket. Ini adalah file pertama yang dibaca oleh aplikasi Word.
+ _rels/: Folder yang berisi informasi hubungan (relationships). Di sinilah letak instruksi jika dokumen harus memanggil file eksternal (Web Beacon).
+ docProps/: Berisi metadata (Core & App). Tempat menyimpan nama penulis (Creator), waktu pengeditan, dan versi aplikasi.
+ word/: Jantung dari dokumen.
+ document.xml: Berisi teks utama.
+ styles.xml: Definisi format dan gaya.
+ footer[n].xml: Sering digunakan untuk menyembunyikan Canary Token (Web Beacon).

# Tabel Panduan Arsitektur OOXML Versi Lengkap

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


**3. Teknik Manipulasi Metadata (Anti-Forensics)**
Untuk mengubah identitas file tanpa meninggalkan jejak dari aplikasi Office, kita dapat menggunakan manipulasi direct-stream menggunakan sed.

> Contoh Kasus: Merubah Nama Pencipta (Creator)

```Bash
# Masuk ke folder metadata
cd docProps/

# Mengubah tag creator secara presisi
sed -i 's/<dc:creator>.*<\/dc:creator>/<dc:creator>Pardiansyah Putra<\/dc:creator>/' core.xml
```

***Kenapa menggunakan sed?***

+ Presisi: Menghindari penambahan karakter hidden atau newline yang sering dilakukan editor grafis (seperti Nano/Vim) yang bisa merusak struktur XML.
- Stealth: Tidak memicu pembaruan otomatis pada Revision Number atau Last Printed Date jika tidak diinginkan.

**4. Deteksi "Canary"/sejenisnya (Analisis Forensik)**
Untuk mendeteksi apakah sebuah dokumen memiliki jebakan, analis harus mencari referensi eksternal di dalam file ***.rels***:

+ Periksa file word/_rels/document.xml.rels atau word/_rels/footer[n].xml.rels.
+ Cari atribut TargetMode="External".
+ Jika URL yang dituju mengarah ke domain asing (seperti canarytokens.com), maka dokumen tersebut terkonfirmasi sebagai Honeypot.

**5. Repackaging (Membungkus Kembali)**
Setelah modifikasi selesai, dokumen harus dibungkus kembali dengan struktur yang tepat agar bisa dibaca oleh Microsoft Word:

```Bash
# Jalankan di dalam folder hasil bedah
zip -r ../Final_Document.docx * .rels
```

**6.Bembuktian dengan perubahan**
Jika tadi sudah kita ubah Autohor/penulisnya , kita bisa lihat hasilnya dengan melakukan command ini :

``` bash
exiftool namafile.docx
```
jika berhasil nama penulis akan terganti tampa merubah waktu edit terakhir. Dan begitu seterusnya kamu bisa memanipulasi dengan cara yang sama.

---
Tanggal Riset: 29/05/2026 20:24

Jika dalam praktiknya mengalami kesulitan dalam melakukan perubahan sistem secara terminal/menggunakan windows, kita juga bisa menggunakan teknik manual, yakni dengan cara mengubah file menjadi  `.zip`, kemudian masuk kedalam `.zip` dan pilih bagian yang ingin di ubah datanya. seperti contoh kita ingin mengubah dibagian `setting.xml`. kita ubah dulu menjadi `setting.txt` selanjutnya ubah data yang ingin di ubah. kemudian ubah lagi menjadi `setting.xml` agar data kembali ke extensi semula dan terakhir ubah zip menjadi file awal tadi ( docx/pptx/xlsx).

jika ingin lebih simple lagi, kita bisa memanfaatkan bahasa pemograman `python` yang dirancang untuk membaca dan memahami proses yang ada. kenapa python ? - karna bahasa ini mudah untuk di mengerti dan modifikasi dan pastinya ramah bagi pemula

***NOTE***
berikut ada beberapa main maps yang bisa di jadikan acuan dalam melakukan deep analisis kedepannya, mungkin beberapa memiliki sedikit perbedaan:

> Ekstensi ==> .docx   &Folder Konten  ==> word/    &File Utama  ==> document.xml
Ekstensi ==> .xlsx   &Folder Konten  ==> xl/, workseets   &File Utama ==> sharedStrings.xml
Ekstensi ==> .pptx   &Folder Konten  ==> ppt/, slide   &File Utama ==> slide1.xml

***BACA JUGA***
+ **Setup Lab & Defensif:** [Panduan Penggunaan Canarytokens](../Lab-Setup/Canarytokens-Guide.md)
+ **penjelasan sistem:** [https://www.loc.gov/preservation/digital/formats/fdd/fdd000397.shtml]
+ **membaca dan menulis kostume fie:** [https://www.textcontrol.com/blog/2024/07/23/read-and-write-custom-xml-parts-in-ms-word-office-open-xml-docx-files-using-net-csharp/]
+ 


