# REVERSE SHELL OOXML

###### Materi: penjelasan umum terkait lab reverse shell

###### Media: docx/docm + cloudflareTunneling

###### Tanggal mulai riset: 01/06/2026

---

**Penjelasan**
REVERSE SHELL OOXML didasari dari penasaran saya setelah melakukan analisis awal untuk membuat [alat analisis OOXML](/Tools-Reference/Tool-OOXML-Analisis/README.md). selain itu saya mencoba menggunakan http bukan TCP dalam melakukan testing ini dengan memanfaatkan [cloudflare tuneeling](/Writeups/2026-03-26-analisis-phising-dengan-methode-tunneling-dan-vektor-sosial-engineering.md) sebagaimana dokumenasi [cloudflare](/Lab-Setup/phising-&-Data-Exfiltration-Research/README.md)

**rangkuman alat**

- menggunakan tunneling dalam hubungan (agar bisa berbicara lintas jaringan)
- tidak menggunakan TCP murni
- memanfaatkna file OOXML (terutama docx/docm) dan macro di VBA
- sejauh ini - berhasil hanya dengan pengecekan VBA macro dimatikan

**Baca selangkapnya**

- [Ide awal dalam prosesnya](ide-awal.md)
- [Terkain DOH](mencoba-DOH.md)
- [setup macro dan VBA](setup-macro&VBA.md)
