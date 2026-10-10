# 🎓 SIRITA Mahad Portal (Portal Mandiri Mahasantri)

Modul **SIRITA Mahad Portal** (`sirita_mahad_portal`) adalah modul integrasi **Odoo Web Portal** khusus untuk Mahasantri **UPT Ma'had Al-Jami'ah PTKIN**. Modul ini menyediakan layanan mandiri berbasis web agar mahasantri dapat memantau kegiatan asrama, perizinan, pembinaan hafalan, kedisiplinan, serta kelulusan syahadah secara transparan dan real-time.

---

## 🌟 Fitur Utama

1. **Dashboard Akun Mahasantri (`/my`)**:
   - Tampilan integrasi card-based modern di halaman portal Odoo.
   - Akses cepat ke seluruh fitur utama layanan mahasantri.

2. **🎫 E-Perizinan Pesiar & Bermalam (`/my/permits`)**:
   - Pemantauan status pengajuan perizinan keluar asrama (*Draft*, *Approved*, *Rejected*).
   - Pengajuan izin mandiri oleh mahasantri.

3. **📖 Buku Kendali (Ta'lim & Hafalan) (`/my/talim`)**:
   - Pemantauan kehadiran kegiatan ta'lim subuh & malam.
   - Catatan setoran hafalan Al-Qur'an dan bimbingan musyrif/pengampu.

4. **⚠️ Catatan Kedisiplinan & Poin (`/my/penalties`)**:
   - Transparansi poin pelanggaran kedisiplinan mahasantri.
   - Informasi sanksi edukatif terpadu.

5. **📜 Syahadah Digital & Kelulusan (`/my/syahadah`)**:
   - Verifikasi status kelulusan ma'had dan predikat.
   - Unduh sertifikat digital (PDF) dengan nomor seri resmi.

---

## 🏗️ Arsitektur & Dependensi

Modul ini dibuat untuk berjalan di lingkungan **Odoo 20** dan membutuhkan dependensi modul berikut:

- `base`
- `web`
- `portal`
- `sirita_mahad`
- `sirita_mahad_pembinaan`

---

## 📦 Struktur Direktori

```text
sirita_mahad_portal/
├── README.md
├── __init__.py
├── __manifest__.py
├── controllers/
│   ├── __init__.py
│   └── portal.py
├── security/
│   └── ir.access.csv
└── views/
    └── portal_templates.xml
```

---

## 👤 Author & Lisensi

- **Pengembang**: sufyALDI | UPT TIPD IAIN Parepare
- **Website**: [https://iainpare.ac.id](https://iainpare.ac.id)
- **Lisensi**: LGPL-3
