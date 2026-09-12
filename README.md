# Sistem Informasi Akuntansi & Transparansi Keuangan (SIA)
### BUMDes Karya Raharja — Desa Wonoharjo, Kecamatan Pangandaran

Aplikasi sistem informasi akuntansi dan dasbor transparansi publik berskala *full-stack* yang dirancang khusus untuk digitalisasi tata kelola keuangan pada Badan Usaha Milik Desa (BUMDes) Karya Raharja, Desa Wonoharjo, Kabupaten Pangandaran. Aplikasi ini menggunakan arsitektur terpisah (*decoupled architecture*) untuk memisahkan layanan backend dan antarmuka frontend secara independen.

SIA BUMDes Karya Raharja adalah wujud nyata komitmen BUMDes Karya Raharja Desa Wonoharjo dalam menerapkan tata kelola keuangan yang transparan, akuntabel, dan profesional dengan berpedoman pada **Kepmendesa PDTT No. 136 Tahun 2022**. Data yang ditampilkan di dalam sistem ini adalah data yang diperoleh secara *real-time* dari hasil pencatatan transaksi aktivitas usaha BUMDes. 

Kehadiran platform ini memastikan setiap rupiah pendapatan dioptimalkan untuk meminimalkan beban, memaksimalkan laba bersih, dan memperbesar kontribusi Pendapatan Asli Desa (PADes) demi pembangunan desa yang berkelanjutan.

---

## 🏢 Daftar Unit Usaha BUMDes

Sistem ini dirancang untuk mengkonsolidasikan data keuangan dari 6 unit usaha aktif yang dikelola oleh BUMDes Karya Raharja:
*   **UU01:** Pembibitan Domba Garut
*   **UU02:** Peternakan Ikan Air Tawar Sistem Bioflok
*   **UU03:** Sewa Kendaraan Angkutan Barang
*   **UU04:** Perdagangan dan Produksi Barang Jadi
*   **UU05:** Toko Offline BUMDes
*   **UU06:** Toko Online BUMDes via Marketplace

---

## ⚖️ Landasan Hukum & Standar Akuntansi

Sistem ini dirancang, dibangun, dan disesuaikan seluruh komponen outputnya dengan berpedoman pada **Keputusan Menteri Desa, Pembangunan Daerah Tertinggal, dan Transmigrasi (Kepmendesa PDTT) Nomor 136 Tahun 2022** tentang Panduan Penyusunan Laporan Keuangan Badan Usaha Milik Desa. 

Dengan mematuhi regulasi ini, sistem secara otomatis menghasilkan format laporan keuangan yang valid untuk keperluan sidang pertanggungjawaban BUMDes, meliputi:
*   Laporan Posisi Keuangan (Neraca)
*   Laporan Laba Rugi
*   Laporan Perubahan Ekuitas
*   Laporan Arus Kas
*   Catatan atas Laporan Keuangan (CALK)

---

## 📂 Struktur Repositori

```text
├── backend/      # Layanan API berbasis FastAPI, pemrosesan data, & dokumen laporan keuangan
└── frontend/     # Single-Page Application (SPA) berbasis React untuk dasbor & visualisasi data
```

---

## 👥 Manajemen Hak Akses Pengguna (User Roles)

Aplikasi ini menerapkan *Role-Based Access Control* (RBAC) untuk menjaga keamanan dan akuntabilitas data keuangan berdasarkan struktur organisasi BUMDes:

