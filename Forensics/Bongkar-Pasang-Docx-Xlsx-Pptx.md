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

***NOTE***
berikut ada beberapa main maps yang bisa di jadikan acuan dalam melakukan deep analisis kedepannya, mungkin beberapa memiliki sedikit perbedaan:

> Ekstensi ==> .docx   &Folder Konten  ==> word/    &File Utama  ==> document.xml
Ekstensi ==> .xlsx   &Folder Konten  ==> xl/, workseets   &File Utama ==> sharedStrings.xml
Ekstensi ==> .pptx   &Folder Konten  ==> ppt/, slide   &File Utama ==> slide1.xml

***BACA JUGA***
**Setup Lab & Defensif:** [Panduan Penggunaan Canarytokens](../Lab-Setup/Canarytokens-Guide.md)
