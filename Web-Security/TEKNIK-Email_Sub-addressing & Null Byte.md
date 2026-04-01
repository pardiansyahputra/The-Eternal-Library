### Catatan Teknis: Eksploitasi Identitas Melalui Sub-addressing & Null Byte
###### Target: Form register, Form login, Form survey [semua Form yang ada kaitan dengan email]
###### Date: April 01 , 2026
##### write-up catatan:[write-up](/Web-Security/TEKNIK-Email_Sub-addressing%20&%20Null%20Byte.md)
---
#### 1. Konsep Dasar & Mekanisme
Celah ini terjadi karena adanya inkonsistensi pengolahan data (Data Inconsistency) antara tiga lapisan sistem:
+ `Gmail Sub-addressing (Fitur)`: Gmail mengabaikan karakter setelah tanda +. Secara teknis: user+apapun@gmail.com == user@gmail.com.
+ `Database Validation (Celah)`: Aplikasi menganggap user+1@gmail.com adalah string yang unik. Ini memungkinkan pendaftaran akun ganda dengan satu kotak masuk.
+ `Null Byte Injection (%00) (Eksploitasi)`: Karakter %00 adalah pembatas akhir string (string terminator) dalam banyak bahasa pemrograman (seperti C/C++). Ketika sistem mengirim email, ia berhenti membaca alamat saat bertemu %00, sehingga email "nyasar" ke alamat yang lebih pendek.

#### 2. Skenario Penggunaan (Attack Vector)
klasifikasikan skenario ini menjadi dua:

**A. Multi-Account Abuse (Sybil Attack)**
+ Cara: Daftar akun ke-1, ke-2, dst. dengan menambahkan +1, +2, atau +random.
+ Tujuan: Melewati batasan "Satu akun per email" untuk manipulasi voting, klaim promo berulang, atau spamming.

B. Account Takeover (ATO) / Shadow Account

+ Cara:Penyerang mendaftarkan akun dengan email: korban+shadow%00@gmail.com.
+ Aplikasi menyimpan akun ini sebagai entitas baru.
+ Penyerang memicu "Reset Password".
+ Karena ada %00, sistem mengirim link reset ke korban@gmail.com (milik korban/penyerang).

Tujuan: Menguasai identitas yang sah namun tersembunyi di bawah kendali email yang sama.

#### 3. Teknik Pengujian (Testing Methodology)
Jika kamu ingin melakukan testing ini lagi di masa depan, gunakan daftar periksa (checklist) berikut:
| Jenis Test            | Payload / Input        | Yang Harus Dicek                                              |
|----------------------|-----------------------|----------------------------------------------------------------|
| Email Sub-addressing | user+test@gmail.com   | Apakah sistem mengizinkan pendaftaran baru?                   |
| Dot Manipulation     | u.s.e.r@gmail.com     | Apakah dianggap akun berbeda oleh aplikasi?                   |
| Null Byte Injection  | user%00@gmail.com     | Apakah notifikasi terkirim ke user@gmail.com?                 |
| Case Sensitivity     | UsEr@gmail.com        | Apakah aplikasi membedakan huruf besar/kecil sebagai akun unik? |

#### 4. Kapan Teknik Ini Cocok Digunakan? 
Metode ini sangat efektif digunakan pada target dengan karakteristik berikut:
+ Sistem dengan Limitasi Per-User: Aplikasi yang memberikan reward atau akses terbatas hanya untuk satu akun (misal: SaaS gratisan, E-commerce promo).
+ Sistem Institusi/Pemerintah: Yang biasanya memiliki integrasi sistem lama (Legacy) di mana Input Sanitization-nya masih lemah.
+ Aplikasi dengan Fitur "Reminder": Di mana sistem akan mengirimkan daftar semua username yang terhubung ke satu email 
+ Integrasi Third-Party: Saat aplikasi menggunakan layanan pihak ketiga untuk pengiriman email (seperti Oracle Service Cloud atau SendGrid) yang mungkin memproses string secara berbeda dari database internal.

#### 5. Rekomendasi Testing

##### 1. Teknik Manipulasi Karakter (Gmail/Outlook)

| Teknik                  | Payload / Input                      | Yang Harus Dicek |
|------------------------|-------------------------------------|------------------|
| Dot Randomization      | s.i.s.t.e.m.i.n.f.o@gmail.com       | Apakah dianggap sama dengan sisteminfo@gmail.com? |
| Double Plus            | user++test@gmail.com                | Apakah filter hanya menghapus satu '+'? |
| Hyphen Sub-addressing  | user-test@outlook.com               | Apakah '-' diperlakukan seperti '+'? |
| Case Swapping          | SistemInfo@gmail.com                | Apakah database case-sensitive? |

---

##### 2. Teknik Injeksi Karakter Kontrol

| Teknik              | Payload / Input            | Yang Harus Dicek |
|--------------------|---------------------------|------------------|
| Newline Injection  | user%0Atest@gmail.com     | Apakah memutus parsing SMTP / log? |
| Space Injection    | user @gmail.com           | Apakah spasi di-trim oleh sistem? |
| Tab Character      | user%09@gmail.com         | Apakah lolos dari regex validasi email? |
| Comment In-Address | user(comment)@gmail.com   | Apakah dianggap email unik oleh database? |

---

##### 3. Teknik Bypass Domain & TLD

| Teknik                  | Payload / Input            | Yang Harus Dicek |
|------------------------|----------------------------|------------------|
| Internal IP Translation| user@127.0.0.1             | Apakah sistem menerima domain tanpa TLD? |
| Duplicate Domain       | user@gmail.com@gmail.com   | Apakah parser salah membaca email? |
| Trailing Dot           | user@gmail.com.            | Apakah dianggap valid tapi unik oleh DB? |
| Homograph Attack       | user@gmаil.com             | Apakah sistem bisa mendeteksi karakter mirip (Unicode)? |

---

##### 4. Teknik Injeksi Payload (Advanced)

| Teknik              | Payload / Input                          | Yang Harus Dicek |
|--------------------|------------------------------------------|------------------|
| XSS in Email       | "><script>alert(1)</script>@gmail.com    | Apakah terjadi XSS di dashboard/admin panel? |
| SQLi in Email      | ' OR 1=1--@gmail.com                     | Apakah query SQL rentan injection? |
| Command Injection  | ;calc.exe;@gmail.com                     | Apakah email diproses oleh sistem command? |
| Template Injection | {{7*7}}@gmail.com                        | Apakah template engine dieksekusi? |

---

##### 5. Teknik Logika & Business Flow

| Teknik                  | Payload / Input                  | Yang Harus Dicek |
|------------------------|----------------------------------|------------------|
| Email Length Overflow  | (email > 255 karakter)           | Apakah merusak struktur database? |
| Disposable Email Alias | user@mohmal.com                  | Apakah domain disposable diblokir? |
| Unicode Normalization  | user@GMAIL.com                   | Apakah normalisasi konsisten di sistem (LDAP/SSO)? |
| Null Prefix            | %00user@gmail.com                | Apakah null byte mempengaruhi parsing email? |