# Menggunakan Konsep template injection

###### Materi: penjelasan umum terkait lab reverse shell

###### Media: docx + docm + doct + cloudflareTunneling

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
+ kemudian jalankan `send_cmd.py`

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

+ script code `template.dotm`
