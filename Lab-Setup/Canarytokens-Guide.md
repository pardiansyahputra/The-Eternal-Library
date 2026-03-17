# Intrusion Detection with Canarytokens
---
###### Tanggal Riset: 15/03/2026 23:15
###### Kategori: Honeypot / Defensive Security


**1. Deskripsi Singkat**
Canarytokens adalah alat keamanan yang berfungsi sebagai "alarm" digital menggunakan konsep Honeypot. Alat ini menyisipkan beacon (tanda) ke dalam objek (file/folder/domain). Ketika objek tersebut diakses tanpa izin, sistem akan secara otomatis mengirimkan peringatan ke email pemilik lengkap dengan metadata pelaku.

**2. Mekanisme Teknis**
Web Beacon (HTTP): Menggunakan HTTP GET Request melalui URL unik yang tersembunyi (misalnya pada objek gambar 1x1 piksel dalam file .docx). Memberikan data lengkap seperti IP Address dan User-Agent.

>ALUR KERJA SISTEM
file/folder/domain =>> masuk ke canarytokens =>> masukkan email kita (sebagai pemilik) ==> ketika file/folder/domain dibuka ==> informasi sipembuka ==> dikirim ke email kita(pemilik).

DNS Beacon: Menggunakan DNS Lookup ke subdomain unik. Lebih sulit dideteksi dan diblokir karena hampir semua jaringan mengizinkan trafik DNS (Port 53).

**3. Parameter Informasi yang Diperoleh**
Dalam pengujian pribadi pada file MS Word, data yang berhasil diekstraksi dari sisi "pembuka" adalah:

- Source IP: IP publik pembuka file.
- Timestamp: Tanggal dan waktu akses (UTC).
- User Agent: Detail aplikasi/browser dan OS yang digunakan (misal: MSOffice 16).
- Token ID: Identifier unik untuk melacak file mana yang dibuka.

**4. Keterbatasan** 
Sistem peringatan tidak akan terpicu jika:

- Perangkat pembuka dalam kondisi Offline.
- File dibuka dalam lingkungan Isolated Lab (Air-gapped) tanpa akses jaringan keluar.

**5. Referensi Cepat**
URL Pembuatan: https://canarytokens.org
Dokumentasi Resmi: https://docs.canarytokens.org


***NOTE***
1. Web Beacon (Pelacak Jalur HTTP)
Berikut beberapa penjelasan singkat:
+ Cara Kerja: Di dalam file, disisipkan sebuah link gambar (biasanya berukuran 1x1 piksel) yang transparan dengan URL unik.
+ Contoh: <img src="http://canarytokens.org/b7p9eqfy9i7.../pixel.png">
+ Proses: Begitu file dibuka, aplikasi (Word/Browser) akan melakukan HTTP GET Request ke URL tersebut untuk mengambil gambar.
+ Data yang Didapat: Sangat lengkap (IP Address, User-Agent/Tipe Browser, Versi OS).
+ Kelemahan: Mudah diblokir oleh Firewall atau Proxy tingkat lanjut karena terlihat seperti trafik web biasa.



2. DNS Beacon (Pelacak Jalur Sistem Nama)
Berikut beberapa penjelasan singkat:
+ Cara Kerja: Ia tidak meminta gambar, melainkan mencoba melakukan DNS Lookup (pencarian alamat IP) terhadap sebuah domain unik.
+ Contoh: Aplikasi mencoba menghubungi b7p9eqfy9i7scb0kvpss2is9v.canarytokens.com.
+ Proses: Laptop si pembuka akan bertanya ke server DNS terdekat: "di mana IP untuk alamat ini?". Pertanyaan ini akan terus diteruskan hingga sampai ke server milik Canary.
+ Data yang Didapat: Terbatas (Hanya IP Address dari server DNS yang bertanya, bukan selalu IP asli si pelaku).
+ Kelebihan: Sangat sulit diblokir. Banyak jaringan yang memblokir akses web (HTTP), tapi hampir semua jaringan wajib mengizinkan trafik DNS agar internet bisa jalan.
+ Guna: Biasanya digunakan di dalam folder atau file-file sistem yang sangat dalam.
