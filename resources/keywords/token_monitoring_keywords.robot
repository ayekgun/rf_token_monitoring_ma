*** Settings ***
Documentation    Keyword Layer untuk Mahkamah Agung Token WABA Monitoring Web UI & BFF
...              Menerapkan True Web UI Testing (Playwright Chromium) + Multi-Layer Observability
...              Sesuai Global QA SDET & Robot Framework Constitution (Clean BDD Murni)
Library          ../../libraries/TokenMonitoringLibrary.py

*** Keywords ***
# ==============================================================================
# SETUP & TEARDOWN KEYWORDS
# ==============================================================================

Persiapkan Lingkungan Pengujian Web UI
    SSH Persiapkan Skenario Uji SUT Log

Pulihkan Lingkungan Pengujian Web UI
    SSH Selesaikan Skenario Uji SUT Log

# ==============================================================================
# TC-001 KEYWORDS (LOGIN BERHASIL)
# ==============================================================================

Catat Snapshot Sesi Pengguna Awal Pada Database MongoDB
    DB Catat Snapshot Pengguna Awal Pada MongoDB

Pengguna Membuka Halaman Login Web UI
    UI Navigasi Ke Halaman Login

Pengguna Memasukkan Kredensial Valid Dan Mengklik Tombol Login
    UI Input Kredensial Valid Dan Submit Login

Halaman Teralihkan Ke Dashboard Dengan Judul Dan Subtitle Yang Tepat
    UI Verifikasi Tampilan Halaman Dashboard Dan Header

Cookie Keamanan Sesi Terbentuk Dengan Atribut Lengkap
    UI Verifikasi Atribut Cookie Sesi Keamanan

Database MongoDB Memperbarui Kolom Waktu Login Terakhir Pengguna
    DB Verifikasi Waktu Login Terakhir Pada MongoDB

# ==============================================================================
# TC-002 KEYWORDS (TAB INSIGHT 12 BULAN)
# ==============================================================================

Pengguna Berada Di Tab Insight Pada Halaman Dashboard
    UI Pastikan Berada Pada Tab Insight Dashboard

Judul Kartu Grafik Dan Jumlah Batang 12 Bulan Terverifikasi Sempurna
    UI Verifikasi Kartu Grafik Insight Dan Batang Bulanan

Kueri SQL Independen Berbatas Rentang Eksplisit Cocok Sempurna Dengan Metrik UI
    DB Verifikasi Agregasi SQL 12 Bulan Cocok Dengan Metrik UI

# ==============================================================================
# TC-003 KEYWORDS (TAB TOKEN STATS & 12 BULAN DROPDOWN)
# ==============================================================================

Pengguna Berpindah Ke Tab Token Stats
    UI Navigasi Ke Tab Token Stats Dashboard

Dropdown Bulan Memuat Tepat 12 Opsi Terurut Kronologis Dan Default Terpilih Bulan Berjalan
    UI Verifikasi Opsi Dropdown 12 Bulan Kronologis

Kueri SQL Independen Daftar Bulan Dan Harian November Sesuai Sempurna
    DB Verifikasi Daftar 12 Bulan Dan Harian November Pada SQL

# ==============================================================================
# TC-004 KEYWORDS (FILTER BULAN OKTOBER 2026)
# ==============================================================================

Pengguna Memilih Bulan Oktober 2026 Pada Dropdown Toolbar
    UI Pilih Opsi Bulan Oktober Pada Dropdown

Permintaan Jaringan AJAX Terkirim Dengan Parameter Query Month 2026-10
    UI Verifikasi Permintaan Jaringan AJAX Bulan Oktober

Metrik Dan Grafik Harian Diperbarui Sesuai Data Oktober Tanpa Residu November
    DB Verifikasi Metrik Dan Grafik Harian Oktober Pada SQL

# ==============================================================================
# TC-005 KEYWORDS (DATA FRESHNESS & TIMEZONE)
# ==============================================================================

Indikator Kesegaran Data Menampilkan Format Tanggal Dan Jam WIB
    UI Verifikasi Tampilan Teks Data Freshness

Kontrak Zona Waktu Asia Jakarta Terbukti Selaras Antara Database Dan API
    DB Verifikasi Kontrak Checkpoint Dan Zona Waktu Asia Jakarta

# ==============================================================================
# TC-006 KEYWORDS (LOGIN GAGAL)
# ==============================================================================

