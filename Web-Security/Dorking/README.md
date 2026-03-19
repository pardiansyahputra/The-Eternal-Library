# Personal Reconnaissance & Dorking Index

> **Project:** Cybersecurity Research & Information Gathering  
> **Purpose:** Dokumentasi metodologi dorking untuk audit infrastruktur terkait.

---

## Deskripsi Utama

Dokumentasi ini berfungsi sebagai pusat referensi (Master Index) untuk teknik _Advanced Search_ dan _Dorking_ menggunakan berbagai platform intelijen terbuka (OSINT). Tujuannya adalah untuk memetakan aset digital, menemukan kebocoran data, dan mengidentifikasi kerentanan sebelum dieksploitasi oleh pihak yang tidak bertanggung jawab.

---

## Platform & Sumber Daya (Toolkits)

Berikut adalah daftar platform utama yang digunakan dalam proses pengumpulan informasi:

| Platform           | Fokus Utama                          | Link Referensi                                                  |
| :----------------- | :----------------------------------- | :-------------------------------------------------------------- |
| **Google Hacking** | Dokumentasi & Direktori Terbuka      | [Google Search](https://google.com)                             |
| **Shodan**         | Infrastruktur IoT & Server           | [Shodan.io](https://www.shodan.io/)                             |
| **GitHub**         | Kebocoran Source Code & Secrets      | [GitHub Search](https://github.com/search)                      |
| **GrayHatWarfare** | Open Cloud Storage (S3 Buckets)      | [Top Keywords](https://buckets.grayhatwarfare.com/top_keywords) |
| **Wiggle.net**     | Wardriving & Wireless Mapping        | [Wigle](https://wigle.net/)                                     |
| **Censys**         | Host & SSL Certificate Intel         | [Censys Search](https://platform.censys.io/home)                |
| **Crt.sh**         | Subdomain & Certificate Transparency | [Crt.sh ](https://crt.sh/)                                      |

---

## Metodologi Kerja (Workflow)

1.  **Passive Recon:** Memulai dengan `Crt.sh` dan `Google` untuk memetakan domain dan subdomain target.
2.  **Infrastructure Discovery:** Menggunakan `Shodan` dan `Censys` untuk melihat layanan (ports) yang terbuka di IP target.
3.  **Credential & Secret Hunting:** Melakukan dorking di `GitHub` untuk mencari API Keys atau password yang "hardcoded".
4.  **Cloud Leak Analysis:** Memeriksa `GrayHatWarfare` untuk file backup atau dokumen sensitif yang bocor di cloud.
5.  **Physical/Wireless Recon:** Menggunakan `Wigle` untuk memetakan titik akses Wi-Fi di sekitar lokasi target fisik.(Gunakan VPN jika tidak bisa dibuka)

---

## Aturan Penggunaan (Rules of Engagement)

- **Legalitas:** Hanya dilakukan pada aset yang masuk dalam cakupan Program Disclosure Vulnerability (VDP) atau seizin pemilik aset.
- **Etika:** Tidak melakukan perubahan data (Read-only) saat menemukan kerentanan.
- **Reporting:** Segala temuan kritikal harus segera dilaporkan ke instansi terkait .

---

## Catatan Mendatang (Next Steps)

- [ ] Buat file detail `GOOGLE_DORK.md`
- [ ] Buat file detail `SHODAN_QUERIES.md`
- [ ] Buat file detail `GITHUB_SECRETS.md`
- [ ] Buat file detail `CLOUD_BUCKETS.md`

---

_Dibuat untuk keperluan edukasi dan penguatan keamanan siber nasional._