1.  **Admin:** Mengelola data pengguna (tambah/hapus akun staff), konfigurasi sistem, dan pemeliharaan basis data.
2.  **Direktur:** Memantau dasbor performa bisnis makro dari seluruh unit usaha (UU01 - UU06), menyetujui anggaran belanja besar, dan mengunduh laporan keuangan konsolidasi akhir.
3.  **Bendahara:** Memiliki hak penuh untuk mencatat transaksi kas masuk/keluar, memvalidasi setoran omset dari unit usaha, mengunggah bukti kuitansi fisik, menyusun jurnal, dan mengelola arus kas utama BUMDes.
4.  **Pengelola Unit Usaha:** Menginput data transaksi harian, omset harian, dan mengunggah nota pengeluaran operasional khusus untuk kode unit usaha yang dipimpinnya (misal: pengelola UU01 hanya bisa menginput transaksi Pembibitan Domba Garut).
5.  **Penasihat (Kepala Desa):** Memiliki hak akses peninjauan (*read-only*) terhadap seluruh performa keuangan lintas unit usaha dan grafik transparansi sebagai bentuk pengawasan reguler pemerintahan desa.
6.  **Pengawas:** Memantau laporan neraca, arus kas, dan memeriksa kesesuaian antara catatan akuntansi dengan bukti fisik transaksi yang diunggah dari tiap unit usaha.
7.  **Auditor:** Memiliki hak akses khusus untuk mengunduh seluruh data mentah transaksi (format Excel via OpenPyXL) dan dokumen laporan resmi (format PDF via ReportLab) guna keperluan audit tahunan sesuai standar Kepmendesa.

---

## 🔄 Alur Kerja Sistem (System Workflow)

```text
[Unit Usaha / Bendahara]             [Sistem / Pandas]             [Semua Stakeholder]
   Input Transaksi       ───>    Proses Jurnal & Neraca    ───>   Visualisasi Dasbor 
   & Bukti Fisik                 Secara Otomatis                 & Unduh Laporan PDF/Excel
```

1.  **Pencatatan Data:** Pengelola Unit Usaha atau Bendahara memasukkan data transaksi (nominal, tanggal, kategori, dan kode unit usaha UU01-UU06) serta mengunggah dokumen fisik pendukung via formulir React.
2.  **Validasi & Otorisasi:** Sistem memverifikasi hak akses pengguna. Transaksi dari unit usaha akan diverifikasi oleh Bendahara sebelum masuk ke Buku Besar konsolidasi utama.
3.  **Pemrosesan Otomatis:** *Backend* (FastAPI + Pandas) secara otomatis memproses jurnal umum, memposting ke buku besar, menghitung neraca saldo, hingga menghasilkan data siap saji untuk laporan laba rugi per unit usaha maupun konsolidasi.
4.  **Diseminasi Informasi:** Data hasil kalkulasi ditampilkan dalam bentuk grafik interaktif di *frontend* (React + Recharts) untuk transparansi, serta siap diekspor menjadi dokumen cetak oleh Auditor atau Direktur.

---

## 🖼️ Alur Penyimpanan Bukti Transaksi

Untuk menghemat kapasitas penyimpanan server lokal, sistem memanfaatkan integrasi *Cloud Storage* berbasis Google Drive untuk mengelola berkas nota, kuitansi, atau *invoice*:

```text
[Frontend React] ──(Upload Foto Nota)──> [Backend FastAPI] ──(Kirim File via API)──> [Google Drive Storage]
                                                 │
                                         (Ambil Link File)
                                                 │
                                                 ▼
                                         [Simpan Metadata] ──> [Database MongoDB]
```

1.  **Pengunggahan:** Pengguna mengunggah berkas bukti transaksi (JPG/PNG/PDF) melalui antarmuka React.
2.  **Penerusan Berkas:** FastAPI menerima berkas tersebut sebagai *multipart/form-data*, mengotentikasi sesi via **Google OAuth 2.0**, lalu mengirimkannya ke folder khusus di Google Drive milik BUMDes melalui Google Drive API.
3.  **Pencatatan Dokumen:** Google Drive API mengembalikan ID Unik berkas (*File ID*) beserta Tautan Tinjauan (*Web View Link*).
4.  **Penyimpanan Metadata:** FastAPI menyimpan informasi teks transaksi beserta Tautan Google Drive tersebut ke dalam dokumen transaksi di **MongoDB**.
5.  **Peninjauan Bukti:** Saat pengawas atau auditor mengklik tombol "Lihat Bukti" pada aplikasi, sistem akan memuat Tautan Google Drive tersebut secara aman di tab baru atau jendela *pop-up*.

---

## 🚀 Tech Stack yang Digunakan

