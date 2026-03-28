# Panduan penggunaan Environment Mobile Testing For kali linux Vmware (Cheat Sheet Harian)
---
###### Tanggal Riset: 18/03/2026 11:09
###### Kategori: Cheat Sheet Harian / Mobile Testing

Tahapan-tahapan yang ada dibawah ini merupakan `Cheat Sheet Harian` yang hanya berlaku jika sudah melakukan `setup environment` terlebih dahulu, jika belum harap melakukan `setup environtement` kunjungi ini : [setup environment](setup-environment.md)

**1. Tahap Persiapan (The Start-up)**
Lakukan urutan ini setiap kali baru menyalakan laptop dan HP :

+ Colok USB > Pastikan di VirtualBox/VMware HP sudah tercentang masuk ke Kali.

+ Cek Koneksi:
```Bash
#tulis diterminal
adb devices
(Pastikan muncul tulisan device).
```

+ Buka Mirroring (Biar enak lihat HP):
```Bash
#tulis di terminal
scrcpy
```

+ Buka Pipa Data (Wajib!):
```Bash
#tulis di terminal
adb reverse tcp:8080 tcp:8080
```

+ Aktifkan Penyadapan (Proxy):
```Bash
#tulis di terminal
adb shell settings put global http_proxy 127.0.0.1:8080
```

**2. Tahap Selesai (The Cleanup)**
PENTING! Jangan langsung cabut kabel, nanti HP vivo kamu tidak bisa internetan (karena masih mencari Proxy 8080 yang sudah mati).

+ Matikan Proxy di HP:
```Bash
#tulis di terminal
adb shell settings put global http_proxy :0
```
+ Tes Internet HP: Buka browser di HP, pastikan sudah lancar tanpa Burp.

---
***TAMBAHAN PENTING***

jika suatu waktu terjadi perebutan port yang mana dia selalu connect ke windows kamu dan tidak mau connect ke vmware kali linux kamu, maka lakukan cara dibawah ini:
+ lakukan set-up seperti penjelasan sebelumnya
+ jika dia connect ke windows pertama kali, lakukan command ini didalam directory adb di windows:
```Bash
adb kill-server
```
+ maka dia akan terputus dari windows dan colokkan lagi ke vmware & aktifkan dia di sana
+ jika keduanya tidak ada yang di kenali oleh `adb` maka hapus port di vmware lalu sambungkan lagi dan colok kabelnya ,maka pop up akan keluar `tanda adb sudah di kenali kembali`
+ dan berhasil....
