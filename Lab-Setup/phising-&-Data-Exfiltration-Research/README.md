# Panduan penggunaan dan source code phising & data extrafiltration 

hai semuanya, pada folder ini saya akan menjelaskan terkait phising & data extrafiltration, hal ini saya bangun untuk tujuan edukasi saja dan segala tindakan yang ilegal adalah berbahaya, kemudian saya sudah membaut beberapa contoh sourcode dalam latihan ini. 

Dalam penjelasan kali ini saya menggunakan Device sebagai berikut ini:
+ Laptop: sebagai tempat tunneling berjalan dan tempat analisis
+ HP: sebagai contoh korban
+ VScode: tempat script code dijalankan nantinya
+ Tools : Cloudflared Tunneling (untuk menghubungkan script kita ke website yang memiliki url dan bisa diakses secara umum) [link download](https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe  )

berikut beberapa penjelasan
+ Disetipa source code kamu harus menyesuikan dengan Path penyimpanan di Laptop kamu
+ kamu bisa menjalankannya di laptop untuk testing cepat atau bisa juga dengan tunneling cloudflared untuk membaut url umum (BACA BAGIAN `penjelasan singkat`)
+ sourcode dibuat secara bertahap, mulai dari `phising-1.py` yang menandakan contoh simple simulasi-nya dan begitu seterusnya

***NB:semua hal yang ada di sini untuk tujuan edukasi saja, kami tidak membernarkan tindakan yang melanggar hukum!!***


+ Write up saya : [penjelasan singkat](/Writeups/2026-03-26-analisis-phising-dengan-methode-tunneling-dan-vektor-sosial-engineering.md)
+ source code simpel: [phising-1](phising-1.py)
+ source code varian: [phising-2](phising-2.py)
+ source code lengkap: [phising-3](phising-3-&-data-exfiltration.py)
+ source code simulasi banking: [phising-4](phising-4-for-simulation-bank.py)