### Backend (`/backend`)
*   **Core Framework:** [FastAPI](https://tiangolo.com) - *Framework* Python asinkron berperforma tinggi untuk penyediaan endpoint API.
*   **Database:** [MongoDB](https://mongodb.com) - Database NoSQL berbasis dokumen untuk menyimpan jurnal, buku besar, dan metadata transaksi secara fleksibel.
*   **Data Processing:** [Pandas](https://pydata.org) - Komputasi data untuk otomatisasi perhitungan neraca saldo, arus kas, dan laporan laba rugi.
*   **Document Generation (Ekspor Laporan):** 
    *   [ReportLab](https://reportlab.com) - *Engine* pembuat berkas laporan keuangan dalam format PDF secara dinamis.
    *   [OpenPyXL](https://readthedocs.io) - Konfigurasi otomatis laporan dalam bentuk *spreadsheet* Excel bulanan/tahunan.
*   **Integrations:** [Google Drive API](https://google.com) diotentikasi melalui **[Google OAuth 2.0](https://google.com)** - Penyimpanan digital bukti transaksi keuangan tanpa membebani penyimpanan *database*.

### Frontend (`/frontend`)
*   **Core UI Framework:** [React](https://react.dev) - Pembangunan antarmuka reaktif dengan kustomisasi konfigurasi via [Craco](https://js.org).
*   **Styling:** [Tailwind CSS](https://tailwindcss.com) - Kerangka kerja *utility-first* untuk desain dasbor akuntansi yang bersih dan responsif.
*   **Data Visualization:** [Recharts](https://recharts.org) - Komponen grafik interaktif untuk menyajikan transparansi visual terkait realisasi anggaran dan arus kas BUMDes.
*   **Iconography:** [Phosphor Icons](https://phosphoricons.com) - Pustaka ikon minimalis dan konsisten untuk navigasi menu keuangan.

---

## Deployment monorepo

Deploy `frontend` dan `backend` sebagai dua project terpisah dari repository yang sama.

### Project frontend

- Root Directory: `frontend`
- Framework preset: Create React App
- Install Command: `yarn install --frozen-lockfile`
- Build Command: `yarn build`
- Output Directory: `build`
- Environment variable: `REACT_APP_BACKEND_URL=https://api.example.com`

`frontend/yarn.lock` adalah satu-satunya lockfile frontend. Gunakan Yarn 1 sesuai `packageManager` di `package.json`; jangan membuat `package-lock.json` atau `pnpm-lock.yaml` tambahan.

### Project backend

- Root Directory: `backend`
- Runtime: Python/FastAPI dengan server ASGI
- Install Command: `pip install -r requirements.txt`
- Start Command: `uvicorn server:app --host 0.0.0.0 --port $PORT`
- Required variables: `MONGO_URL`, `DB_NAME`, `JWT_SECRET`, `CORS_ORIGINS`
- Google Drive variables, required only for Drive proof storage: `GDRIVE_OAUTH_CLIENT_DATA`, `GDRIVE_FOLDER_ID`, `GDRIVE_REDIRECT_URI`

Set environment variables separately for the frontend and backend deployment. Never commit real secrets. The repository-level `vercel.json` is intentionally not used for both applications: Vercel project settings control the Root Directory independently for each project.

## 🛠️ Panduan Instalasi & Pengoperasian

### Pengaturan Backend (Python)
1. Masuk ke dalam direktori backend:
   ```bash
   cd backend
   ```
2. Buat dan aktifkan lingkungan virtual (*virtual environment*):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Untuk Windows gunakan: venv\Scripts\activate
   ```
3. Pasang seluruh dependensi pustaka Python:
   ```bash
   pip install -r requirements.txt
   ```
4. Salin file `.env.example` menjadi `.env` lalu sesuaikan konfigurasi kode *Connection String* MongoDB, folder ID tujuan di Google Drive, serta kredensial **Google OAuth 2.0** Anda.
5. Jalankan server pengembangan lokal:
   ```bash
   uvicorn main:app --reload
   ```

### Pengaturan Frontend (Node.js)
1. Masuk ke dalam direktori frontend:
   ```bash
   cd frontend
   ```
2. Pasang modul Node.js yang diperlukan:
   ```bash
   npm install
   ```
3. Jalankan aplikasi React pada mode pengembangan:
   ```bash
   npm start
   ```
