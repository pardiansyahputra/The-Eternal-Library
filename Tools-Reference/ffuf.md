# Penjelasan penggunaan alat FFUF dalam melakukan testing 

###### Tanggal Riset: 28/03/2026 11:09
###### Kategori: tools Enumerasi 
---
**Penjelasan**
FFuF adalah alat fuzzing web cepat yang dibuat dalam bahasa Go.
Adapun Fuzzing adalah proses otomatis mengirimkan data acak ke suatu aplikasi untuk menemukan kesalahan konfigurasi, perilaku yang tidak terduga, atau parameter tersembunyi. FFuF adalah fuzzer pilihan bagi banyak peneliti saat ini.FFuF (Fuzz Faster u Fool)

**instalasi**
+ instalasi go
Jika teman-teman ingin menginstalnya dari situs web, kunjungi https://golang.org, namun teman teman yang menggunakan linux bisa melakukan command ini :
```bash
sudo apt install golang
```

+ instalasi FFuF
Kunjungi di https://github.com/ffuf/ffuf . Untuk menginstal, kita akan menggunakan Go untuk mendapatkan versi terbaru.
```bash
go get -u github.com/ffuf/ffuf
```

+ instalasi daftar kata
kami merekomendasikan “SecLists” ( https://github.com/danielmiessler/SecLists ). Ini adalah kumpulan wordlist umum untuk berbagai keperluan.
```bash
Sudo git clone https://github.com/danielmiessler/SecLists
```

**perintah penggunaan**
+ Sintaks Dasar
```Bash
ffuf -u http://target.com/FUZZ -w /usr/share/wordlists/dirb/common.txt
```
***penjelasan***
>`-u (URL)`: Target utama.
`-w (Wordlist)`: Daftar kata yang akan disuntikkan ke posisi FUZZ [INI DI SESUAIKAN].
---
+ Teknik Filtering
```bash
ffuf -u http://target.com/FUZZ -w /usr/share/wordlists/dirb/common.txt -fc 404 -fs 0
```
Artinya: Tampilkan semua hasil KECUALI yang statusnya 404 dan yang ukurannya 0 byte.
***penejelasan***
> `-fc (Filter Code):` Menyaring berdasarkan HTTP Status Code (misal: -fc 200,301,302,401,404,403,500).
`-fs (Filter Size):` Menyaring berdasarkan ukuran respon (sangat berguna jika halaman "Not Found" kustom memiliki ukuran yang sama, misal: -fs 1492).
`-fl (Filter Line):` Menyaring berdasarkan jumlah baris dalam respon.
`-fw (Filter Word):` Menyaring berdasarkan jumlah kata dalam respon.

ada kebalikan dari command `f` diatas, sebagaimana berikut ini :
> `-mc (Match Code):` Hanya tampilkan jika status code tertentu (misal: -mc 200,301).
`-ms (Match Size):` Hanya tampilkan jika ukurannya tepat sekian.
`-mr (Match Regex):` Ini yang paling kuat. Hanya tampilkan jika di dalam isi halaman tersebut terdapat kata tertentu (misal: "admin", "dashboard", atau "root").

dengan contoh seperti ini:
```bash
ffuf -u http://target.com/FUZZ -w /usr/share/wordlists/dirb/common.txt -mr "index of"
```

---
+ Parameter Fuzzing
```bash
ffuf -u http://target.com/admin.php?FUZZ=1 -w /usr/share/wordlists/dirb/common.txt -fs 1200
```
+ Header Fuzzing
```bash
# Digunakan untuk menguji Header seperti X-Forwarded-For atau mencari Virtual Hosts.
ffuf -u http://target.com/ -H "Host: FUZZ.target.com" -w subdomains.txt -fs 250
```

+ Multiple Wordlists

```bash
ffuf -u http://target.com/login -X POST -d "user=W1&pass=W2" -w users.txt:W1 -w pass.txt:W2 -fc 200
```

```bash
ffuf -u http://target.com/api/W1/user/W2 -w wordlist1.txt:W1 -w wordlist2.txt:W2
```

***penjelasan***
>`W1` akan mengambil data dari `users.txt.`
`W2` akan mengambil data dari `pass.txt.`
---
+ Optimalisasi Performa & Output
```bash
ffuf -u http://localhost/FUZZ -w /usr/share/wordlists/dirb/common.txt -recursion -recursion-depth 2 -v
```

***penjelasan***
> `-t 100:` Mengatur jumlah threads (default 40). Semakin tinggi, semakin cepat, namun beban server target semakin berat.
`-p 0.1:` Memberikan jeda (delay) antar request (misal 0.1 detik) untuk menghindari deteksi WAF atau IP blocking.
`-recursion:` Melakukan pencarian mendalam. Jika ditemukan direktori, ffuf akan otomatis melakukan fuzzing di dalam direktori tersebut.
`-of html`:Menyimpan hasil dalam format HTML
`-o report.json -of json:` Menyimpan hasil dalam format JSON untuk kemudian diolah menjadi laporan atau diintegrasikan dengan alat lain.
`-v`:Ini akan menampilkan URL lengkap beserta redirect (Location header), yang sangat krusial untuk membedakan antara direktori asli dan endpoint palsu.

---
+ mencari extensi
```Bash
ffuf -u http://target.com/FUZZ -w /usr/share/wordlists/dirb/common.txt -e .php,.txt,.bak,.zip
```
>`-e (Extensions):` Menambahkan ekstensi pada setiap kata di wordlist.

+ pencegahan error

```bash
ffuf -u http://target.com/FUZZ -w /usr/share/wordlists/dirb/common.txt -sf
```

> `-sf (Stop on Flag):` Menghentikan proses jika persentase error terlalu tinggi (misal: kena blokir WAF).
`-se (Stop on Error):` Langsung berhenti jika ada kesalahan koneksi (biar tidak buang-buang waktu jika server down).
`-sa (Stop on All):` Gabungan keduanya.
---
**Tambahan**
reverensi:https://www.intigriti.com/researchers/blog/hacking-tools/hacker-tools-ffuf-fuzz-faster-u-fool-2
