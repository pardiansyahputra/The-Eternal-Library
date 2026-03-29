# TEKNIK DATA HIDING & ANTI-FORENSIK (WINDOWS)

###### Tanggal Riset: 29/03/2026 23:15
###### Kategori: Digital Forensics / Anti-Forensics
###### Media Uji: Internal SSD (NTFS) & Flashdrive 2 GB (FAT32)
---
Pada rangkuman kali ini saya menulis beberapa intisari terhadap temuan yang percobaan yang saya lakukan. mungkin ini adalah tahap awal untuk memahami bagaimana system data tersimpan didalam perangkat kita dan di pembahasan kali ini saya menggunakan `WINDOWS 11`. ada banyak cara yang lebih hebat dari ini, namun ini adalh pintu awal untuk menggenal lebih jauh.

##### I. MANIPULASI SISTEM FILE (OS LEVEL)
**1. Alternate Data Streams (ADS) - "The Ghost File"**
Teknik menyembunyikan data di dalam stream tambahan pada sistem `file NTFS`.
```bash
# Perintah Pembuatan: 
type rahasia.txt > induk.txt:rahasia.txt
# Cara Deteksi:
dir /r (Hanya di CMD, tidak terlihat di Explorer).
# Cara Eksekusi:
start notepad induk.txt:rahasia.txt
```
***penjelasan***
dalam skenario ini file seakan akan di lengketkan satu sama lain dan perlu di ingat ini hanya berlaku untuk `file NTFS` Karakteristik: File induk tidak berubah ukuran. Data hilang jika dipindah ke Flashdisk (FAT32/exFAT).

jika pengguna hanya membuka `induk.txt` saja. maka isi dalam file `induk.txt:rahasia.txt` tidak akan kelihatan. untuk itu disarankan membukanya dari `TERMINAL`


**2. Folder Cloaking (The God Mode Trick)**
Mengubah identitas folder menjadi objek sistem Windows menggunakan kode CLSID.

Perintah: 
```bash
ren "NamaFolder" "NamaFolder.{21EC2020-3AEA-1069-A2DD-08002B30309D}"
```

Efek: Folder berubah menjadi ikon Control Panel. Jika diklik, akan membuka Control Panel asli.

+ Kode Lain: {645FF040-5081-101B-9F08-00AA002F954E} untuk berubah menjadi Recycle Bin.

##### II. MANIPULASI STRUKTUR FILE (FILE LEVEL)
**3. Binary Copy (Polyglot File)**
Menggabungkan dua file berbeda format menjadi satu file tunggal yang valid.

```bash
# Perintah:
copy /b gambar.jpg + rahasia.zip hasil_rahasia.jpg

# Cara Akses: 
Klik kanan > Open With > WinRAR/7-Zip.
```
Kelebihan: Tahan banting (Bisa di email, WA, dan Flashdisk FAT32). Bypass deteksi antivirus dasar.

**4. Header Sabotage (Killing Executables)**
Merusak identitas file .exe secara manual agar tidak bisa dijalankan oleh orang lain.

+ Metode: Buka `.exe` via Notepad.
+ Eksekusi: Ubah karakter `MZ` di baris paling awal menjadi `XX`.
+ Efek: Windows akan memberikan error "This app can't run on your PC".
+ Recovery: Kembalikan `XX` menjadi `MZ` untuk menormalkan kembali.

##### III. TEKNIK PENYAMARAN (OBFUSCATION)
**5. Extension Mimicry (Penyamaran Ekstensi)**
Mengganti ekstensi file menjadi file sistem yang membosankan untuk menghindari kecurigaan.Kamu bisa lakukan ganti extensi dulu jika diinginkan

> Contoh:mainan.exe -> wind.dll atau vcruntime140.sys.

command :
```bash 
attrib +s +h +r "nama_file.dll" 
# (Membuat file benar-benar hilang dari pandangan Explorer).
```
***penjelasan***
+ `+s`: File Sistem (sangat rahasia).
+ `+h`: Hidden (tersembunyi).
+ `+r`: Read-only (tidak bisa diedit/hapus sembarangan).

+ Cara Melihat Kembali: Ketik `attrib -s -h -r "nama_file.dll".`

**6. Invisible Folder (Unicode Trick)**
Membuat folder yang ada di sistem namun tidak terlihat secara visual.

