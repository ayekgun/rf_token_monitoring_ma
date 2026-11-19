*** Settings ***
Documentation    Suite Pengujian Otomasi E2E & Backend Mahkamah Agung Token WABA Monitoring Web UI & BFF
...              Tiket: PB192644862601YA & PB192644872602YA | SUT: Mahkamah Agung Monitoring
...              Menerapkan Clean BDD Murni, Zero False Positive & Transparent Multi-Layer Logging
Resource         ../resources/keywords/token_monitoring_keywords.robot
Suite Setup      UI Buka Sesi Browser Playwright
Suite Teardown   UI Tutup Sesi Browser Playwright
Test Setup       Persiapkan Lingkungan Pengujian Web UI
Test Teardown    Pulihkan Lingkungan Pengujian Web UI

*** Test Cases ***
TC-001 Verifikasi Login Pengguna Monitoring Dengan Kredensial Valid Berhasil Masuk Ke Dashboard
    [Tags]    P0    TC-001    auth    login    session    happy_path
    Given Catat Snapshot Sesi Pengguna Awal Pada Database MongoDB
    When Pengguna Membuka Halaman Login Web UI
    And Pengguna Memasukkan Kredensial Valid Dan Mengklik Tombol Login
    Then Halaman Teralihkan Ke Dashboard Dengan Judul Dan Subtitle Yang Tepat
    And Cookie Keamanan Sesi Terbentuk Dengan Atribut Lengkap
    And Database MongoDB Memperbarui Kolom Waktu Login Terakhir Pengguna

TC-002 Verifikasi Tab Insight Memuat Metrik Ringkasan Dan Grafik Batang Untuk Rentang Waktu 12 Bulan
    [Tags]    P0    TC-002    dashboard    insight    history12m    summary_mysql    happy_path
    Given Pengguna Berada Di Tab Insight Pada Halaman Dashboard
    When Judul Kartu Grafik Dan Jumlah Batang 12 Bulan Terverifikasi Sempurna
    Then Kueri SQL Independen Berbatas Rentang Eksplisit Cocok Sempurna Dengan Metrik UI

TC-003 Verifikasi Tab Token Stats Memuat Daftar 12 Bulan Pada Dropdown Dan Grafik Harian Bulan Berjalan
    [Tags]    P0    TC-003    dashboard    token_stats    month_dropdown    summary_mysql    happy_path
    Given Pengguna Berada Di Tab Insight Pada Halaman Dashboard
    When Pengguna Berpindah Ke Tab Token Stats
    Then Dropdown Bulan Memuat Tepat 12 Opsi Terurut Kronologis Dan Default Terpilih Bulan Berjalan
    And Kueri SQL Independen Daftar Bulan Dan Harian November Sesuai Sempurna

TC-004 Verifikasi Perubahan Pilihan Bulan Pada Dropdown Memperbarui Ringkasan Metrik Dan Grafik Harian
    [Tags]    P1    TC-004    dashboard    token_stats    month_filter    ajax    happy_path
    Given Pengguna Berpindah Ke Tab Token Stats
    When Pengguna Memilih Bulan Oktober 2026 Pada Dropdown Toolbar
    Then Permintaan Jaringan AJAX Terkirim Dengan Parameter Query Month 2026-10
    And Metrik Dan Grafik Harian Diperbarui Sesuai Data Oktober Tanpa Residu November

TC-005 Verifikasi Teks Data Freshness Di Header Dashboard Sesuai Data Checkpoint Pemrosesan Database
    [Tags]    P1    TC-005    dashboard    observability    freshness    timezone    happy_path
    Given Pengguna Berada Di Tab Insight Pada Halaman Dashboard
    When Indikator Kesegaran Data Menampilkan Format Tanggal Dan Jam WIB
    Then Kontrak Zona Waktu Asia Jakarta Terbukti Selaras Antara Database Dan API

TC-006 Verifikasi Sistem Menolak Login Kredensial Invalid Dan Menampilkan Pesan Error Inline Seragam
    [Tags]    P1    TC-006    auth    login    negative    security
    Given Pengguna Membuka Halaman Login Web UI
    When Pengguna Mengirimkan Kredensial Dengan Password Salah
    Then Sistem Menampilkan Pesan Kesalahan Seragam Dan Tidak Menerbitkan Sesi
    And Pengguna Mengirimkan Kredensial Dengan Akun Yang Tidak Terdaftar

