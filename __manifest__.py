# -*- coding: utf-8 -*-
{
    'name': "SIRITA Mahad Portal (Portal Mahasantri)",
    'version': '20.0.1.0.0',
    'category': 'Website/Portal',
    'summary': 'Portal Layanan Mandiri Mahasantri (E-Perizinan, Buku Kendali, Syahadah, & Tagihan Asrama)',
    'description': """
SIRITA Mahad Portal — Layanan Mandiri Portal Mahasantri
======================================================
Modul integrasi Odoo Web Portal khusus Mahasantri UPT Ma'had Al-Jami'ah PTKIN.

Fitur Portal Mahasantri:
------------------------
* Dashboard Akun Mahasantri (/my)
* E-Perizinan Pesiar & Bermalam (Pengajuan & Status Approval)
* Buku Kendali (Hafalan Al-Qur'an & Riwayat Ta'lim)
* Catatan Disiplin & Poin Pelanggaran
* Syahadah & Sertifikat Kelulusan Digital
* Tagihan Asrama & Pembayaran BLU
    """,
    'author': 'sufyALDI | UPT TIPD IAIN Parepare',
    'website': 'https://mahad.iainpare.ac.id',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'web',
        'portal',
        'sirita_mahad',
        'sirita_mahad_pembinaan',
    ],
    'data': [
        'security/ir.access.csv',
        'views/portal_templates.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
