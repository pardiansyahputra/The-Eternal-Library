# Setup Environment Mobile Testing For kali linux Vmware
---
###### Tanggal Riset: 18/03/2026 11:09
###### Kategori: environment / Mobile Testing

Berikut ini saya paparkan informasi terkait dengan cara setup awal dalam membuat environment untuk persiapan mobile testing, dalam tutorial ini saya pribadi mencoba menggunakan kali linux sebagai os-nya dan menggunakan HP vivo sebagai Objek-nya

**A. setup Tahap 1**
+ sambungkan HP dengan Laptop dengan menggunakan kabel USB (yang bisa tranferdata kabelnya ya..)
+ masuk ke developer mode didalam HP (setiap HP punya cara masing masing)
+ jika sudah berhasil jadi developer mode, masuk ke opsi developer yang ada di HP
+ di bagian `Debugging` hidupkan bagian `Debugging USB`

**B. Setup Tahap 2**
setelah selesai setup Tahap 1, lakukan tata cara berikut ini:
+ masuk ke vmware (kali linuxnya jangan dihidupkan dulu!)
+ di bagian Pengaturan `network` jadikan dia `NAT` (disini konsepnya HP saya menjadi tempat testing dan sekaligus menjadi Hostpost untuk Laptop saya nantinya), jika kalian menggunakan wifi rumah sebgai pusat jaringannya bisa pakai `Bridget Adapter`
+ kemudian masuk ke bagian Pengaturan `USB`, tambahkan HP kalian yang sudah terhubung melalui kabel data tadi (pastikan terceklis)
+ kemudian jalankan kali linux nya ...(biasanya terpapar nama HP di tampilan Desktop nantinya[itu penyimpanan HPnya] )

**C Setup Tahap 3**
setelah selesai Setup Tahap 2, lakukan tata cara berikut ini :
+ install alat mirroring dengan command ini :
```bash
#tulis di terminal
sudo apt update && sudo apt install scrcpy
```
+ lakukan Reverse Proxy dengan command berikut ini :
```bash
#tulis di terminal
adb reverse tcp:8080 tcp:8080
```
> kamu harus melakukn ini setiap kali ingin menjalankan nantinya
+ Set Proxy Global: Ketik ini untuk memaksa HP kirim data ke Burp tanpa setting WiFi:
```bash
#tulis di terminal
adb shell settings put global http_proxy 127.0.0.1:8080
```
> kamu harus melakukan command ini setiap kali menjalankan

**D. Setup Tahap 4**
setelah selesai melakukan konfigurasi di setup tahap 3, lakukan tahapan tahapan ini:

+ masuk ke Konfigurasi Burp Suite
+ kemudian masuk ke pengaturannya tepatnya dibagian Proxy Listeners: Di tab Proxy > Settings, klik Edit pada port 8080.
+ kemudian tekan Bind Address: Ubah dari `Loopback only` menjadi `All interfaces`.
+ kemudian nyalakan burpsutie dan Intercept: Pastikan tab Intercept posisinya ON.

**E. Setup Tahap 5**
setelah selesai melakukan konfigurasi di setup 4, lakukan beberapa tahapan ini

+ Buka browser HP, akses http://burp. Download CA Certificate.
+ Buka File Manager HP, Rename file `cacert.der`hasil download tadi menjadi burp.cer.
+ kemudian di Hp kalian Buka Settings > Security > Encryption & credentials > Install a certificate > CA Certificate.
+ Pilih file burp.cer tadi dan install.
+ JIKA ADA PERINGATAN IZINKAN SAJA (sebab sekarang kita memonitoring jaringan HP kita melalui laptop dengan Burpsuite)

***NOTE***
>Ditahap 3 setelah command `1. install alat mirroring` coba lakukan perintah ini :
```bash
#tulisa di terminal
adb devices
```
jika hasil dari perintah nya adalah seperti ini (itu berarti HP berhasil terhubung dengan terminal kali)

```bash
#di terminal
┌──(kali㉿kali)-[~/Desktop]
└─$ adb devices                                                                                                               
List of devices attached
*********01F8 device [ini angka dari HP kamu]
```

namun jika hasilnya seperti ini (artinya HP gagal Terhung dengan terminal kali)
```bash
#di terminal
┌──(kali㉿kali)-[~/Desktop]
└─$ adb devices                                                                                                               
List of devices attached
[TIDAK ADA ANGKA DISINI ]
```


TATA CARA PEMECAHAN MASALAH:
1. lakukan beberapa kali percobaan di setup bagian 1 dan 2 