# Penjelasan Penggunaan Alat OOXML Analisis

###### Tanggal Riset: 30/05/2026 07:51 
###### Kategori: Analisi file Docx, PPTx, Xlsx (Edukasi) 
---
**Penjelasan**
Ini merupakan Tool lanjutan dari catatan saya terkait [Bongkar-Pasang-Docx-Xlsx-Pptx](/Forensics/Bongkar-Pasang-Docx-Xlsx-Pptx.md), dikarnakan hal ini menurut saya cocok untuk dibahas kepada khlayak umum. jadi saya membuat tool sederhana berbasis GUI untuk analisis materi ini, dengan kata lain tools ini tidak direkomendasikan untuk alat tempur analisis malware dan forensik medium ketas. 

**karakteristik**
meskipun saya belum puas dengan hasil yang ada sekarang (ketika saya menulis ini), namun tool ini sudah dapat dipakai oleh siapapun yang membutuhkannya. Berikut karakteristik dari alat ini :

+ Dibangun dengan bahasa pemograman `python`
+ Tampilan berbasis GUI
+ Cocok untuk semua kalangan (pelajar, pengajar dan analisis dasar forensik dan malware)
+ Memiliki diagram hubung dan tampilan yang informatif
+ Dapat digunakan untuk melakukan pengubahan meta data
+ Dapat digunakan untuk melakukan analisis link internal tampa merender file (seperti analisis Canarytokens) [baca selengkapnya](/Lab-Setup/Canarytokens-Guide.md)
+ Dan lain lain

**depedensi & instalasi**
Untuk menjalankan alat ini dibutuhkan beberapa depensi terlebih dahulu, berikut command yang bisa dijalakan :

```bash
pip install matplotlib networkx lxml reportlab
```
setelah menjalankan itu kemudian clone code alat ini/simpan di komputer [Klik disini](Tool-OOXML.py)

**Tampilan alat**
Berikut adalah bebera tangkapan layar dari alat ini:
1. tampilan tab 1
![alt text](/Writeups/gambar/image_8.png)
2. tampilan tab 2 
![alt text](/Writeups/gambar/image_9.png)
3. tampilan tab 3
![alt text](/Writeups/gambar/image_10.png)

**Baca juga**
+ [Panduan Penggunaan Canarytokens](../Lab-Setup/Canarytokens-Guide.md)
+ [Bongkar-Pasang-Docx-Xlsx-Pptx Dalam Konteks Meta-Data file](/Forensics/Bongkar-Pasang-Docx-Xlsx-Pptx.md)
+ [Tabel panduan OOXML](/Forensics/Tabel-Panduan-Arsitektur-OOXML.md)