TC-007 Verifikasi Form Login Menahan Submit Saat Field Kosong Serta Backend Menolak Request Kosong
    [Tags]    P1    TC-007    auth    login    validation    client_server    negative
    Given Pengguna Membuka Halaman Login Web UI
    When Pengguna Menekan Tombol Login Dengan Field Input Dikosongkan
    Then Permintaan Langsung Ke Backend Dengan Payload Kosong Ditolak Kode 400

TC-008 Verifikasi URL Dashboard Dan Seluruh Endpoint Monitoring Menolak Akses Tanpa Autentikasi
    [Tags]    P0    TC-008    security    protected_route    api_auth    negative
    Given Pengguna Tanpa Sesi Mengakses URL Dashboard Secara Langsung
    When Komponen ProtectedRoute Mengalihkan Halaman Langsung Ke Form Login
    Then Seluruh Endpoint Monitoring Backend Menolak Akses Tanpa Sesi Dengan Kode 401

TC-009 Verifikasi Alur Logout Terminasi Sesi Nyata Dan Penolakan Replay Token Terhadap Replay Attack
    [Tags]    P0    TC-009    auth    logout    session_invalidation    replay_attack    security
    Given Pengguna Login Aktif Dan Menangkap Token Akses Sebelum Logout
    When Pengguna Mengklik Tombol Logout Pada Header Dashboard
    Then Sesi Browser Dibersihkan Dan Tombol Back Peramban Menolak Akses
    And Versi Sesi Pada MongoDB Bertambah Dan Token Lama Ditolak Kode 401 Terhadap Replay Attack

TC-010 Verifikasi Perpindahan Tab Navigasi Bolak Balik Multi Roundtrip Mempertahankan Integritas Data
    [Tags]    P1    TC-010    dashboard    navigation    roundtrip    connection_leak    stability
    Given Catat Baseline Koneksi Database Aktif
    When Pengguna Melakukan Navigasi Bolak Balik Antar Tab Sebanyak Tiga Putaran Penuh
    Then Integritas Tampilan Grafik Tetap Utuh Dan Bebas Dari Kebocoran Pool Koneksi

TC-011 Verifikasi Interaksi Hover Pada Elemen Batang Grafik Menampilkan Rincian Bulan Dan Nilai Token
    [Tags]    P2    TC-011    dashboard    chart    tooltip    hover    ux
    Given Pengguna Berada Di Tab Insight Pada Halaman Dashboard
    When Pengguna Berada Di Tab Token Stats Bulan November Dan Menyorot Batang Tanggal 18
    Then Tooltip Menampilkan Nilai Yang Terbukti Cocok Dengan SQL Harian Dan Log SUT Bebas Peringatan

TC-012 Verifikasi Pemilihan Bulan Dengan Aktivitas Nol Menampilkan Metrik Nol Tanpa Merusak Antarmuka
    [Tags]    P2    TC-012    dashboard    token_stats    empty_state    retention    edge_case
    Given Pengguna Berada Di Tab Insight Pada Halaman Dashboard
    When Pengguna Memilih Bulan Tertua Desember 2025 Pada Dropdown Toolbar
    Then Metrik Penggunaan Dan Top Up Bernilai Nol Sementara Saldo Snapshot Dipertahankan


TC-013 Komparasi Kinerja Tiga Lapisan Before After Dan Audit Akurasi Kelengkapan Agregasi
    [Tags]    P1    TC-013    performance    benchmark    before_after    three_tier    audit
    Given Pengukuran Kinerja Kueri Database Sebelum Dan Sesudah Pembaruan Telah Dilakukan
    When Pengukuran Kinerja API Dan Waktu Muat Antarmuka Dashboard Terekam
    Then Peningkatan Kinerja Tiga Lapisan Terbukti Sesuai Formula Dan Target
    And Akurasi Kelengkapan Serta Keandalan Agregasi Terverifikasi Seratus Persen
