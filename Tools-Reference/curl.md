# Penjelasan penggunaan alat CURL dalam melakukan testing 

###### Tanggal Riset: 12/04/2026 07:51 [belum tuntas]
###### Kategori: tools serbaguna 
---
**Penjelasan**
curl (Client URL) adalah alat baris perintah untuk mentransfer data menggunakan berbagai protokol (HTTP, HTTPS, FTP, SMB, dll).  curl memungkinkan kamu melihat apa yang disembunyikan oleh browser (seperti Chrome atau Firefox).Dengan curl, kamu memegang kendali penuh atas setiap header dan byte yang dikirim.

#### COMMAND DASAR
berikut ini beberapa command dasar yang bisa kamu pelajari sebagai fundamental dari curl, untuk membangun pemahaman dan keterampilan yang lebih terlatih kedepannya, setelah command dasar ini di pahami terdapat command expert yang bisa kamu coba

**Request Dasar (GET)**
```bash
curl https://example.com
```
+ Melihat source code mentah tanpa render dari browser. Kamu bisa melihat komentar-komentar tersembunyi yang mungkin ditinggalkan oleh desainer web.

**Melihat Header Saja**
```bash
curl -I https://example.com
```
+ Mengetahui jenis server (Nginx/Apache), versi PHP, atau apakah website tersebut menggunakan proteksi seperti Cloudflare.

**Menyimpan Hasil ke File**
```bash
curl -o hasil_web.html https://example.com/contoh_file.js
```
+ berguna saat kamu ingin mengunduh script `.js` atau file `.php` (yang ter-expose) untuk dipelajari kodenya secara offline.

**Mengikuti Redirect**
```bash
curl -L https://google.com
```
+ Memastikan kamu sampai ke halaman tujuan akhir [dalam konteks redirect situs], bukan cuma tertahan di halaman pengalihan.

**Mode Verbose**
```bash
curl -v https://example.com
```
+ melihat semua hasil dengan detail, Membantu debugging kenapa sebuah koneksi gagal atau melihat cookie yang dikirimkan server secara detail.

**Mengunduh File dengan Nama Asli**
```bash
curl -O https://example.com/files/tools.zip
```
**Menyamar sebagai Browser (User-Agent)**
```bash
curl -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0" https://example.com
```
+ Menembus proteksi dasar yang melarang akses non-browser atau melihat konten khusus mobile.

**Menggunakan Proxy**
```bash
curl -x http://127.0.0.1:8080 https://example.com
```
+ Memungkinkan kamu melihat request curl kamu di dalam software analisis trafik seperti Burp Suite atau OWASP ZAP.

** IP-Spoofing via HTTP Header**
```bash
curl https://target.com/api/admin \
-H "X-Forwarded-For: 127.0.0.1" \
-H "X-Real-IP: 127.0.0.1"
```
+ untuk penjelasan & payload [Klik](/Web-Security/Header%20Manipulations/IP-Spoofing%20via%20HTTP%20Headers.md)