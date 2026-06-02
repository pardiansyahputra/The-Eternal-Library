import os
import re
import sys
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import zipfile
import shutil
import xml.etree.ElementTree as ET
from xml.dom import minidom
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import networkx as nx
from lxml import etree as LET  

# Import komponen ReportLab untuk cetak PDF
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# --- CONFIGURATION & MAPS ---
GRAPH_LEVEL_COLORS = {
    0: "#2ECC71",  # Root
    1: "#3498DB",  # Level 1save_xml_changes
    2: "#9B59B6",  # Level 2
    3: "#E67E22",  # Level 3
    4: "#E74C3C"   # Level 4+
}

XML_EDUCATION_MAP = {
     # --- Elemen Dasar & Dokumen Teks (WordprocessingML / .docx) ---
    'p': 'Paragraph: Blok teks utama atau satu paragraf penuh.',
    'r': 'Text Run: Kontainer teks yang memiliki properti/formatting yang sama (misal sekumpulan kata yang bold).',
    't': 'Text Node: Kontainer string teks aktual tempat karakter tulisan disimpan.',
    'rPr': 'Run Properties: Mengatur formatting huruf internal (Bold, Italic, Font Family, Size).',
    'pPr': 'Paragraph Properties: Mengatur formatting paragraf (Alignment, Spacing, Indentasi).',
    'body': 'Body: Kontainer utama yang membungkus seluruh konten dokumen struktural.',
    'hyperlink': 'Hyperlink: Tautan referensi menuju URL eksternal atau jangkar internal.',
    'br': 'Break: Perintah pembatas baris (Line break) di dalam run.',
    'sectPr': 'Section Properties: Mengatur properti satu bagian dokumen (Ukuran halaman, orientasi, margin).',
    'fldSimple': 'Simple Field: Kontainer untuk teks dinamis otomatis seperti nomor halaman (PAGE).',
    'instrText': 'Instruction Text: String instruksi/kode mentah untuk Field Codes (seperti formula mail merge).',
    'sym': 'Symbol: Kontainer khusus untuk menyisipkan karakter simbol atau special character dari font.',
    'lastRenderedPageBreak': 'Last Rendered Page Break: Penanda jejak posisi pemotongan halaman otomatis terakhir oleh aplikasi.',
    
    # --- Properti & Pemformatan Huruf/Paragraf Lanjutan ---
    'color': 'Color: Menentukan warna teks menggunakan nilai heksadesimal (Hex RGB) di dalam rPr.',
    'sz': 'Size: Menentukan ukuran huruf (font size) dalam satuan half-points (nilai 24 = 12pt).',
    'szCs': 'Complex Script Size: Menentukan ukuran huruf untuk karakter skrip kompleks seperti Arab atau Ibrani.',
    'jc': 'Justification: Mengatur perataan teks (Alignment) pada paragraf (left, right, center, both).',
    'ind': 'Indentation: Mengatur jarak indentasi paragraf (batas kiri, kanan, baris pertama, atau hanging indent).',
    'b': 'Bold: Tag biner atau sakelar untuk mengaktifkan pemformatan tebal pada huruf.',
    'i': 'Italic: Tag biner atau sakelar untuk mengaktifkan pemformatan miring pada huruf.',
    'u': 'Underline: Mengatur gaya garis bawah pada teks (misal: single, double, dotted).',
    'rFonts': 'Run Fonts: Menentukan jenis font (Font Family) yang digunakan untuk teks (ASCII, High ANSI, Complex Script).',
    'shd': 'Shading: Mengatur warna latar belakang (highlight/background) pada teks atau sel tabel.',
    'highlight': 'Highlight: Memberikan efek stabilo warna pada teks run.',
    'spacing': 'Spacing: Mengatur jarak antar baris teks (line spacing) atau jarak sebelum/sesudah paragraf.',
    'rStyle': 'Run Style: Merujuk pada ID gaya huruf kustom yang didefinisikan di file styles.xml.',
    'pStyle': 'Paragraph Style: Merujuk pada ID gaya paragraf global (seperti Heading 1, Normal, Title).',

    # --- Struktur Tabel (Table Elements) ---
    'tbl': 'Table: Struktur pembungkus tabel dokumen.',
    'tr': 'Table Row: Representasi baris di dalam tabel.',
    'tc': 'Table Cell: Representasi kolom atau sel spesifik di dalam baris tabel.',
    'tblPr': 'Table Properties: Mengatur properti global dari tabel seperti lebar default dan gaya garis tepi.',
    'tblGrid': 'Table Grid: Mendefinisikan struktur kolom dasar tabel dan menentukan lebar statis masing-masing kolom.',
    'gridCol': 'Grid Column: Menentukan lebar spesifik dari satu kolom yang terdaftar di dalam tblGrid.',
    'tblBorders': 'Table Borders: Kontainer untuk mengatur jenis, ketebalan, dan warna garis tepi pada tabel.',
    'tcPr': 'Table Cell Properties: Mengatur profesionalitas spesifik sel individu (warna latar, margin, atau merge).',
    'vMerge': 'Vertical Merge: Mengindikasikan bahwa sebuah sel digabungkan secara vertikal dengan sel di sekitarnya.',
    'gridSpan': 'Grid Span: Menentukan jumlah kolom horizontal yang digabungkan (merge) ke samping oleh satu sel.',
    'cantSplit': 'Cant Split: Instruksi agar baris tabel tidak terpotong ke halaman berikutnya jika berada di batas halaman.',
    'tblHeader': 'Table Header: Menandakan bahwa baris tabel tersebut adalah header yang akan diulang di setiap halaman baru.',

    # --- Sistem Penomoran & List (Numbering) ---
    'numPr': 'Numbering Properties: Mengaitkan paragraf dengan sistem penomoran otomatis atau bullet point.',
    'numId': 'Numbering ID: ID referensi yang menghubungkan paragraf ke definisi penomoran di numbering.xml.',
    'ilvl': 'Indent Level: Menentukan tingkatan hierarki/level pada list penomoran (dimulai dari level 0).',

    # --- Referensi, Catatan, & Komentar ---
    'footnote': 'Footnote: Kontainer isi teks catatan kaki yang terletak di bagian bawah halaman.',
    'endnote': 'Endnote: Kontainer isi teks catatan akhir yang terletak di bagian paling akhir dokumen.',
    'footnoteReference': 'Footnote Reference: Penanda berupa angka kecil (superscript) di teks utama yang merujuk pada footnote.',
    'comment': 'Comment: Kontainer teks komentar yang disematkan oleh peninjau (reviewer) pada area teks.',
    'commentRangeStart': 'Comment Range Start: Penanda titik awal dari teks yang disorot (highlighted) oleh sebuah komentar.',
    'commentRangeEnd': 'Comment Range End: Penanda titik akhir dari teks yang disorot oleh sebuah komentar.',

    # --- Elemen Lembar Kerja (SpreadsheetML / .xlsx) ---
    'worksheet': 'Worksheet: Struktur utama root dari lembar kerja spreadsheet (Xlsx).',
    'sheetData': 'Sheet Data: Kumpulan baris (rows) dan kolom yang berisi sel data.',
    'row': 'Row: Baris horizontal pada lembar kerja.',
    'c': 'Cell: Sel spesifik tempat koordinat data berada (misal: A1, B5).',
    'v': 'Value: Nilai mentah (raw data) yang disimpan di dalam sel.',
    'f': 'Formula: Rumus atau formula kalkulasi matematis/logika sel.',
    'cols': 'Columns Collection: Kontainer global untuk mengatur konfigurasi sekelompok kolom pada worksheet.',
    'col': 'Column Definition: Mengatur properti spesifik satu atau beberapa kolom (lebar atau status hidden).',
    'extLst': 'Extension List: Kontainer fleksibel untuk menyimpan data fitur baru atau metadata kustom.',
    'is': 'Inline String: Kontainer alternatif untuk menyimpan teks langsung di dalam sel tanpa Shared Strings Table.',
    'sst': 'Shared Strings Table: Root elemen file sharedStrings.xml yang menyimpan semua string teks unik dokumen.',
    'si': 'String Item: Entri teks individu di dalam Shared Strings Table.',
    'definedNames': 'Defined Names Collection: Kumpulan nama kustom yang dibuat untuk merujuk pada suatu range sel atau formula.',
    'definedName': 'Defined Name: Menentukan satu nama referensi range sel spesifik (Named Range).',
    'mergeCells': 'Merge Cells Collection: Daftar seluruh koordinat range sel yang digabungkan (merged) di dalam satu worksheet.',
    'mergeCell': 'Merge Cell: Menentukan koordinat spesifik dari satu area sel yang digabungkan (misal: ref="A1:B3").',
    'conditionalFormatting': 'Conditional Formatting: Aturan pemformatan bersyarat yang diterapkan pada range sel tertentu.',
    'cfRule': 'Conditional Formatting Rule: Aturan logika spesifik di dalam pemformatan bersyarat.',
    'dataValidations': 'Data Validations Collection: Kumpulan aturan pembatasan input data yang diperbolehkan masuk ke sel.',
    'dataValidation': 'Data Validation: Aturan validasi spesifik untuk satu range sel (seperti tipe dropdown list).',
    'numFmt': 'Number Format: Mendefinisikan format tampilan angka di sel (misal format mata uang, tanggal, desimal).',
    'pane': 'Pane: Mengatur pembagian tampilan lembar kerja, seperti fitur Freeze Panes.',

    # --- Elemen Slide Presentasi (PresentationML / .pptx) ---
    'sld': 'Slide: Kontainer utama untuk halaman slide presentasi (Pptx).',
    'sp': 'Shape: Elemen bentuk visual, boks, atau kontainer teks di dalam slide.',
    'txBody': 'Text Body: Area penampung teks di dalam sebuah bentuk (shape).',
    'sldTree': 'Slide Tree: Struktur pohon utama yang mengatur urutan, pengelompokan, dan hierarki objek visual slide.',
    'sldLayout': 'Slide Layout: Root elemen untuk file template tata letak slide.',
    'sldMaster': 'Slide Master: Root elemen untuk master slide tertinggi yang mengontrol tema, warna, dan font global.',
    'notes': 'Notes Page: Kontainer halaman catatan pembicara (speaker notes) yang terhubung dengan slide.',
    'nvSpPr': 'Non-Visual Shape Properties: Menyimpan properti non-visual bentuk seperti nama objek, ID, dan status lock.',
    'spPr': 'Shape Properties: Mengatur properti visual geometric objek (posisi X Y, ukuran, warna latar).',
    'xfrm': '2D Transform: Menentukan posisi pergeseran (offset) dan ukuran dimensi objek dalam satuan EMUs.',
    'off': 'Offset: Menentukan koordinat titik awal X dan Y tempat objek diletakkan pada layar.',
    'ext': 'Extents: Menentukan dimensi lebar (cx) dan tinggi (cy) dari ruang kotak pembungkus objek.',
    'prstGeom': 'Preset Geometry: Menentukan bentuk geometris bawaan yang digunakan oleh objek (misal: rect, ellipse).',
    'pLst': 'Paragraph List: Kumpulan blok paragraf di dalam boks teks presentasi.',
    'endParaRPr': 'End Paragraph Run Properties: Informasi pemformatan huruf untuk karakter kosong di akhir paragraf.',
    'blnLst': 'Blend List: Mengatur efek transisi visual antar slide presentasi.',

    # --- Elemen Grafis Umum & Media (DrawingML) ---
    'drawing': 'Drawing: Kontainer biner untuk objek grafis, gambar, atau shape.',
    'blip': 'Binary Large Image Panel: Elemen yang mereferensikan file gambar biner internal melalui ID relasi (r:id).',
    'blipFill': 'Blip Fill: Mengatur bagaimana gambar diposisikan untuk mengisi ruang kontainer (stretch atau tile).',
    'stretch': 'Stretch: Instruksi untuk meregangkan gambar agar memenuhi seluruh area kontainer objek secara penuh.',
    'fillRect': 'Fill Rectangle: Menentukan margin offset pemotongan (cropping) saat gambar diregangkan.',
    'graphic': 'Graphic Object: Kontainer universal untuk objek visual kompleks eksternal (SmartArt, chart, tabel).',
    'graphicData': 'Graphic Data: Menyimpan data spesifik dan skema URI yang menjelaskan jenis objek grafis.',
    'ln': 'Line: Mengatur properti garis luar (outline) dari objek shape atau grafis.',

    # --- Elemen Relasi & Metadata Sistem (Core / Relationships) ---
    'Relationships': 'Relationships Root: Root elemen file .rels yang memetakan hubungan antar file XML atau aset eksternal.',
    'Relationship': 'Individual Relationship: Menentukan satu jalur koneksi spesifik (ID Relasi, Type skema, dan Target file).',
    'coreProperties': 'Core Properties: Root elemen file core.xml yang menyimpan metadata standar (judul, creator, tanggal).',
    'dc:creator': 'Dublin Core Creator: Tag metadata yang menyimpan nama asli pembuat atau akun yang membuat dokumen.',
    'cp:lastModifiedBy': 'Core Properties Last Modified By: Tag metadata yang mencatat nama pengguna terakhir yang memodifikasi dokumen.',
    'appProperties': 'App Properties: Root elemen file app.xml yang menyimpan metadata aplikasi seperti jumlah kata, halaman, atau versi template.',

    # --- Keamanan & Proteksi Dokumen (Security Elements) ---
    'documentProtection': 'Document Protection: Menyimpan konfigurasi pembatasan edit dokumen atau status read-only.',
    'sheetProtection': 'Sheet Protection: Mengunci sel atau struktur worksheet tertentu agar tidak bisa dimodifikasi tanpa izin.',
    'hash': 'Hash Value: Menyimpan nilai hash (seperti algoritma SHA-512) dari password proteksi untuk validasi keamanan.'
}