+ Nama: Gunakan Unicode NADS atau ALT+255 (Numpad) untuk nama kosong.
+ Ikon: Ganti ikon folder ke ikon transparan melalui Properties > Customize.

**7. melakukan double extensi**
kamu juga bisa melakukan double extensi, namun hal itu terkadang banyak disadari oleh pengguna, seperti cotoh penerapan ini `harap lakukan di CMD`

contoh:
```bash
ren main.exe tugas_kuliah.pdf.exe
```
kamu akan mendapati hasil sebagai berikut:
```bash
tugas_kuliah.pdf
#padahal sebenarnya dia adalah .exe
```

**8.Tambahan**
kamu bisa melakukan sebuah command berjalan di latar belakang tampa terlihat membuka cmd, dengan contoh penerapan di bawah ini:

+ pastikan di windows kamu bisa melakukan complile dengan gcc
+ buat file dalam bahasa c. contoh:`main.c`
+ dengan isi seperti ini :
```c
#include <windows.h>
#include <stdio.h>

// Fungsi XOR sederhana untuk dekripsi string saat runtime
void obfuscate(char *data, char key, int len) {
    for (int i = 0; i < len; i++) {
        data[i] ^= key;
    }
}

int main() {
    // Pesan: "Selamat Anda Kena Prank!" yang sudah di-XOR dengan kunci 'K'
    // Tujuannya agar saat discan, kata "Prank" tidak terbaca sebagai teks biasa
    char secret_msg[] = {0x1a, 0x2c, 0x25, 0x28, 0x24, 0x28, 0x3d, 0x69, 0x08, 0x27, 0x2d, 0x28, 0x20, 0x69, 0x02, 0x2c, 0x27, 0x28, 0x69, 0x19, 0x3b, 0x28, 0x27, 0x22, 0x68}; 
    int msg_len = sizeof(secret_msg);
    char key = 'K';

    // Junk Code: Operasi matematika tidak berguna untuk mengecoh penganalisa otomatis
    int x = 100; x = (x * 2) / 2; if (x < 1) return 0;

    // Dekripsi pesan hanya saat program dijalankan (di memori)
    obfuscate(secret_msg, key, msg_len);

    // Eksekusi Pesan (Menggunakan MessageBox API Windows)
    MessageBoxA(NULL, secret_msg, "System Update", MB_OK | MB_ICONINFORMATION);

    // Simulasi Membuka Browser (Rickroll atau edukasi)
    ShellExecute(NULL, "open", "https://www.youtube.com/watch?v=dQw4w9WgXcQ", NULL, NULL, SW_SHOWNORMAL);

    return 0;
}
```
+ kemudian simpan file tersebut dan jalankan command ini :
```bash
gcc main.c -o prank.exe -mwindows
```
***penjelasan***
+ `-o prank.exe`: Nama file output (samarkan).
+ `-mwindows`: Sangat Penting! Ini akan menghilangkan jendela CMD hitam saat program dijalankan, sehingga program benar-benar berjalan "siluman" di latar belakang.

> ini adalah awal dari cara cara lainnya....

##### IV. Tabel Perbandingan Resiliensi (Update)

| Teknik            | Media     | Ketahanan Kirim      | Deteksi Forensik                  |
|------------------|----------|----------------------|----------------------------------|
| ADS NTFS Only    | NTFS     | Lemah (Hilang)       | Menengah (dir /r)                |
| Binary Copy      | Semua    | Sangat Kuat          | Tinggi (Cek ukuran file)         |
| Mimicry          | Semua    | Kuat                 | Menengah (Cek Header)            |
| Header Sabotage  | Semua    | Sangat Kuat          | Sulit bagi orang awam            |
| Invisible Folder | Semua    | Lemah                | Mudah (Select All)               |

## PERHATIAN
+ DI HARAPKAN JANGAN MELAKUKAN DI SYSTEM UTAMA `JIKA INGIN MELAKUKAN PERCOBAAN YANG LAIN / TIDAK AMAN`
+ DILARANG UNTUK DILAKUKAN TERHADAP DEVICE MILIK ORANG LAIN. SEBAB LANGKAH AWAL DARI KEGIATAN KEJAHATAN
+ SEMUA HAL INI HANYALAH EDUKASI SAJA