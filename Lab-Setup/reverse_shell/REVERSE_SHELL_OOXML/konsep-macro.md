# Menggunakan Konsep Macro dalam Bentuk .docm

###### Materi: penjelasan umum terkait lab reverse shell 
###### Media:  docx/docm + cloudflareTunneling
---
**penjelasan**
Di pembahasan kali ini kita akan membahas cara membentuk reverse shell dalam `file .docm`, hal ini dibagun atas fitur kekuatan yang disediakan MS-Word. macro memungkinkan semua orang untuk menjalakan sistem secara otomatis dengan basis kekuatan yang kuat. hal ini yang nanti kita manfaatkan untuk mejalankan reverse shell.

****cara kerja****
+ attacker membuat macro file dan disimpan dengan extensi `.docm`
+ Didalam file terdapat module macro yang sudah di inject dengan url tunneling - ini yang akan berkomunikasi dengan kita
+ korban membuka file  > file berjalan > jalur komunikasi terbuka

**kelebihan & kekurangan**
Bisa saya sampaikan methode ini tidak sepenuhnay sempurna, ketika tulisan ini pertama kali saya buat. sebab ada kelebihan & kekurangan yang sangat jelas didalam methode ini.

***kelebihan***
+ disini kita menggunakan http/https dalam melakukan percobaan ini (tidak dengan TCP murni). hal ini didasari dari ide saya dengan memanfaatkan cloudflare tunneling - ALASANYA ? 
    + orang yang membedah file akan sedikit kesulitan membedah file ini sebab tidak ada pertinggal dari attcker - sebab Ling cloudflare tuneeling selalu berubah
    + gratis - ya , ini free kita bebas menggunakan nya berapa kali dan untuk penggunaan yang pernah saya coba ini cukp baik

***kekurangan***
+ tidak seperti  reverse shell lainnya , methode ini tidak bisa menjalankan command berat seperti membuka cmd.exe , namun masih bisa digunakan untuk promting di cmd korban tersebut - KENAPA ?- hal ini terjadi sebab kita menggunakan http/https untuk saling berkomunikasi tidak seperti TCP murni
+ sedikit rumit - jika kita tidak menggunakan otomatisasi, ketika kita memulain setup kita harus menjalankannya satu per satu
+ alert pada sistem - ya pada saat saya menjalankan ini , alert pada sistem tetap mucul sebab kita menjalakan konsep macro dan MS_WORD memberikna peringatan kepada user yang membuka file kita - satu satunya cara yaitu dengan user menonaktifkan alert tersebut