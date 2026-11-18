# IoT Absensi Biometrik — Versi Lite (Demo Lokal)

**2-Layer Anti-Spoofing Attendance** — eksperimen deteksi kehadiran orang
menggunakan OpenCV murni. Berjalan **penuh lokal tanpa server & tanpa database**.

---

## 🎯 Konsep: Anti-Spoofing 2 Lapis

Sistem absensi berbasis kamera rentan ditipu dengan foto diam. Versi ini
menolak foto dengan menggabungkan **dua lapis verifikasi**:

| Lapis | Fungsi | Menangkal |
|---|---|---|
| 1. **Face Detection** | Memastikan ada orang di depan kamera | Tidak ada orang / frame kosong |
| 2. **Gesture Liveness** | Memastikan itu orang hidup lewat gestur angkat tangan | Foto diam / video statis |

Hanya ketika **wajah terdeteksi** DAN **tangan terangkat di atas wajah**
→ status `VERIFIED OK`. Foto diam saja tidak akan lolos.

## ✨ Fitur Versi Lite

- Deteksi wajah real-time (Haar cascade bawaan OpenCV).
- Deteksi gestur "angkat tangan" sebagai bukti hidup (liveness).
- Overlay visual: kotak wajah + status langsung di jendela kamera.
- Tanpa server, tanpa database, tanpa terhubung ke internet saat dijalankan.
- Kode singkat & berkomentar — mudah dipelajari/dimodifikasi.

## ▶️ Cara Install & Jalankan

Persyaratan: **Python 3.8+** dan webcam.

```bash
# 1. Clone
git clone https://github.com/novalnw/Vall_iot_karyawan_monitoring_source.git
cd Vall_iot_karyawan_monitoring_source

# 2. (Disarankan) buat virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependensi
pip install -r requirements.txt

# 4. Jalankan
python lite_attendance_demo.py
```

> Pada Debian/Kali (PEP 668), wajib memakai virtual environment di atas.

**Cara pakai:** hadapkan wajah ke kamera, lalu **angkat tangan di atas kepala**.
Lihat status di jendela: `WAJAH TERDETEKSI` → `TANGAN TERANGKAT` → `VERIFIED OK`.
Tekan **Q** untuk keluar.

## 📁 Struktur

```
Vall_iot_karyawan_monitoring_source/
├── lite_attendance_demo.py   # skrip utama (deteksi wajah + liveness)
├── requirements.txt           # opencv-python, numpy
└── README.md
```

## 🔒 Privasi

Semua pemrosesan dilakukan **lokal di perangkatmu**. Tidak ada video/foto
yang diunggah ke server mana pun.

---

## 🚀 Versi Full-Stack Tersedia

Repositori ini hanya berisi **versi Lite** untuk mencoba konsepnya. Tersedia
pula **versi Full-Stack** yang sudah lengkap, mencakup:

- **Dashboard Monitoring Real-Time** (berbasis web).
- **Integrasi Database** (MariaDB/MySQL) untuk penyimpanan log absensi.
- **API & WebSocket** untuk verifikasi dua tahap + autentikasi multi-user.
- **Deploy cloud**: Frontend (Firebase Hosting) + Backend (Fly.io/Render).
- **Bantuan setup** hingga sistem berjalan.

Untuk demo, kolaborasi, atau lisensi versi Full-Stack, hubungi langsung:

- 🌐 **https://vallportofolio.web.app**
- 💬 **WhatsApp: [tulis nomor WhatsApp-mu di sini]**

---

© Ven Source code ini dibagikan untuk keperluan evaluasi/pembelajaran.
Dilarang menjual ulang tanpa izin pemilik.