Pengguna Mengirimkan Kredensial Dengan Password Salah
    UI Input Kredensial Password Salah Dan Verifikasi Penolakan

Sistem Menampilkan Pesan Kesalahan Seragam Dan Tidak Menerbitkan Sesi
    Log    Verifikasi penolakan login kredensial invalid telah dieksekusi

Pengguna Mengirimkan Kredensial Dengan Akun Yang Tidak Terdaftar
    UI Input Kredensial Akun Tidak Terdaftar Dan Verifikasi Penolakan

# ==============================================================================
# TC-007 KEYWORDS (VALIDASI FORM KLIEN & DIRECT BACKEND 400)
# ==============================================================================

Pengguna Menekan Tombol Login Dengan Field Input Dikosongkan
    UI Validasi Native Klien Tahan Form Input Kosong

Permintaan Langsung Ke Backend Dengan Payload Kosong Ditolak Kode 400
    SEC Verifikasi Permintaan Backend Payload Kosong Ditolak 400

# ==============================================================================
# TC-008 KEYWORDS (PROTECTED ROUTE & API SECURITY)
# ==============================================================================

Pengguna Tanpa Sesi Mengakses URL Dashboard Secara Langsung
    UI Akses Langsung URL Dashboard Tanpa Sesi Otentikasi

Komponen ProtectedRoute Mengalihkan Halaman Langsung Ke Form Login
    UI Verifikasi Komponen ProtectedRoute Mengalihkan Ke Login

Seluruh Endpoint Monitoring Backend Menolak Akses Tanpa Sesi Dengan Kode 401
    SEC Verifikasi Seluruh Endpoint Monitoring Backend Ditolak 401

# ==============================================================================
# TC-009 KEYWORDS (LOGOUT LIFECYCLE & REPLAY ATTACK)
# ==============================================================================

Pengguna Login Aktif Dan Menangkap Token Akses Sebelum Logout
    UI Login Dan Ambil Token Sesi Dengan Protokol Masking

Pengguna Mengklik Tombol Logout Pada Header Dashboard
    UI Eksekusi Tombol Logout Pada Header Dashboard

Sesi Browser Dibersihkan Dan Tombol Back Peramban Menolak Akses
    UI Verifikasi Pembersihan Cookie Dan Proteksi Browser Back

Versi Sesi Pada MongoDB Bertambah Dan Token Lama Ditolak Kode 401 Terhadap Replay Attack
    SEC Verifikasi Kenaikan Versi Sesi Dan Replay Attack Ditolak 401

# ==============================================================================
# TC-010 KEYWORDS (ROUNDTRIP NAVIGASI & CONNECTION LEAK)
# ==============================================================================

Catat Baseline Koneksi Database Aktif
    DB Catat Baseline Koneksi Database Threads Connected

Pengguna Melakukan Navigasi Bolak Balik Antar Tab Sebanyak Tiga Putaran Penuh
    UI Eksekusi Navigasi Bolak Balik Tiga Putaran Penuh

Integritas Tampilan Grafik Tetap Utuh Dan Bebas Dari Kebocoran Pool Koneksi
    DB Verifikasi Integritas Tampilan Dan Ketiadaan Kebocoran Koneksi

# ==============================================================================
# TC-011 KEYWORDS (HOVER TOOLTIP & LOG SUT TERUKUR)
# ==============================================================================

Pengguna Berada Di Tab Token Stats Bulan November Dan Menyorot Batang Tanggal 18
    UI Arahkan Kursor Mouse Ke Batang Grafik Tanggal 18

Tooltip Menampilkan Nilai Yang Terbukti Cocok Dengan SQL Harian Dan Log SUT Bebas Peringatan
    DB Verifikasi Nilai Tooltip Cocok Dengan SQL Harian Dan Log Bersih

# ==============================================================================
# TC-012 KEYWORDS (EMPTY STATE DESEMBER 2025)
# ==============================================================================

Pengguna Memilih Bulan Tertua Desember 2025 Pada Dropdown Toolbar
    UI Pilih Opsi Bulan Tertua Desember 2025 Pada Dropdown

Metrik Penggunaan Dan Top Up Bernilai Nol Sementara Saldo Snapshot Dipertahankan
    DB Verifikasi Kondisi Nol Desember Dan Retensi Saldo Snapshot
