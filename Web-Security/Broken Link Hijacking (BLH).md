# Broken Link Hijacking (BLH)
###### severity: information `biasanya` ,low `biasannya` , medium, High
---
## 1. Apa itu Broken Link Hijacking?
Broken Link Hijacking (BLH) adalah serangan yang terjadi ketika penyerang mengambil alih link eksternal (media sosial, file JS, atau endpoint API) yang sudah tidak aktif atau "mati" (404) namun masih tercantum di website target.

## 2. Jenis-Jenis Serangan
**A. Social Media Hijacking (Low Impact - P4/P5)**
Terjadi ketika website masih menautkan (link) ke akun media sosial yang sudah dihapus atau diganti username-nya.

+ Cara Kerja: Penyerang mendaftarkan kembali username tersebut.
+ Dampak: Impersonation (penyamaran), penyebaran phishing ke pengunjung website resmi, dan merusak reputasi brand.

**B. External Script Hijacking (High Impact - P2/P3)**
Terjadi ketika website memanggil file JavaScript dari domain pihak ketiga yang sudah kedaluwarsa (expired).

+ Cara Kerja: Penyerang membeli domain yang expired tersebut dan meng-host file JS jahat dengan nama yang sama.
+ Dampak: Stored XSS (Cross-Site Scripting) secara masal. Penyerang bisa mencuri cookie, melakukan keylogging, atau mengarahkan user ke situs berbahaya.

## 3. Alur Kerja Penemuan (Reconnaissance)
Untuk menemukan celah ini, saya menggunakan workflow berikut:

Crawl/Spidering:
Gunakan Katana atau Gau untuk mengambil semua link dari target.

```Bash
katana -u https://target.com -d 5 | grep http > all_links.txt
```
+ Filter Link Eksternal: Cari link yang tidak menuju ke domain utama.

+ Cek Status Code: Gunakan `httpx` untuk mencari link yang mengembalikan status `404 Not Found` atau `NXDOMAIN`.

```Bash
cat all_links.txt | httpx -status-code -mc 404,410
```
***ALTERNATIF***
bisa juga menggunakan alat otomatisasi: https://www.brokenlinkcheck.com/ 

## 4. Verifikasi Ketersediaan:

+ Jika itu Twitter/Instagram: Cek apakah handle tersebut bisa didaftarkan.
+ Jika itu Domain: Cek di Whois apakah domain tersedia untuk dibeli.

---
## referensi
+ https://www.invicti.com/learn/broken-link-hijacking-blh 
+ https://shahjerry33.medium.com/broken-link-hijacking-mr-user-agent-cd124297f6e6 
+ https://www.linuxsec.org/2021/01/broken-link-hijacking.html 
+ https://hackerone.com/reports/1466889 
+ https://www.youtube.com/watch?v=2rjEDMMYNmk 