class MetadataDeepInspectionModule:
    def __init__(self, tab_parent, app_instance):
        self.app = app_instance
        self.tab_inspect = tk.Frame(tab_parent, bg="#1e1e24")
        tab_parent.add(self.tab_inspect, text=" 🕵️ Metadata Deep Inspection ")
        self.metadata_storage = {}
        self.setup_ui()
        
    def setup_ui(self):
        ctrl_frame = tk.Frame(self.tab_inspect, bg="#2a2a35", height=50)
        ctrl_frame.pack(fill=tk.X, padx=5, pady=5)
        
        btn_run = tk.Button(
            ctrl_frame, text="🔍 RUN ULTIMATE DEEP INSPECTION", command=self.run_deep_inspection,
            bg="#3498db", fg="#ffffff", font=("Segoe UI", 9, "bold"), relief=tk.FLAT, padx=10
        )
        btn_run.pack(side=tk.LEFT, padx=5, pady=5)
        
        btn_pdf = tk.Button(
            ctrl_frame, text="📄 EXPORT FORENSIC REPORT TO PDF", command=self.export_to_pdf,
            bg="#2ecc71", fg="#ffffff", font=("Segoe UI", 9, "bold"), relief=tk.FLAT, padx=10
        )
        btn_pdf.pack(side=tk.LEFT, padx=5, pady=5)
        
        tree_frame = tk.LabelFrame(self.tab_inspect, text=" 📊 12-Cluster Deep Forensic Investigation Results ", bg="#1e1e24", fg="#3498db", font=("Consolas", 10, "bold"))
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.tree_meta = ttk.Treeview(tree_frame, columns=("Cluster", "Property", "Value"), show="headings")
        self.tree_meta.heading("Cluster", text="Kluster Forensik")
        self.tree_meta.heading("Property", text="Properti / Indikator")
        self.tree_meta.heading("Value", text="Nilai Temuan Lapangan")
        
        self.tree_meta.column("Cluster", width=180, anchor=tk.W)
        self.tree_meta.column("Property", width=250, anchor=tk.W)
        self.tree_meta.column("Value", width=650, anchor=tk.W)
        self.tree_meta.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
    def _parse_xml_safely(self, xml_path):
        if not os.path.exists(xml_path): return None
        try:
            secure_parser = LET.XMLParser(resolve_entities=False, no_network=True)
            return LET.parse(xml_path, parser=secure_parser)
        except Exception: return None

    def run_deep_inspection(self):
        if not hasattr(self.app, 'extract_dir') or not self.app.extract_dir or not os.path.exists(self.app.extract_dir):
            messagebox.showwarning("Peringatan", "Silakan load berkas OOXML terlebih dahulu di Tab Utama!")
            return
            
        for item in self.tree_meta.get_children(): self.tree_meta.delete(item)
        self.metadata_storage.clear()
        
        R = self.app.extract_dir

        # ====================================================================
        # 1. CORE METADATA
        # ====================================================================
        c_name = "1. Core Metadata"
        self.metadata_storage[c_name] = []
        core_path = os.path.join(R, "docProps", "core.xml")
        tree = self._parse_xml_safely(core_path)
        fields = {
            "title": ".//dc:title", "subject": ".//dc:subject", "creator": ".//dc:creator",
            "lastModifiedBy": ".//cp:lastModifiedBy", "created": ".//dcterms:created", "modified": ".//dcterms:modified",
            "keywords": ".//cp:keywords", "description": ".//dc:description", "category": ".//cp:category",
            "contentStatus": ".//cp:contentStatus", "revision": ".//cp:revision", "language": ".//dc:language",
            "identifier": ".//dc:identifier", "version": ".//cp:version"
        }
        ns = {'cp': 'http://schemas.openxmlformats.org/package/2006/metadata/core-properties', 'dc': 'http://purl.org/dc/elements/1.1/', 'dcterms': 'http://purl.org/dc/terms/'}
        for k, xpath in fields.items():
            val = "N/A"
            if tree:
                el = tree.getroot().find(xpath, namespaces=ns)
                if el is not None and el.text: val = el.text
            self.tree_meta.insert("", tk.END, values=(c_name, k, val))
            self.metadata_storage[c_name].append((k, val))

        # ====================================================================
        # 2. APP METADATA
        # ====================================================================
        c_name = "2. App Metadata"
        self.metadata_storage[c_name] = []
        app_path = os.path.join(R, "docProps", "app.xml")
        tree = self._parse_xml_safely(app_path)
        fields = {
            "Application": ".//ap:Application", "AppVersion": ".//ap:AppVersion", "Company": ".//ap:Company",
            "Manager": ".//ap:Manager", "Template": ".//ap:Template", "TotalTime": ".//ap:TotalTime",
            "Pages": ".//ap:Pages", "Words": ".//ap:Words", "Characters": ".//ap:Characters",
            "CharactersWithSpaces": ".//ap:CharactersWithSpaces", "Lines": ".//ap:Lines", "Paragraphs": ".//ap:Paragraphs",
            "Slides": ".//ap:Slides", "Notes": ".//ap:Notes", "HiddenSlides": ".//ap:HiddenSlides",
            "MMClips": ".//ap:MMClips", "PresentationFormat": ".//ap:PresentationFormat", "SharedDoc": ".//ap:SharedDoc",
            "HyperlinksChanged": ".//ap:HyperlinksChanged", "LinksUpToDate": ".//ap:LinksUpToDate",
            "ScaleCrop": ".//ap:ScaleCrop", "DocSecurity": ".//ap:DocSecurity"
        }
        ns = {'ap': 'http://schemas.openxmlformats.org/officeDocument/2006/extended-properties'}
        for k, xpath in fields.items():
            val = "N/A"
            if tree:
                el = tree.getroot().find(xpath, namespaces=ns)
                if el is not None and el.text: val = el.text
            self.tree_meta.insert("", tk.END, values=(c_name, k, val))
            self.metadata_storage[c_name].append((k, val))

        # ====================================================================
        # 3. CUSTOM METADATA
        # ====================================================================
        c_name = "3. Custom Metadata"
        self.metadata_storage[c_name] = []
        custom_path = os.path.join(R, "docProps", "custom.xml")
        tree = self._parse_xml_safely(custom_path)
        req_custom = ["EmployeeID", "Department", "ProjectID", "WorkflowState", "TicketID", "InternalUUID", "BuildVersion", "ApprovalStatus", "Environment", "Owner", "Reviewer", "CostCenter", "Confidentiality"]
        found_custom = {}
        if tree:
            ns = {'ct': 'http://schemas.openxmlformats.org/officeDocument/2006/custom-properties'}
            props = tree.getroot().findall(".//ct:property", namespaces=ns)
            for p in props:
                name = p.get("name", "")
                children = p.getchildren()
                val = children[0].text if children and children[0].text else "N/A"
                if name: found_custom[name] = val
        for k in req_custom:
            val = found_custom.get(k, "N/A")
            self.tree_meta.insert("", tk.END, values=(c_name, k, val))
            self.metadata_storage[c_name].append((k, val))

        # ====================================================================
        # 4. RELATIONSHIP METADATA (*.rels) & GLOBAL URL ANALYSIS
        # ====================================================================
        c_name = "4. Relationship Metadata"
        self.metadata_storage[c_name] = []
        rels_data = {"Relationship Id": [], "Type": [], "Target": [], "TargetMode": [], "External URL": [], "Hyperlink": [], "Image Reference": [], "Embedded Object": [], "OLE Object": [], "VBA Relation": [], "Template Relation": [], "Package Relation": []}
        
        for root_dir, _, files in os.walk(R):
            for file in files:
                if file.endswith('.rels'):
                    tree_r = self._parse_xml_safely(os.path.join(root_dir, file))
                    if tree_r:
                        ns = {'rel': 'http://schemas.openxmlformats.org/package/2006/relationships'}
                        for r in tree_r.getroot().findall(".//rel:Relationship", namespaces=ns):
                            r_id, r_type, target, mode = r.get("Id", "N/A"), r.get("Type", "N/A"), r.get("Target", "N/A"), r.get("TargetMode", "Internal")
                            rels_data["Relationship Id"].append(r_id)
                            rels_data["Type"].append(r_type)
                            rels_data["Target"].append(target)
                            rels_data["TargetMode"].append(mode)
                            
                            if mode == "External": rels_data["External URL"].append(target)
                            if "hyperlink" in r_type.lower(): rels_data["Hyperlink"].append(target)
                            if "image" in r_type.lower(): rels_data["Image Reference"].append(target)
                            if "oleobject" in r_type.lower(): rels_data["OLE Object"].append(target)
                            elif "ole" in r_type.lower() or "package" in r_type.lower(): rels_data["Embedded Object"].append(target)
                            if "vba" in r_type.lower() or "macro" in r_type.lower(): rels_data["VBA Relation"].append(target)
                            if "template" in r_type.lower(): rels_data["Template Relation"].append(target)
                            if "package" in r_type.lower(): rels_data["Package Relation"].append(target)

        for k, v_list in rels_data.items():
            val = " | ".join(set(v_list)) if v_list else "N/A"
            self.tree_meta.insert("", tk.END, values=(c_name, k, val))
            self.metadata_storage[c_name].append((k, val))

        # ====================================================================
        # REKURSION DAN PEMETAAN UNTUK DATA KLUSTER 5 SAMPAI 12
        # ====================================================================
        all_paths = []
        for root_dir, _, files in os.walk(R):
            for file in files: all_paths.append(os.path.relpath(os.path.join(root_dir, file), R).replace("\\", "/"))

        def check_exist(patterns):
            matches = [p for p in all_paths if any(re.search(pat, p, re.IGNORECASE) for pat in patterns)]
            return " | ".join(matches) if matches else "N/A"

        # 5. DOCX METADATA
        c_name = "5. DOCX Metadata"
        self.metadata_storage[c_name] = []
        docx_map = {
            "document.xml": ["word/document.xml"], "styles.xml": ["word/styles.xml"], "settings.xml": ["word/settings.xml"],
            "fontTable.xml": ["word/fontTable.xml"], "numbering.xml": ["word/numbering.xml"], "comments.xml": ["word/comments.xml"],
            "footnotes.xml": ["word/footnotes.xml"], "endnotes.xml": ["word/endnotes.xml"], "people.xml": ["word/people.xml"],
            "webSettings.xml": ["word/webSettings.xml"], "header*.xml": ["word/header\d+\.xml"], "footer*.xml": ["word/footer\d+\.xml"],
            "theme": ["word/theme/"], "glossary": ["word/glossary/"], "trackChanges": ["word/settings.xml"], # Track changes diuji di kluster forensik
            "hiddenText": ["word/document.xml"], "embeddedObjects": ["word/embeddings/"], "hyperlinks": ["word/_rels/document.xml.rels"],
            "bookmarks": ["word/document.xml"]
        }
        for k, pats in docx_map.items():
            val = check_exist(pats) if "word/" in "".join(all_paths) else "N/A"
            # Berikan penanda ketersediaan file induknya
            if k in ["trackChanges", "hiddenText", "bookmarks"] and val != "N/A": val = "Available in structure (Scan via Editor)"
            self.tree_meta.insert("", tk.END, values=(c_name, k, val))
            self.metadata_storage[c_name].append((k, val))

        # 6. XLSX METADATA
        c_name = "6. XLSX Metadata"
        self.metadata_storage[c_name] = []
        xlsx_map = {
            "workbook.xml": ["xl/workbook.xml"], "worksheets": ["xl/worksheets/"], "sharedStrings.xml": ["xl/sharedStrings.xml"],
            "styles.xml": ["xl/styles.xml"], "calcChain.xml": ["xl/calcChain.xml"], "connections.xml": ["xl/connections.xml"],
            "externalLinks": ["xl/externalLinks/"], "queryTables": ["xl/queryTables/"], "pivotCache": ["xl/pivotCache/"],
            "slicers": ["xl/slicers/"], "tables": ["xl/tables/"], "namedRanges": ["xl/workbook.xml"],
            "hiddenSheets": ["xl/workbook.xml"], "veryHiddenSheets": ["xl/workbook.xml"], "formulas": ["xl/worksheets/sheet"],
            "charts": ["xl/charts/"], "macros": ["xl/vbaProject.bin", "xl/drawings/vmlDrawing"], "embeddedObjects": ["xl/embeddings/"]
        }
        for k, pats in xlsx_map.items():
            val = check_exist(pats) if "xl/" in "".join(all_paths) else "N/A"
            if k in ["namedRanges", "hiddenSheets", "veryHiddenSheets", "formulas"] and val != "N/A": val = "Available (Requires Deep Parsing)"
            self.tree_meta.insert("", tk.END, values=(c_name, k, val))
            self.metadata_storage[c_name].append((k, val))

        # 7. PPTX METADATA
        c_name = "7. PPTX Metadata"
        self.metadata_storage[c_name] = []
        pptx_map = {
            "presentation.xml": ["ppt/presentation.xml"], "slides/*.xml": ["ppt/slides/slide\d+\.xml"], "notesSlides": ["ppt/notesSlides/"],
            "comments": ["ppt/comments/"], "slideMasters": ["ppt/slideMasters/"], "slideLayouts": ["ppt/slideLayouts/"],
            "handoutMasters": ["ppt/handoutMasters/"], "embeddedFonts": ["ppt/fonts/"], "media": ["ppt/media/"],
            "animations": ["ppt/slides/slide"], "transitions": ["ppt/slides/slide"], "hiddenSlides": ["ppt/presentation.xml"],
            "tags": ["ppt/tags/"], "hyperlinks": ["ppt/slides/_rels/"], "embeddedObjects": ["ppt/embeddings/"]
        }
        for k, pats in pptx_map.items():
            val = check_exist(pats) if "ppt/" in "".join(all_paths) else "N/A"
            if k in ["animations", "transitions", "hiddenSlides"] and val != "N/A": val = "Available in slide configurations"
            self.tree_meta.insert("", tk.END, values=(c_name, k, val))
            self.metadata_storage[c_name].append((k, val))

        # 8. MACRO / VBA METADATA
        c_name = "8. Macro / VBA Metadata"
        self.metadata_storage[c_name] = []
        vba_file = [p for p in all_paths if "vbaProject.bin" in p]
        vba_fields = ["VBA Author", "VBA Modules", "Macro Names", "AutoOpen", "AutoExec", "Form Controls", "Embedded Payload", "Shell Commands", "Obfuscated Strings", "Persistence Logic"]
        for f in vba_fields:
            val = "N/A"
            if vba_file:
                val = f"Detected ({vba_file[0]}) - Use OLE Engine Tab for full decoding"
            self.tree_meta.insert("", tk.END, values=(c_name, f, val))
            self.metadata_storage[c_name].append((f, val))

        # 9. SIGNATURE METADATA
        c_name = "9. Signature Metadata"
        self.metadata_storage[c_name] = []
        sig_files = [p for p in all_paths if "_xmlsignatures" in p or "sig" in p]
        sig_fields = ["Signer Name", "Certificate", "Issuer", "Timestamp", "Digest Method", "Signature Value", "Validation Status"]
        for f in sig_fields:
            val = f"Detected ({sig_files[0]})" if sig_files else "N/A"
            self.tree_meta.insert("", tk.END, values=(c_name, f, val))
            self.metadata_storage[c_name].append((f, val))

        # 10. THUMBNAIL METADATA
        c_name = "10. Thumbnail Metadata"
        self.metadata_storage[c_name] = []
        thumb_file = check_exist(["docProps/thumbnail\.jpeg", "docProps/thumbnail\.png"])
        thumb_fields = {"Preview Image": thumb_file, "Cached Preview": thumb_file, "Old Preview": "N/A", "Embedded EXIF": "N/A"}
        for k, v in thumb_fields.items():
            self.tree_meta.insert("", tk.END, values=(c_name, k, v))
            self.metadata_storage[c_name].append((k, v))

        # 11. EMBEDDED OBJECT METADATA
        c_name = "11. Embedded Object Metadata"
        self.metadata_storage[c_name] = []
        embed_map = {
            "Embedded DOCX": ["embeddings/.*\.docx"], "Embedded XLSX": ["embeddings/.*\.xlsx"], "Embedded PPTX": ["embeddings/.*\.pptx"],
            "Embedded PDF": ["embeddings/.*\.pdf"], "Embedded EXE": ["embeddings/.*\.exe"], "ActiveX Object": ["activeX/.*\.xml"],
            "OLE Package": ["embeddings/.*\.bin", "embeddings/oleObject"], "Binary Payload": ["embeddings/"]
        }
        for k, pats in embed_map.items():
            val = check_exist(pats)
            self.tree_meta.insert("", tk.END, values=(c_name, k, val))
            self.metadata_storage[c_name].append((k, val))

        # ====================================================================
        # 12. HIDDEN / FORENSIC METADATA & SYSTEM LEAKS
        # ====================================================================
        c_name = "12. Hidden / Forensic Metadata"
        self.metadata_storage[c_name] = []
        
        # Ekstraksi Spool Printer & Windows Local Path Carving
        printer_leaks = "N/A"
        printer_files = [p for p in all_paths if "printerSettings" in p]
        if printer_files:
            try:
                with open(os.path.join(R, printer_files[0]), 'rb') as pf:
                    bin_data = pf.read(2048)
                    extracted = [s.decode('utf-8', errors='ignore') for s in bin_data.split(b'\x00') if len(s) > 3]
                    filtered = [s.strip() for s in extracted if any(x in s.lower() for x in ['\\\\', 'c:', 'users', 'printer', 'hp', 'epson', 'canon'])]
                    if filtered: printer_leaks = " | ".join(filtered[:3])
            except Exception: pass

        forensic_dynamic = {
            "Username Windows": "N/A (No active spool leak)" if printer_leaks == "N/A" else "Extracted from Spool Path",
            "Computer Name": "N/A", "Printer Name": printer_leaks, "File Path": printer_leaks if "c:" in printer_leaks.lower() else "N/A",
            "UNC Path": printer_leaks if "\\\\" in printer_leaks else "N/A", "Timezone": "N/A", "Locale": "N/A",
            "Editing Duration": self.tree_meta.item(self.tree_meta.get_children()[19])['values'][2] if len(self.tree_meta.get_children()) > 19 else "N/A", # Mengambil data dari TotalTime
            "Last Printed": "N/A", "Revision Count": "N/A", "Deleted Text": "N/A (Check track changes)", "Track Changes Author": "N/A",
            "Comment Author": "N/A", "Hidden Rows/Columns": "N/A", "Hidden Slides": "N/A", "Hidden Sheets": "N/A",
            "External API URL": rels_data["External URL"][0] if rels_data["External URL"] else "N/A", "SharePoint URL": "N/A", "Internal Server Name": "N/A",
            "SQL Connection String": "N/A", "Email Address": "N/A", "UUID/GUID": "N/A", "Template Path": "N/A",
            "Sync Metadata": "N/A", "Collaboration Metadata": "N/A", "Session Info": "N/A", "Device Info": "N/A"
        }
        
        # Sync dengan core/app metadata jika tersedia
        if len(self.metadata_storage["1. Identity & Core Properties"]) > 4:
            forensic_dynamic["Revision Count"] = self.metadata_storage["1. Identity & Core Properties"][4][1]
        
        for k, v in forensic_dynamic.items():
            self.tree_meta.insert("", tk.END, values=(c_name, k, v))
            self.metadata_storage[c_name].append((k, v))

        messagebox.showinfo("Ultimate Analysis Sukses", "Seluruh 12 Kluster Data Forensik Selesai Dibongkar!")

    def export_to_pdf(self):
        if not self.metadata_storage:
            messagebox.showwarning("Gagal", "Tidak ada data untuk dicetak. Jalankan Deep Inspection dulu!")
            return
            
        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")], title="Simpan Laporan Forensik")
        if not save_path: return
        
        try:
            doc = SimpleDocTemplate(save_path, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=40, bottomMargin=40)
            story, styles = [], getSampleStyleSheet()
            
            title_style = ParagraphStyle('TitleStyle', fontName='Helvetica-Bold', fontSize=18, textColor=colors.HexColor("#2c3e50"), spaceAfter=5, alignment=1)
            subtitle_style = ParagraphStyle('SubTitleStyle', fontName='Helvetica', fontSize=10, textColor=colors.HexColor("#7f8c8d"), spaceAfter=20, alignment=1)
            h2_style = ParagraphStyle('H2Style', fontName='Helvetica-Bold', fontSize=11, textColor=colors.HexColor("#2980b9"), spaceBefore=14, spaceAfter=6)
            text_style = ParagraphStyle('TextStyle', fontName='Courier', fontSize=8, textColor=colors.HexColor("#2c3e50"))
            header_style = ParagraphStyle('HeaderStyle', fontName='Helvetica-Bold', fontSize=9, textColor=colors.whitesmoke)
            
            story.append(Paragraph("ADVANCED OOXML FORENSIC INVESTIGATION REPORT", title_style))
            story.append(Paragraph(f"Target Directory Hash Reference ID: {os.path.basename(self.app.extract_dir)}", subtitle_style))
            story.append(Spacer(1, 10))
            
            for category, data_list in self.metadata_storage.items():
                if not data_list: continue
                story.append(Paragraph(category.upper(), h2_style))
                
                table_data = [[Paragraph("<b>Kunci Properti Indikator</b>", header_style), Paragraph("<b>Hasil Analisis & Temuan Lapangan</b>", header_style)]]
                for key, val in data_list:
                    table_data.append([Paragraph(f"<b>{key}</b>", text_style), Paragraph(val, text_style)])
                
                t = Table(table_data, colWidths=[180, 370])
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (1, 0), colors.HexColor("#2c3e50")),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                    ('TOPPADDING', (0, 0), (-1, -1), 4),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor("#f8f9fa"), colors.white]),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#bdc3c7")),
                ]))
                story.append(t)
            
            doc.build(story)
            messagebox.showinfo("Sukses", f"Laporan PDF Komprehensif berhasil dicetak ke:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mengekspor PDF: {str(e)}")

class OOXMLInspectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OOXML Inspector & OLE Advanced Forensic Engine")
        self.root.geometry("1450x880")
        self.root.configure(bg="#1e1e24")

        
        # State Variables
        self.extract_dir = ""
        self.current_filepath = ""
        self.selected_rel_path = ""
        self.tree_map = {}
        
        # --- STYLE CONFIGURATION ---
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure(".", background="#1e1e24", foreground="#e0e0e0")
        self.style.configure("TNotebook", background="#1e1e24", borderwidth=0)
        self.style.configure("TNotebook.Tab", background="#2a2a35", foreground="#a0a0a0", padding=[15, 5], font=('Segoe UI', 10, 'bold'))
        self.style.map("TNotebook.Tab", background=[("selected", "#3498db")], foreground=[("selected", "#ffffff")])
        
        # Treeview Styling
        self.style.configure("Treeview", background="#2a2a35", foreground="#ffffff", fieldbackground="#2a2a35", rowheight=24, font=("Segoe UI", 9))
        self.style.map("Treeview", background=[("selected", "#3498db")], foreground=[("selected", "#ffffff")])
        self.style.configure("Treeview.Heading", background="#1e1e24", foreground="#3498db", font=("Segoe UI", 10, "bold"))

        # --- MULTI-TAB NOTEBOOK ROOT ---
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.tab_ooxml = tk.Frame(self.notebook, bg="#1e1e24")
        self.tab_ole = tk.Frame(self.notebook, bg="#1e1e24")
        
        self.notebook.add(self.tab_ooxml, text="  📦 OOXML STRUCTURE INSPECTOR  ")
        self.notebook.add(self.tab_ole, text="  🛡️ OLE ENGINE ANALYSIS (OLETOOLS)  ")
        self.metadata_module = MetadataDeepInspectionModule(self.notebook, self)

        
        # Initialize Sub-UIs
        self.setup_ooxml_ui()
        self.setup_ole_engine_ui()


    def setup_ooxml_ui(self):
        """Membangun antarmuka utama Tab 1: Penjelajah Struktur OOXML."""
        hdr_frame = tk.Frame(self.tab_ooxml, bg="#2a2a35", height=55)
        hdr_frame.pack(fill=tk.X, padx=5, pady=5)
        
        btn_load = tk.Button(
            hdr_frame, text="📁 LOAD BERKAS OOXML", command=self.load_ooxml_file,
            bg="#3498db", fg="#ffffff", font=("Segoe UI", 10, "bold"),
            activebackground="#2980b9", activeforeground="#ffffff", relief=tk.FLAT, padx=15, pady=5
        )
        btn_load.pack(side=tk.LEFT, padx=10, pady=10)
        
        btn_repack = tk.Button(
            hdr_frame, text="⚙️ REPACK ZIP ENGINE", command=self.repack_file,
            bg="#e74c3c", fg="#ffffff", font=("Segoe UI", 10, "bold"),
            activebackground="#c0392b", activeforeground="#ffffff", relief=tk.FLAT, padx=15, pady=5
        )
        btn_repack.pack(side=tk.LEFT, padx=5, pady=10)
        
        self.lbl_status = tk.Label(
            hdr_frame, text="📊 STATUS: Engine Siap. Menunggu berkas...",
            bg="#2a2a35", fg="#2ecc71", font=("Segoe UI", 10, "bold")
        )
        self.lbl_status.pack(side=tk.RIGHT, padx=15)

        main_paned = ttk.PanedWindow(self.tab_ooxml, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        left_paned = ttk.PanedWindow(main_paned, orient=tk.VERTICAL)
        main_paned.add(left_paned, weight=1)
        
        tree_frame = tk.LabelFrame(left_paned, text=" 🗂️ Container Sandbox Treeview ", bg="#1e1e24", fg="#3498db", font=("Consolas", 10, "bold"))
        left_paned.add(tree_frame, weight=3)
        
        self.tree = ttk.Treeview(tree_frame, columns=("Size"), show="tree headings")
        self.tree.heading("Size", text="Ukuran Berkas", anchor=tk.W)
        self.tree.column("Size", width=100, stretch=False)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        
        search_frame = tk.LabelFrame(left_paned, text=" 🔍 Omni Global Discovery Search & Extractor ", bg="#1e1e24", fg="#3498db", font=("Consolas", 10, "bold"))
        left_paned.add(search_frame, weight=2)
        
        search_ctrl = tk.Frame(search_frame, bg="#1e1e24")
        search_ctrl.pack(fill=tk.X, padx=5, pady=5)
        
        self.ent_search = tk.Entry(search_ctrl, bg="#2a2a35", fg="#ffffff", insertbackground="#ffffff", relief=tk.FLAT, font=("Segoe UI", 10))
        self.ent_search.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2, pady=2)
        self.ent_search.bind("<Return>", lambda e: self.execute_omni_global_search())
        
        btn_search = tk.Button(search_ctrl, text="Search", command=self.execute_omni_global_search, bg="#34495e", fg="#ffffff", relief=tk.FLAT)
        btn_search.pack(side=tk.LEFT, padx=2)
        
        btn_ext = tk.Button(search_ctrl, text="Extract External", command=self.execute_external_only_extraction, bg="#9b59b6", fg="#ffffff", relief=tk.FLAT)
        btn_ext.pack(side=tk.LEFT, padx=2)
        
        btn_reset = tk.Button(search_ctrl, text="🔄", command=self.reset_omni_search, bg="#7f8c8d", fg="#ffffff", relief=tk.FLAT)
        btn_reset.pack(side=tk.LEFT, padx=2)
        
        list_scroll_y = tk.Scrollbar(search_frame, orient=tk.VERTICAL)
        list_scroll_x = tk.Scrollbar(search_frame, orient=tk.HORIZONTAL)
        self.lst_results = tk.Listbox(
            search_frame, bg="#111116", fg="#ffffff", selectbackground="#3498db",
            font=("Consolas", 9), relief=tk.FLAT, yscrollcommand=list_scroll_y.set, xscrollcommand=list_scroll_x.set
        )
        list_scroll_y.config(command=self.lst_results.yview)
        list_scroll_x.config(command=self.lst_results.xview)
        
        list_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        list_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.lst_results.pack(fill=tk.BOTH, expand=True, padx=5, pady=2)
        self.lst_results.bind("<<ListboxSelect>>", self.on_search_result_click_sync)
        self.lst_results.insert(tk.END, "📊 STATUS: Engine Siap. Masukkan keyword atau klik 'Extract External'.")

        right_paned = ttk.PanedWindow(main_paned, orient=tk.HORIZONTAL)
        main_paned.add(right_paned, weight=2)
        
        editor_paned = ttk.PanedWindow(right_paned, orient=tk.VERTICAL)
        right_paned.add(editor_paned, weight=1)
        
        xml_frame = tk.LabelFrame(editor_paned, text=" 📝 Source XML Editor (Pretty Print Auto-Format) ", bg="#1e1e24", fg="#3498db", font=("Consolas", 10, "bold"))
        editor_paned.add(xml_frame, weight=3)
        
        self.txt_xml = tk.Text(xml_frame, bg="#111116", fg="#ffffff", insertbackground="#ffffff", font=("Consolas", 10), wrap=tk.NONE)
        self.txt_xml.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.txt_xml.bind("<ButtonRelease-1>", self.on_editor_click_sync)
        
        self.txt_xml.tag_config('xml_tag', foreground='#e74c3c', font=('Consolas', 10, 'bold'))
        self.txt_xml.tag_config('xml_attr', foreground='#f1c40f')
        self.txt_xml.tag_config('xml_val', foreground='#2ecc71')
        self.txt_xml.tag_config('xml_comment', foreground='#7f8c8d', font=('Consolas', 10, 'italic'))
        
        btn_save_xml = tk.Button(xml_frame, text="💾 INJEKSI PERUBAHAN KE SANDBOX", command=self.save_xml_changes, bg="#2ecc71", fg="#ffffff", font=("Segoe UI", 9, "bold"), relief=tk.FLAT)
        btn_save_xml.pack(fill=tk.X, padx=5, pady=2)

        self.txt_xml.config(undo=True, maxundo=-1, autoseparators=True)

        frame_undo_redo = tk.Frame(xml_frame, bg="#1e1e24")
        frame_undo_redo.pack(fill=tk.X, padx=5, pady=2)
        
        # Hubungkan command tombol langsung ke fungsi pengaman baru
        btn_undo = tk.Button(frame_undo_redo, text="↩️ Undo Injeksi", command=self.safe_undo, bg="#2d2d2d", fg="#ffffff", font=("Segoe UI", 9))
        btn_undo.pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        
        btn_redo = tk.Button(frame_undo_redo, text="↪️ Redo Injeksi", command=self.safe_redo, bg="#2d2d2d", fg="#ffffff", font=("Segoe UI", 9))
        btn_redo.pack(side=tk.LEFT, padx=2, expand=True, fill=tk.X)
        
        # Bind shortcut keyboard ke fungsi pengaman baru
        self.txt_xml.bind("<Control-z>", self.safe_undo)
        self.txt_xml.bind("<Control-y>", self.safe_redo)

        
        edu_frame = tk.LabelFrame(editor_paned, text=" 📖 OOXML Interactive Education Map ", bg="#1e1e24", fg="#2ecc71", font=("Consolas", 10, "bold"))
        editor_paned.add(edu_frame, weight=1)

        self.txt_edu = tk.Text(edu_frame, bg="#16161d", fg="#e0e0e0", font=("Segoe UI", 9), wrap=tk.WORD, relief=tk.FLAT)
        self.txt_edu.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.txt_edu.insert("1.0", "📖 Kumpulan Arsitektur Tag yang Terdeteksi:\n(Pilih file XML dan klik sebuah kata/tag di editor untuk melihat deskripsinya.)")

        graph_frame = tk.LabelFrame(right_paned, text=" 📊 Topologi Hubungan Relasional Rels (Top-Down Hierarchy) ", bg="#1e1e24", fg="#3498db", font=("Consolas", 10, "bold"))
        right_paned.add(graph_frame, weight=1)
        
        self.fig, self.ax = plt.subplots(figsize=(5, 5))
        self.fig.patch.set_facecolor("#2a2a35")
        self.ax.set_facecolor("#2a2a35")
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.canvas.mpl_connect('scroll_event', self.json_canvas_zoom)
        
        self.toolbar_frame = tk.Frame(graph_frame, bg="#2a2a35")
        self.toolbar_frame.pack(fill=tk.X, padx=5, pady=2)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.toolbar_frame)
        self.toolbar.update()

    def setup_ole_engine_ui(self):
        """Membangun antarmuka untuk Tab 2: Analisis Forensik Komponen OLE."""
        ole_ctrl_frame = tk.Frame(self.tab_ole, bg="#2a2a35", height=50)
        ole_ctrl_frame.pack(fill=tk.X, padx=5, pady=5)
        
        btn_scan_ole = tk.Button(
            ole_ctrl_frame, text="🚀 JALANKAN OLE & MACRO RAPTOR SCAN", 
            command=self.execute_ole_forensic_scan,
            bg="#2ecc71", fg="#ffffff", font=("Segoe UI", 10, "bold"),
            activebackground="#27ae60", activeforeground="#ffffff",
            relief=tk.FLAT, padx=15, pady=5
        )
        btn_scan_ole.pack(side=tk.LEFT, padx=10, pady=5)
        
        lbl_info = tk.Label(
            ole_ctrl_frame, 
            text="💡 Scanner menggunakan Hybrid Engine (Internal Library & Global CLI Subprocess Fallback).",
            bg="#2a2a35", fg="#a0a0a0", font=("Segoe UI", 9, "italic")
        )
        lbl_info.pack(side=tk.LEFT, padx=10)

        ole_paned = ttk.PanedWindow(self.tab_ole, orient=tk.HORIZONTAL)
        ole_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        frame_left = tk.LabelFrame(ole_paned, text=" [1] Macro Raptor (mraptor) - Heuristic Verdict ", bg="#1e1e24", fg="#3498db", font=("Consolas", 10, "bold"))
        ole_paned.add(frame_left, weight=1)
        
        self.txt_mraptor = tk.Text(frame_left, bg="#111116", fg="#2ecc71", font=("Consolas", 10), wrap=tk.WORD, relief=tk.FLAT)
        self.txt_mraptor.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        frame_right = tk.LabelFrame(ole_paned, text=" [2] OLE Object Scanner (oleobj) - Embedded Links & Relationships ", bg="#1e1e24", fg="#3498db", font=("Consolas", 10, "bold"))
        ole_paned.add(frame_right, weight=1)
        
        self.txt_oleobj = tk.Text(frame_right, bg="#111116", fg="#e67e22", font=("Consolas", 10), wrap=tk.WORD, relief=tk.FLAT)
        self.txt_oleobj.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def safe_undo(self, event=None):
        """Mengeksekusi undo dengan aman tanpa memicu crash jika stack kosong."""
        try:
            self.txt_xml.edit_undo()
        except tk.TclError:
            pass
        return "break" # Menghentikan event ganda bawaan Tkinter

    def safe_redo(self, event=None):
        """Mengeksekusi redo dengan aman tanpa memicu crash jika stack kosong."""
        try:
            self.txt_xml.edit_redo()
        except tk.TclError:
            pass
        return "break" # Menghentikan event ganda bawaan Tkinter

    def trigger_undo(self):
        """Mengembalikan teks editor ke kondisi sebelum injeksi/perubahan dilakukan."""
        try:
            self.txt_sandbox.edit_undo()
        except tk.TclError:
            # Error ditangkap jika stack undo sudah kosong (tidak ada riwayat lagi)
            pass

    def trigger_redo(self):
        """Memulihkan kembali teks yang sempat dibatalkan oleh fungsi undo."""
        try:
            self.txt_sandbox.edit_redo()
        except tk.TclError:
            # Error ditangkap jika stack redo sudah kosong
            pass

    def defang_url(self, url):
        """Mengubah http://attacker.com menjadi hxxp[://]attacker[.]com untuk keamanan analisis."""
        if not url:
            return url
        # Ubah http/https menjadi hxxp/hxxps
        defanged = url.replace("http://", "hxxp://").replace("https://", "hxxps://")
        # Berikan bracket pada token :// dan titik pertama setelah domain
        defanged = defanged.replace("://", "[://]")
        # Defang titik pada domain (menghindari pengetikan IP/Domain utuh)
        defanged = re.sub(r'(?<=\w)\.(?=\w)', '[.]', defanged, count=2)
        return defanged

    # --- CORE FILE LOADING ENGINE ---
    def load_ooxml_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Office Open XML Documents", "*.docx;*.xlsx;*.pptx;*.docm;*.xlsm;*.pptm"), ("All Files", "*.*")]
        )
        if not file_path:
            return
            
        self.current_filepath = file_path
        if self.extract_dir and os.path.exists(self.extract_dir):
            shutil.rmtree(self.extract_dir)
            
        self.extract_dir = os.path.join(os.path.dirname(file_path), f"_sandbox_{os.path.basename(file_path)}")
        
        try:
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(self.extract_dir)
                
            self.lbl_status.config(text=f"📂 Loaded: {os.path.basename(file_path)}")
            self.build_tree_structure()
            self.generate_relationship_graph()
            
            self.lst_results.delete(0, tk.END)
            self.lst_results.insert(tk.END, "✅ Sandbox terekstrak secara utuh. Engine Siap menganalisis.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mengekstrak arsip OOXML: {str(e)}")

    def build_tree_structure(self):
        self.tree.delete(*self.tree.get_children())
        self.tree_map.clear()
        
        if not self.extract_dir or not os.path.exists(self.extract_dir):
            return
            
        root_node = self.tree.insert("", tk.END, text=os.path.basename(self.current_filepath), open=True)
        
        def process_dir(current_path, parent_node):
            try:
                for entry in sorted(os.scandir(current_path), key=lambda e: (e.is_file(), e.name)):
                    rel_path = os.path.relpath(entry.path, self.extract_dir).replace("\\", "/")
                    if entry.is_dir():
                        sub_node = self.tree.insert(parent_node, tk.END, text=f"📁 {entry.name}", open=False, tags=(rel_path,))
                        self.tree_map[rel_path] = sub_node
                        process_dir(entry.path, sub_node)
                    else:
                        size_bytes = entry.stat().st_size
                        size_str = f"{size_bytes} B" if size_bytes < 1024 else f"{size_bytes/1024:.1f} KB"
                        file_node = self.tree.insert(parent_node, tk.END, text=f"📄 {entry.name}", values=(size_str,), tags=(rel_path,))
                        self.tree_map[rel_path] = file_node
            except Exception:
                pass
                
        process_dir(self.extract_dir, root_node)

    # --- OMNI GLOBAL DISCOVERY SEARCH ---
    def execute_omni_global_search(self):
        keyword = self.ent_search.get().strip()
        self.lst_results.delete(0, tk.END)
        
        if not self.extract_dir:
            self.lst_results.insert(tk.END, "❌ ERROR: Load berkas dokumen OOXML terlebih dahulu.")
            return
        if not keyword:
            self.lst_results.insert(tk.END, "💡 Tips: Masukkan kata kunci pencarian.")
            return
            
        search_keyword_lower = keyword.lower()
        match_count = 0
        
        for root_dir, _, files in os.walk(self.extract_dir):
            for file in files:
                if file.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bin')):
                    continue
                full_filepath = os.path.join(root_dir, file)
                rel_filepath = os.path.relpath(full_filepath, self.extract_dir).replace("\\", "/")
                
                try:
                    with open(full_filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                    for line_num, line_content in enumerate(lines, 1):
                        if search_keyword_lower in line_content.lower():
                            match_count += 1
                            clean_line = line_content.strip()
                            if len(clean_line) > 110:
                                clean_line = clean_line[:110] + "..."
                            self.lst_results.insert(tk.END, f"[{rel_filepath} | L:{line_num}] -> {clean_line}")
                except Exception:
                    pass
        if match_count == 0:
            self.lst_results.insert(tk.END, f"❌ Kata kunci '{keyword}' tidak ditemukan.")

    # --- AUTOMATED EXTERNAL ONLY EXTRACTOR ---
    def execute_external_only_extraction(self):
        self.lst_results.delete(0, tk.END)
        if not self.extract_dir:
            self.lst_results.insert(tk.END, "❌ ERROR: Load berkas dokumen OOXML terlebih dahulu.")
            return

        self.lst_results.insert(tk.END, "🔍 MENGEKSTRAKSI & DEFANGING SEMUA ENTITAS EXTERNAL LINK...")
        self.lst_results.insert(tk.END, "--------------------------------------------------------------------------------------------------------------------------------")
        
        url_pattern = re.compile(r'https?://[^\s\'"]+')
        external_count = 0
        
        for root_dir, _, files in os.walk(self.extract_dir):
            for file in files:
                if file.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bin')):
                    continue
                full_filepath = os.path.join(root_dir, file)
                rel_filepath = os.path.relpath(full_filepath, self.extract_dir).replace("\\", "/")
                
                try:
                    with open(full_filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                        
                    for line_num, line_content in enumerate(lines, 1):
                        matches = url_pattern.findall(line_content)
                        for match in matches:
                            clean_url = match.split('"')[0].split("'")[0].split('>')[0].strip()
                            if "schemas.openxmlformats.org" in clean_url or "schemas.microsoft.com" in clean_url:
                                continue
                                
                            external_count += 1
                            # LOGIKA PERBAIKAN: Terapkan Defang URL sebelum tampil di UI
                            defanged_url = self.defang_url(clean_url)
                            
                            # Edukasi Taktis FakeNet-NG jika mendeteksi link mencurigakan
                            if "canary" in clean_url.lower() or "token" in clean_url.lower():
                                defanged_url += "  ⚠️ [POTENSI CANARYTOKEN - Gunakan FakeNet-NG untuk mencedat!]"
                                
                            self.lst_results.insert(tk.END, f"[{rel_filepath} | L:{line_num}] -> {defanged_url}")
                except Exception:
                    pass
                    
        if self.lst_results.size() > 0:
            self.lst_results.delete(0, 1)
            
        if external_count == 0:
            self.lst_results.insert(tk.END, "❌ Tidak ditemukan link atau skema eksternal di luar manifest standar Microsoft.")
        else:
            self.lst_results.insert(0, f"✅ BERHASIL MENEMUKAN {external_count} ENTITAS EKSTERNAL (DEFANGED):")
            self.lst_results.insert(1, "💡 INFO: Tautan berbahaya telah diubah ke format hxxp[://] untuk mencegah 'accidental click'.")
            self.lst_results.insert(2, "💡 TIP FORENSIK: Jalankan FakeNet-NG di lab isolasi untuk menangkap paket data mentah tanpa membocorkan info host kamu.")
            self.lst_results.insert(3, "--------------------------------------------------------------------------------------------------------------------------------")

    def on_search_result_click_sync(self, event):
        selected_idx = self.lst_results.curselection()
        if not selected_idx:
            return
            
        selected_text = self.lst_results.get(selected_idx[0])
        if " -> " not in selected_text:
            return
            
        try:
            parts = selected_text.split(' | ')
            if len(parts) < 2:
                return
            target_rel_path = parts[0].replace('[', '').strip()
            
            line_part = parts[1].split(']')
            line_number = 1
            if len(line_part) > 0:
                line_number = int(line_part[0].replace('L:', '').strip())

            target_rel_path = target_rel_path.replace("\\", "/")

            if target_rel_path in self.tree_map:
                node_to_select = self.tree_map[target_rel_path]
                self.tree.see(node_to_select)         
                self.tree.selection_set(node_to_select) 
                
                self.on_tree_select(None)
                
                self.txt_xml.mark_set("insert", f"{line_number}.0")
                self.txt_xml.see(f"{line_number}.0")
                self.txt_xml.tag_add("sel", f"{line_number}.0", f"{line_number}.end")
                self.txt_xml.focus_set()
        except Exception:
            pass

    def reset_omni_search(self):
        self.ent_search.delete(0, tk.END)
        self.lst_results.delete(0, tk.END)
        self.lst_results.insert(tk.END, "📊 STATUS: Engine Siap. Masukkan keyword atau klik 'Extract External'.")

    # --- XML SELECTION & AUTO PRETTY PRINT (WITH MEMORY GUARD) ---
    def on_tree_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
            
        tags = self.tree.item(selected[0], "tags")
        if not tags:
            return
            
        rel_path = tags[0]
        self.selected_rel_path = rel_path
        full_path = os.path.join(self.extract_dir, rel_path)
        
        if os.path.isfile(full_path):
            file_size = os.path.getsize(full_path)
            
            # SAKLAR MEMORY GUARD: Batasi file raksasa (Contoh: > 10 MB) agar GUI tidak freeze/crash
            MAX_PREVIEW_SIZE = 10 * 1024 * 1024  # 10 Megabytes
            
            if file_size > MAX_PREVIEW_SIZE:
                self.txt_xml.delete("1.0", tk.END)
                self.txt_xml.insert("1.0", f"⚠️ MEMORY GUARD NOTICE:\n"
                                           f"Berkas terlalu besar untuk dimuat di editor visual.\n"
                                           f"Path: {rel_path}\n"
                                           f"Ukuran: {file_size / (1024*1024):.2f} MB\n"
                                           f"Saran: Gunakan external terminal (Hex Editor/Strings) untuk menganalisis berkas ini.")
                self.txt_edu.delete("1.0", tk.END)
                self.txt_edu.insert("1.0", "ℹ️ Analisis dilewati demi menjaga stabilitas memori aplikasi.")
                return

            if rel_path.endswith(('.xml', '.rels', '.txt', '.pml', '.sigs')):
                try:
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        raw_content = f.read()
                    
                    # Logika Parsing, Mitigasi XXE, dan Pretty Print
                    try:
                        secure_parser = LET.XMLParser(
                            resolve_entities=False,  
                            no_network=True,         
                            remove_blank_text=True   
                        )
                        secure_root = LET.fromstring(raw_content.encode('utf-8'), parser=secure_parser)
                        
                        formatted_xml = LET.tostring(
                            secure_root, 
                            xml_declaration=True, 
                            encoding='utf-8', 
                            pretty_print=True
                        ).decode('utf-8')
                    except Exception:
                        formatted_xml = raw_content
                    
                    # Tampilkan ke Editor XML
                    self.txt_xml.delete("1.0", tk.END)
                    self.txt_xml.insert("1.0", formatted_xml)
                    
                    # Jalankan fungsi pasca-load bawaan
                    self.apply_xml_highlighting()
                    self.analyze_xml_education_summary(formatted_xml)
                    
                except Exception as e:
                    self.txt_xml.delete("1.0", tk.END)
                    self.txt_xml.insert("1.0", f"Error membaca konten file: {str(e)}")
            else:
                self.txt_xml.delete("1.0", tk.END)
                self.txt_xml.insert("1.0", f"[Biner / Dokumen Gambar Non-XML]\nPath: {rel_path}\nUkuran: {file_size} Bytes")
                self.txt_edu.delete("1.0", tk.END)
                self.txt_edu.insert("1.0", "ℹ️ File biner terdeteksi. Pembedahan komponen edukasi dilewati.")

    def apply_xml_highlighting(self):
        content = self.txt_xml.get("1.0", tk.END)
        for tag_name in ['xml_tag', 'xml_attr', 'xml_val', 'xml_comment']:
            self.txt_xml.tag_remove(tag_name, "1.0", tk.END)
            
        xml_regex = re.compile(
            r'(?P<comment>)|(?P<tag></?[\w:]+(?=\s|>|/>))|(?P<attr>[\w:]+(?=\s*=))|(?P<val>"[^"]*"|\'[^\']*\')',
            re.DOTALL
        )
        
        for match in xml_regex.finditer(content):
            kind = match.lastgroup
            start_idx = f"1.0 + {match.start()} chars"
            end_idx = f"1.0 + {match.end()} chars"
            
            if kind == 'comment':
                self.txt_xml.tag_add('xml_comment', start_idx, end_idx)
            elif kind == 'tag':
                self.txt_xml.tag_add('xml_tag', start_idx, end_idx)
            elif kind == 'attr':
                self.txt_xml.tag_add('xml_attr', start_idx, end_idx)
            elif kind == 'val':
                self.txt_xml.tag_add('xml_val', start_idx, end_idx)

    def on_editor_click_sync(self, event):
        try:
            cursor_index = self.txt_xml.index(tk.CURRENT)
            line, col = map(int, cursor_index.split('.'))
            line_content = self.txt_xml.get(f"{line}.0", f"{line}.end")
            words = re.findall(r'[\w:]+', line_content)
            clicked_word = ""
            
            accumulated = 0
            for w in words:
                idx = line_content.find(w, accumulated)
                if idx <= col <= (idx + len(w)):
                    clicked_word = w
                    break
                accumulated = idx + len(w)
            
            clean_tag = clicked_word.split(':')[-1] if ':' in clicked_word else clicked_word
            if clean_tag in XML_EDUCATION_MAP:
                self.txt_edu.delete("1.0", tk.END)
                self.txt_edu.insert("1.0", f"🎯 INTERACTIVE TARGET FOUND:\n\nTag Name  : <{clicked_word}>\nDeskripsi : {XML_EDUCATION_MAP[clean_tag]}")
        except Exception:
            pass

    def analyze_xml_education_summary(self, content):
        self.txt_edu.delete("1.0", tk.END)
        self.txt_edu.insert("1.0", "📖 Kumpulan Arsitektur Tag yang Terdeteksi di File Ini:\n(Klik pada tag internal teks editor untuk memicu pembedahan spesifik)\n\n")
        found_tags = set(re.findall(r'</?[\w:]+:([\w]+)', content))
        
        for tag in sorted(found_tags):
            if tag in XML_EDUCATION_MAP:
                self.txt_edu.insert(tk.END, f" • <{tag}> \u2192 {XML_EDUCATION_MAP[tag][:70]}...\n")

    def get_graph_pos(self, G):
        pos = {}
        levels = {}
        
        for node, data in G.nodes(data=True):
            lvl = data.get('level', 0)
            if lvl not in levels:
                levels[lvl] = []
            levels[lvl].append(node)
        
        for lvl, nodes in levels.items():
            y = -lvl  
            width = len(nodes)
            for i, node in enumerate(sorted(nodes)):  
                x = (i - (width - 1) / 2) * 2.5  
                pos[node] = (x, y)
                
        return pos

    def generate_relationship_graph(self):
        self.ax.clear()
        G = nx.DiGraph()
        
        if not self.extract_dir or not os.path.exists(self.extract_dir):
            self.render_empty_graph_message()
            return

        root_node = "[Root Package]"
        G.add_node(root_node, level=0)

        for root_dir, _, files in os.walk(self.extract_dir):
            for file in files:
                if file.endswith('.rels'):
                    full_path = os.path.join(root_dir, file)
                    rel_path_from_sandbox = os.path.relpath(full_path, self.extract_dir).replace("\\", "/")
                    
                    if rel_path_from_sandbox == "_rels/.rels":
                        parent_src = root_node
                    else:
                        parent_src = rel_path_from_sandbox.replace("/_rels/", "/").rsplit('.rels', 1)[0]
                    
                    try:
                        tree = ET.parse(full_path)
                        root = tree.getroot()
                        ns = {'rel': 'http://schemas.openxmlformats.org/package/2006/relationships'}
                        base_dir = "" if rel_path_from_sandbox == "_rels/.rels" else rel_path_from_sandbox.split('/_rels/')[0]

                        for rel in root.findall('.//rel:Relationship', ns):
                            raw_target = rel.get('Target', '')
                            if not raw_target:
                                continue
                                
                            if raw_target.startswith('../'):
                                parts = base_dir.split('/') if base_dir else []
                                t_parts = raw_target.split('/')
                                while t_parts and t_parts[0] == '..':
                                    if parts: parts.pop()
                                    t_parts.pop(0)
                                target_file = "/".join(parts + t_parts) if parts else "/".join(t_parts)
                            else:
                                target_file = f"{base_dir}/{raw_target}" if base_dir else raw_target
                            
                            target_file = target_file.replace("\\", "/").strip("/")

                            if parent_src not in G:
                                G.add_node(parent_src, level=1)
                            
                            parent_level = G.nodes[parent_src].get('level', 0)
                            child_level = parent_level + 1
                            
                            if target_file not in G:
                                G.add_node(target_file, level=child_level)
                            G.add_edge(parent_src, target_file)
                                
                    except Exception:
                        pass
                        
        if len(G) <= 1:  
            self.render_empty_graph_message()
            return

        pos = self.get_graph_pos(G)
        node_colors = [GRAPH_LEVEL_COLORS.get(G.nodes[n].get('level', 0), "#CCCCCC") for n in G.nodes()]
        
        nx.draw_networkx_nodes(G, pos, ax=self.ax, node_color=node_colors, node_size=1000, alpha=0.95, edgecolors="#ffffff", linewidths=1)
        nx.draw_networkx_edges(G, pos, ax=self.ax, edgelist=G.edges(), edge_color='#7F8C8D', width=1.5, arrows=True, arrowsize=14, connectionstyle="arc3,rad=0.05")
        
        labels = {node: (node.split('/')[-1] if '/' in node else node) for node in G.nodes()}
        nx.draw_networkx_labels(G, pos, labels, font_size=7, font_color='#ffffff', font_family='Consolas', font_weight='bold', ax=self.ax)
        
        all_y = [coords[1] for coords in pos.values()]
        min_y, max_y = min(all_y), max(all_y)
        self.ax.set_ylim(min_y - 0.8, max_y + 0.8)
        
        all_x = [coords[0] for coords in pos.values()]
        if all_x:
            min_x, max_x = min(all_x), max(all_x)
            self.ax.set_xlim(min_x - 1.5, max_x + 1.5)

        self.ax.axis('off')
        self.fig.tight_layout()
        self.canvas.draw()

    def render_empty_graph_message(self):
        self.ax.clear()
        self.ax.text(0.5, 0.5, "📭 Tidak ditemukan relasi .rels yang valid untuk divisualisasikan.\n\nPastikan dokumen memiliki struktur relasi yang benar.", 
                     horizontalalignment='center', verticalalignment='center', fontsize=10, color="#e0e0e0", fontfamily='Segoe UI', transform=self.ax.transAxes)
        self.ax.set_facecolor("#2a2a35")
        self.ax.axis('off')
        self.canvas.draw()

    # --- CRUD MODIFICATION INJECTION ---
    def save_xml_changes(self):
        if not self.selected_rel_path:
            messagebox.showwarning("Injeksi Ditolak", "Pilih file target pada struktur pohon internal terlebih dahulu.")
            return
            
        full_path = os.path.join(self.extract_dir, self.selected_rel_path)
        modified_content = self.txt_xml.get("1.0", tk.END).strip()
        
        # LOGIKA PERBAIKAN: lxml parser dengan proteksi XXE (resolve_entities=False, no_network=True)
        secure_parser = LET.XMLParser(resolve_entities=False, no_network=True)
        try:
            LET.fromstring(modified_content.encode('utf-8'), parser=secure_parser)
        except LET.XMLSyntaxError as e:
            if not messagebox.askyesno("XML Broken Warning", f"Struktur XML tidak valid/cacat:\n{str(e)}\n\nTetap paksa tulis data?"):
                return
                
        try:
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(modified_content)
            messagebox.showinfo("Success", f"Data berhasil dimodifikasi di sandbox:\n{self.selected_rel_path}")
            
            size_bytes = os.path.getsize(full_path)
            size_str = f"{size_bytes} B" if size_bytes < 1024 else f"{size_bytes/1024:.1f} KB"
            selected_items = self.tree.selection()
            if selected_items:
                self.tree.item(selected_items[0], values=(size_str,))
            self.generate_relationship_graph()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menulis perubahan: {str(e)}")

    # --- REPACK ENGINE ---
    def repack_file(self):
        if not self.current_filepath or not self.extract_dir:
            messagebox.showwarning("Proses Batal", "Belum ada objek manipulasi di sandbox.")
            return
            
        save_path = filedialog.asksaveasfilename(
            defaultextension=os.path.splitext(self.current_filepath)[1],
            filetypes=[("OOXML Binaries", f"*{os.path.splitext(self.current_filepath)[1]}")],
            initialfile=f"engineered_{os.path.basename(self.current_filepath)}"
        )
        
        if not save_path:
            return
            
        try:
            with zipfile.ZipFile(save_path, 'w', zipfile.ZIP_DEFLATED) as zip_out:
                for root_dir, _, files in os.walk(self.extract_dir):
                    for file in files:
                        full_filepath = os.path.join(root_dir, file)
                        rel_filepath = os.path.relpath(full_filepath, self.extract_dir)
                        zip_out.write(full_filepath, rel_filepath)
                        
            messagebox.showinfo("Repack Complete", f"Binari berhasil dirakit ulang!\n\nLokasi: {save_path}")
            self.lbl_status.config(text=f"⚙️ Repacked to: {os.path.basename(save_path)}")
        except Exception as e:
            messagebox.showerror("Repack Error", f"Gagal kompilasi berkas zip: {str(e)}")

    # --- ADVANCED HYBRID SCANNING ENGINE (WITH CLI FALLBACK) ---
    def execute_ole_forensic_scan(self):
        """Menjalankan scanner dengan metode hibrida: Import lokal, Call CLI Global, dan Custom XML Tracker."""
        self.txt_mraptor.delete("1.0", tk.END)
        self.txt_oleobj.delete("1.0", tk.END)
        
        if not self.extract_dir or not os.path.exists(self.extract_dir):
            messagebox.showwarning("Scan Batal", "Muat berkas dokumen OOXML di Tab pertama terlebih dahulu.")
            return
            
        self.txt_mraptor.insert(tk.END, "⚙️ Menginisialisasi Heuristic Engine Macro Raptor...\n")
        self.txt_oleobj.insert(tk.END, "⚙️ Memindai komponen internal OLE Embedded via Subprocess Fallback...\n")
        
        target_files = []
        for root_dir, _, files in os.walk(self.extract_dir):
            for file in files:
                if file.endswith(('.bin', '.vba', '.vbe', '.ole')) or 'embeddings' in root_dir.lower():
                    target_files.append(os.path.join(root_dir, file))
                    
        if self.current_filepath and os.path.exists(self.current_filepath):
            target_files.append(self.current_filepath)

        # LOGIKA PERBAIKAN: Jalankan Custom Threat Intelligence Parser Terlebih Dahulu
        self.txt_oleobj.insert(tk.END, "🔍 Melakukan Deep XML Scanning untuk melacak hidden Canarytokens...\n")
        xml_threat_report = self._scan_internal_xml_for_canary()
        self.txt_oleobj.insert(tk.END, xml_threat_report)
        self.txt_oleobj.insert(tk.END, "================================================================================\n\n")
            
        if not target_files:
            self.txt_mraptor.insert(tk.END, "✔️ Tidak ditemukan kontainer biner OLE di dalam dokumen.")
            return

        global_python_path = r"C:\Users\Dell 3410\AppData\Local\Programs\Python\Python313\python.exe"
        self.txt_mraptor.insert(tk.END, f"📊 Memindai {len(target_files)} target biner menggunakan Global Engine via CLI...\n\n")
        
        for filepath in target_files:
            rel_name = os.path.relpath(filepath, self.extract_dir) if self.extract_dir in filepath else os.path.basename(filepath)
            
            # Eksekusi mraptor melalui python global CLI
            try:
                self.txt_mraptor.insert(tk.END, f"📄 File: {rel_name}\n")
                cmd_mraptor = [global_python_path, "-m", "oletools.mraptor", filepath]
                res_mr = subprocess.run(cmd_mraptor, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                
                if res_mr.stdout:
                    self.txt_mraptor.insert(tk.END, res_mr.stdout)
                else:
                    self.txt_mraptor.insert(tk.END, f"   [INFO] Tidak ada data keluaran makro atau file kosong.\n")
                self.txt_mraptor.insert(tk.END, "-"*80 + "\n")
            except Exception as e:
                self.txt_mraptor.insert(tk.END, f"⚠️ Gagal memanggil CLI mraptor: {str(e)}\n")

            # Eksekusi oleobj melalui python global CLI
            try:
                self.txt_oleobj.insert(tk.END, f"📁 Analisis Berkas OLE: {rel_name}\n")
                cmd_oleobj = [global_python_path, "-m", "oletools.oleobj", filepath]
                res_obj = subprocess.run(cmd_oleobj, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
                
                if res_obj.stdout:
                    clean_stdout = re.sub(r'oleobj \d+\.\d+\.\d+.*?\n', '', res_obj.stdout)
                    self.txt_oleobj.insert(tk.END, clean_stdout)
                else:
                    self.txt_oleobj.insert(tk.END, "   ✔️ Tidak ditemukan relasi link biner eksternal terselubung.\n")
                self.txt_oleobj.insert(tk.END, "-"*80 + "\n")
            except Exception as e:
                self.txt_oleobj.insert(tk.END, f"⚠️ Gagal memanggil CLI oleobj: {str(e)}\n")


    

    def _scan_internal_xml_for_canary(self):
        """Engine tambahan untuk mendeteksi token pelacak yang bersembunyi di struktur XML teks (Footer/Header)."""
        canary_verdict = ""
        url_pattern = re.compile(r'https?://[^\s\'"]+')
        found_tokens = 0
        
        for root_dir, _, files in os.walk(self.extract_dir):
            for file in files:
                if file.endswith(('.xml', '.rels')):
                    full_filepath = os.path.join(root_dir, file)
                    rel_filepath = os.path.relpath(full_filepath, self.extract_dir).replace("\\", "/")
                    
                    try:
                        with open(full_filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            
                        matches = url_pattern.findall(content)
                        for match in matches:
                            clean_url = match.split('"')[0].split("'")[0].split('>')[0].strip()
                            # Filter skema standar Microsoft
                            if "schemas.openxmlformats.org" in clean_url or "schemas.microsoft.com" in clean_url:
                                continue
                                
                            if "canary" in clean_url.lower() or "token" in clean_url.lower() or "submit.aspx" in clean_url.lower():
                                found_tokens += 1
                                canary_verdict += f"🔥 [ALERT DETECTED] -> {clean_url}\n"
                                canary_verdict += f"   └── Kontainer: {rel_filepath}\n"
                                canary_verdict += f"   └── Taktik Analisis: Jalankan FakeNet-NG untuk mengisolasi request ini!\n\n"
                    except Exception:
                        pass
                        
        if found_tokens > 0:
            header = f"🚨 THREAT INTELLIGENCE REPORT: TERDETEKSI {found_tokens} CANARYTOKEN / WEB TRACKER!\n"
            header += "================================================================================\n"
            return header + canary_verdict
        return "✔️ Internal XML Threat Scan: Tidak ditemukan hidden web tracker di komponen teks XML.\n"

    def json_canvas_zoom(self, event):
        if event.inaxes is None:
            return
            
        if event.key == 'control':
            ax = event.inaxes
            xmin, xmax = ax.get_xlim()
            ymin, ymax = ax.get_ylim()
            
            x_range = xmax - xmin
            y_range = ymax - ymin
            zoom_factor = 0.15
            
            if event.button == 'up':
                new_xmin = xmin + x_range * zoom_factor
                new_xmax = xmax - x_range * zoom_factor
                new_ymin = ymin + y_range * zoom_factor
                new_ymax = ymax - y_range * zoom_factor
            elif event.button == 'down':
                new_xmin = xmin - x_range * zoom_factor
                new_xmax = xmax + x_range * zoom_factor
                new_ymin = ymin - y_range * zoom_factor
                new_ymax = ymax - y_range * zoom_factor
            else:
                return

            ax.set_xlim(new_xmin, new_xmax)
            ax.set_ylim(new_ymin, new_ymax)
            self.canvas.draw_idle()

    def __del__(self):
        if hasattr(self, 'extract_dir') and self.extract_dir and os.path.exists(self.extract_dir):
            try:
                shutil.rmtree(self.extract_dir)
            except Exception:
                pass

if __name__ == "__main__":
    root = tk.Tk()
    app = OOXMLInspectorApp(root)
    root.mainloop()