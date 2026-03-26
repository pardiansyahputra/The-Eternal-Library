# Simulasi Tunneling & Analisis Vektor Social Engineering
----
###### Tanggal: 25/03/2026
###### Kategori: Web Security / Social Engineering
###### sourcode/folder:

---

**1. Pendahuluan**

Riset ini bertujuan untuk menganalisis bagaimana penyerang memanfaatkan infrastruktur tunneling gratis serta teknik manipulasi psikologis untuk melakukan pencurian data identitas (PII) dan metadata perangkat secara real-time. Attcker bisa menyesuaikan script code dengan target yang di tuju (kesehatan, perbankan, pendidikan, dan lain-lain)


**2. Persiapan Infrastruktur (Lab Setup)**

Tahap awal dilakukan dengan menyiapkan jalur tunneling agar server lokal dapat diakses dari internet publik tanpa perlu konfigurasi port forwarding pada router. Disini saya menggunakan Cloudflared untuk tunneling [pada saat praktik ini dijalankan, ini masih gratis dan kita bisa melakukan analisis sesuai kemauan kita]

***Instalasi Cloudflared***

* Unduh binary resmi Cloudflared untuk Windows [link download](https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe  )
* Jalankan executable sesuai arsitektur sistem

***Direktori Kerja***
Untuk Direktori kerja  bisa di sesuiakan, berdasarkan dimana tempat kita akan melakukan testing codenya. disini saya membuat folder kusus sebab saya mau menggunakan bahasa python
```bash
C:\...\...\tempat latihan\bahasa_python\
```


**3. Pengembangan Alat Analisis (PoC Script)**

File `test.py` dibuat menggunakan Flask untuk menangkap data korban.
Script ini mensimulasikan halaman verifikasi biometrik palsu.

```python
# [Snippet Logika Utama Flask]

@app.route('/cek-data')
def index():
    # Menampilkan UI verifikasi palsu
    return render_template_string('''...''')

@app.route('/log-final', methods=['POST'])
def log_final():
    # Menangkap data:
    # - Nama
    # - Email
    # - GPS
    # - Informasi RAM & CPU
    # - Foto (Base64)
    
    # Menyimpan hasil ke file:
    # hasil_investigasi.txt
```

untuk hal ini bisa disesuaikan sesuai dengan tester, untuk code lengkap saya ada di bagian link di header

**4. Eksekusi Tunneling**

Tunnel dijalankan menggunakan Cloudflare untuk menghasilkan URL publik HTTPS yang valid tanpa peringatan SSL.

+ Command

```powershell
.\cloudflared-windows-amd64.exe tunnel --url http://localhost:5000
```

+ Output
kira kira kamu akan menemukan output seperti ini:

```text
https://random-name.trycloudflare.com/cek-data
```

***NB:penting untuk di perhatikan, jika kita menjalankan langsung dengan vscode, kita harus membuka 2 terminal didalam path sistem yang sama, 1 terminail untuk menjalankan code python dari script yagn sudah kita buat tadi (ini sebagai tempat masuknya informasi korban) dan 1 terminal lagi sebagai tempat dijalankannya tunneling agar link bisa di akses dari website secara umum***


**5. Analisis Vektor Manipulasi (Obfuscation)**

Pengujian dilakukan terhadap berbagai teknik penyembunyian link untuk mengevaluasi efektivitas serangan social engineering.

| Level | Teknik            | Contoh                   | Efektivitas   |
| ----- | ----------------- | ------------------------ | ------------- |
| 1     | URL Shortener     | Bitly, S.id              | Tinggi        |
| 2     | Redirect Umpan    | Linktree, Google Sites   | Sangat Tinggi |
| 3     | Hyperlink Masking | Anchor Text (Email/WA)   | Tinggi        |
| 4     | @ Symbol Trick    | google.com@phishing-link | Menengah      |
| 5     | QR Code           | Poster / Media Digital   | Tinggi        |
| 6     | Icon Mockup       | Logo DANA / Banking      | Ekstrim       |

---

**6. Temuan Riset (Key Findings)**

***Hasil Utama***

* Kecepatan Ekstraksi
  Data sensitif seperti lokasi dan foto dapat berpindah ke sistem penyerang dalam waktu kurang dari **2 detik** setelah izin diberikan.

* Hardware Fingerprinting
  Informasi RAM dan CPU memungkinkan penyerang melakukan profiling perangkat untuk serangan lanjutan yang lebih spesifik.

* Psychological Trap


**7. Kesimpulan & Mitigasi**

Simulasi ini menunjukkan bahwa teknologi tunneling yang legal dapat disalahgunakan secara efektif dalam skenario social engineering.

***Rekomendasi***
+ Selalu verifikasi domain utama, bukan hanya subdomain
+ Gunakan 2FA/MFA berbasis hardware (FIDO2)
+ Hindari memberikan izin kamera atau lokasi pada situs yang tidak terpercaya
+ Tingkatkan awareness terhadap teknik phishing modern


# Disclaimer

##### Dokumen ini dibuat hanya untuk tujuan edukasi dan analisis keamanan siber dalam lingkungan terkontrol.Segala bentuk penyalahgunaan di luar konteks tersebut merupakan pelanggaran hukum.