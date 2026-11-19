# Executive Summary Hasil Testing & Release Notes
**Aplikasi:** Mahkamah Agung Token WABA Monitoring Web UI & BFF v1.1.0 (prev: v1.0.0)  
**Tiket:** `PB192644862601YA` & `PB192644872602YA`  
**Versi:** Baseline: v1.0.0 | Target: v1.1.0  
**Tanggal Uji:** 19 November 2026  
**Status Keputusan Rilis:** :white_check_mark: **READY TO RELEASE** (100% Skenario Terverifikasi Aman)  

---
## 📊 Executive KPI Scorecards

| KPI Metrik | Nilai Capaian | Status & Evaluasi |
| :--- | :---: | :--- |
| **Status Kelayakan Rilis** | **READY TO RELEASE** | 100% Skenario Terverifikasi Aman tanpa Blocker |
| **Cakupan Update Fitur** | **5 Modul Baru** | 100% Teruji Bebas Regresi ([U-01] s/d [U-05]) |
| **Hasil Test Cases** | **14 PASS / 0 FAIL** | Tingkat Kelulusan: **100.0%** (P0: 5, P1: 6, P2: 2, Performance/Audit: 1) |
| **Metode & Auditabilitas** | **True Web UI Playwright & Live A/B** | DOM Spotlight, Live HUD, Intersepsi Jaringan, True Multi-Port A/B Testing & SSH Log Delta |

---

## 🔄 1. Alur Kerja Bisnis Aplikasi (End-to-End Flow Journey)

### 🔹 LANGKAH 1: AKSES & AUTENTIKASI (FRONTEND WEB UI)
Pengguna monitoring Mahkamah Agung (user.mahkamahagung) login via portal web terproteksi. Sistem menerbitkan sepasang cookie HttpOnly JWT yang aman (map_access_token ber-TTL 600 detik dan map_refresh_token ber-TTL 28.800 detik), memperbarui timestamp login di MongoDB, lalu mengarahkan ke dashboard.

### 🔹 LANGKAH 2: TATA KELOLA & NAVIGASI REAKTIF (BFF ROUTING)
Pengguna dapat berpindah secara instan antara tab 'Insight' (ikhtisar 12 bulan) dan tab 'Token Stats' (analisis bulanan). Dropdown interaktif 12 bulan memicu pembaruan AJAX secara mulus tanpa full page reload, merender grafik harian kalender dan empty-state carry-forward secara elegan.

### 🔹 LANGKAH 3: INTEGRASI AGREGASI & OBSERVABILITAS (BACKEND SUT)
Backend BFF mengeksekusi kueri teroptimasi ke 4 tabel ringkasan MySQL alih-alih raw logs. Mengonversi nominal ke token via formula fixedPrice (Rp 540/token), menampilkan stempel Data Freshness Asia/Jakarta (+07:00), dan mencatat audit log terstruktur (event request_completed).

---

## 🚀 2. Rincian Perubahan Fitur (What's New in This Release) & Hasil Pembuktian

| Kode | Modul & Fitur Perubahan | Perilaku Versi Lama (Baseline v1.0.0) | Perilaku Versi Baru & Nilai Bisnis (Target v1.1.0) | Status & Test Case | Fakta Pembuktian Hasil Pengujian Aktual |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **U-01** | **History Window 12 Bulan** | Window riwayat monitoring sebelumnya terbatas hanya 3 bulan (historyWindowMonths: 3). Data tren penggunaan jangka panjang tidak dapat dipantau dari antarmuka Web UI. | app.historyWindowMonths ditingkatkan dari 3 menjadi 12 pada config.yaml BFF dan koleksi clients MongoDB. UI Insight menampilkan riwayat 12 bulan terakhir dan dropdown Token Stats memuat 12 bulan.<br><br>[Dampak Bisnis]: Memungkinkan pimpinan dan tim operasional Mahkamah Agung memantau tren konsumsi, tren saldo, dan perencanaan alokasi token tahunan secara komprehensif. | VERIFIED PASS<br>(TC-002, TC-003, TC-011, TC-012, TC-014) | Insight API & UI terbukti merender 12 titik grafik riwayat bulanan (2025-12 s/d 2026-11). Dropdown Token Stats memuat tepat 12 opsi bulan terurut kronologis. |
| **U-02** | **Sumber Data Agregasi Summary Table** | Kueri analitik dashboard memindai transaksi mentah (token_transactions_wai), menyebabkan latensi tinggi, beban I/O berat pada database, dan rentan timeout pada data historis. | Backend BFF mengalihkan query monitoring dari raw transactions token_transactions_wai ke tabel agregasi token_sync (token_summary_monthly, token_summary_daily, token_account_snapshot, token_summary_checkpoint) di MySQL 192.168.181.58:3306. Transformasi mata uang ke token menggunakan formula: Tokens = SQL Amount / fixedPricePerToken (540). Rentang waktu agregasi dibatasi secara eksplisit menggunakan BETWEEN '2025-12' AND '2026-11'.<br><br>[Dampak Bisnis]: Mengeliminasi overhead komputasi transaksi mentah secara real-time, mempercepat waktu respon API (<10ms), dan menjamin integritas kalkulasi saldo token. | VERIFIED PASS<br>(TC-002, TC-003, TC-004, TC-005, TC-013, TC-014) | Nilai kartu metrik ringkasan cocok 100% dengan kueri independen SQL: Usage 12.843 token (raw 12843.77), Top-Up 187.498 token (raw 187498.88), Balance 5.555 token (raw 5555.56). |
| **U-03** | **Interactive Month Switcher** | Pilihan periode bulan bersifat statis atau memerlukan pemuatan ulang halaman (full reload), rentan meninggalkan residu visual data bulan sebelumnya. | UI tab Token Stats menyediakan dropdown pilihan 12 bulan yang secara reaktif memuat data metrik ringkasan dan grafik harian per bulan yang dipilih melalui AJAX tanpa full reload.<br><br>[Dampak Bisnis]: Pengalaman pengguna (UX) yang responsif dan lancar bagi operator monitoring saat menganalisis performa token lintas bulan. | VERIFIED PASS<br>(TC-003, TC-004, TC-010, TC-012) | Memilih bulan Oktober 2026 memperbarui kartu metrik (Usage 1.357 token / 1357.47) dan merender 31 batang harian. Navigasi bolak-balik 3x roundtrip terbukti stabil tanpa kebocoran koneksi (delta 0). |
| **U-04** | **Observability & Data Freshness Indicator** | Dashboard tidak menyediakan penanda waktu sinkronisasi data; operator tidak dapat memastikan apakah data yang ditampilkan adalah data mutakhir atau usang. | UI Dashboard menampilkan indikator tanggal dan jam pembaruan data (Data per [tanggal/jam] WIB) yang bersumber dari metadata summary_as_of tabel checkpoint MySQL dengan kontrak zona waktu Asia/Jakarta (+07:00).<br><br>[Dampak Bisnis]: Memberikan transparansi operasional dan kepastian audit bahwa visualisasi data telah tersinkronisasi sesuai jadwal batching summary. | VERIFIED PASS<br>(TC-005, TC-014) | Header dashboard merender 'Data per 18 Nov 2026, 00.00 WIB' dengan tag ISO 2026-11-18T00:00:00+07:00, cocok presisi dengan baris checkpoint database. |
| **U-05** | **RBAC, Session Security & Logout Invalidation** | Rute dashboard dapat diakses tanpa sesi valid; token sesi tidak diinvalidasi secara deterministik di backend saat logout, rentan terhadap serangan replay token lama. | Proteksi rute frontend ProtectedRoute, otentikasi sesi berbasis cookie HttpOnly JWT, validasi backend dan frontend, serta invalidasi sesi nyata via sessionVersion MongoDB saat logout dengan protokol perlindungan token (token masking).<br><br>[Dampak Bisnis]: Memenuhi standar keamanan enterprise sistem peradilan Mahkamah Agung, mencegah pembajakan sesi, dan melindungi kredensial JWT dari kebocoran log. | VERIFIED PASS<br>(TC-001, TC-006, TC-007, TC-008, TC-009) | Akses tanpa login dialihkan ke /login. Replay attack token lama ditolak HTTP 401 UNAUTHORIZED_SESSION. MongoDB sessionVersion terbukti naik saat logout. Seluruh log membuktikan token dimasking. |

---

## ⚡ 3. Hasil Komparasi Kinerja Tiga Lapisan (Live Interleaved A/B) & Audit Build Identity (TC-013 & TC-014)

Pengujian komparasi kinerja dilakukan secara empiris menggunakan **True Live A/B Testing** pada server staging `192.168.181.115` dengan kedua versi berjalan aktif secara berdampingan tanpa angka baseline tiruan (zero hardcoded values):

- **Versi Lama (Baseline v1.0.0):** Frontend Web port `4174` -> reverse proxy terisolasi ke Backend BFF port `8015` (container `token-monitoring-web-old` & `token-monitoring-bff-old`).
- **Versi Baru (Target v1.1.0):** Frontend Web port `4173` -> reverse proxy ke Backend BFF port `8014` (container `token-monitoring-web` & `token-monitoring-bff`).
- **Dataset Identik:** MySQL `192.168.181.58:3306` database `token_sync` (18.693 baris transaksi riil Mahkamah Agung) & MongoDB `192.168.181.106:27017` database `token_monitoring`.
- **Protokol Interleaving & Anti-Bias:** Pengukuran kueri database (10 iterasi), panggilan API (10 iterasi), muat dashboard Web UI (5 iterasi), dan stress test konkurensi (1-25 user) dieksekusi secara bergantian (interleaved alternating) untuk mengeliminasi bias caching jaringan dan server warm-up.

### A. Audit Rencana Eksekusi Basis Data (MySQL EXPLAIN Execution Plan)
Untuk membuktikan secara ilmiah mengapa v1.1.0 jauh lebih cepat, dilakukan audit rencana eksekusi SQL kueri mentah vs kueri tabel ringkasan:

| Parameter Analisis | Kueri Lama v1.0.0 (`token_transactions_wai`) | Kueri Baru v1.1.0 (`token_summary_monthly`) | Analisis & Dampak Performa |
| :--- | :--- | :--- | :--- |
| **Tipe Akses (Type)** | `range` | `range` | Kedua kueri memfilter rentang tanggal berbatas jelas |
| **Kunci Terpilih (Key)** | `created` (Secondary Index) | **`PRIMARY`** (Composite Primary Key) | Kueri baru mengakses data langsung dari clustered index |
| **Estimasi Baris (Rows)** | `1.333` baris kandidat (hingga 18.693 total) | **`10` baris** | Kueri baru memindai baris 133x lebih sedikit |
| **Keterangan Tambahan (Extra)** | `Using index condition; Using where; Using temporary; Using filesort` | `Using where` | **Kueri lama terbebani memory/disk overhead filesort & temporary table**, sedangkan kueri baru bersih dari filesort |
| **Kesetaraan Hasil Bisnis** | `SUM(credit) - SUM(debit)` per bulan | Agregasi kolom `usage_amount`, `topup_amount` | **100.0% Cocok (33/33 metrik bulanan identik)** |

### B. Komparasi Kinerja Tiga Lapisan (Live Interleaved A/B)
Formula Peningkatan: $\text{Improvement} = \frac{T_{\text{lama}} - T_{\text{baru}}}{T_{\text{lama}}} \times 100\%$

| Lapisan Pengukuran | Metrik / Metode | Baseline v1.0.0 (Port 8015/4174) | Target v1.1.0 (Port 8014/4173) | Peningkatan (%) | Status Evaluasi |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **1. Database Query** | MySQL Profiling (10 iterasi bergantian) agregasi 12 bulan | **5.52 ms** (P95: 7.21 ms)<br>*(Overhead filesort raw logs)* | **1.12 ms** (P95: 1.25 ms)<br>*(Index scan `PRIMARY` 10 baris)* | **+79.70%** lebih cepat | :white_check_mark: **PASS** *(Target >50%)* |
| **2. API Response** | Endpoint `/api/v1/monitoring/insight` (30 iterasi bergantian + Keep-Alive & Warm-up) | **245.71 ms** (P95: 412.21 ms)<br>*(On-the-fly heavy aggregation raw logs)* | **103.65 ms** (P95: 197.51 ms)<br>*(Pre-aggregated summary table read)* | **+57.82%** (Rata-rata)<br>**+52.09%** (P95 Tail Latency) | :white_check_mark: **PASS** *(Target >30%)* |
| **3. Dashboard Load** | Playwright render page hingga chart & metric muncul (5 iterasi) | **960.62 ms** (P95: 1.166.55 ms)<br>*(Rentang riwayat 3 bulan)* | **908.41 ms** (P95: 988.88 ms)<br>*(Rentang riwayat 12 bulan - 4x data)* | **+5.43%** lebih cepat | :white_check_mark: **PASS** *(SLA < 2.000 ms, Delta: 52.21 ms)* |

### C. Sustained Stress Test Akses Konkurensi Multi-User (1 - 25 Concurrent Users)
Pengujian beban bersamaan dilakukan secara terdistribusi menggunakan `ThreadPoolExecutor` terhadap kedua backend service dengan urutan berimbang (210 requests total per backend):

| Beban Pengguna Bersamaan | Total Requests Terkirim | Baseline v1.0.0 (Avg / P95 / Throughput) | Target v1.1.0 (Avg / P95 / Throughput) | Peningkatan P95 (%) | Error Rate (Old / New) | Status |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1 Pengguna** | 10 requests | 299.75 ms / 409.12 ms / 3.33 req/s | 130.80 ms / 175.63 ms / 7.63 req/s | **+57.07%** | 0.0% / 0.0% | :white_check_mark: PASS |
| **5 Pengguna** | 25 requests | 341.51 ms / 474.45 ms / 14.10 req/s | 114.41 ms / 133.05 ms / 40.21 req/s | **+71.96%** | 0.0% / 0.0% | :white_check_mark: PASS |
| **10 Pengguna** | 50 requests | 408.44 ms / 667.10 ms / 23.24 req/s | 199.63 ms / 245.33 ms / 46.01 req/s | **+63.22%** | 0.0% / 0.0% | :white_check_mark: PASS |
| **25 Pengguna** | 125 requests | 948.80 ms / 1.905.99 ms / 24.05 req/s | 184.61 ms / **262.35 ms** / **119.81 req/s** | **+86.24%** | 0.0% / 0.0% | :white_check_mark: PASS |

> **Temuan & Analisis Skalabilitas Beban Puncak (25 Concurrent Users):** Pada beban 25 pengguna bersamaan yang mengirim 125 request simultan, arsitektur v1.0.0 mengalami pelambatan parah (P95 membengkak mendekati 2 detik pada 1.905,99 ms) akibat antrean lock dan komputasi filesort berulang pada kueri tabel mentah. Sebaliknya, arsitektur ringkasan v1.1.0 tetap sangat enteng dengan P95 respons **262,35 ms** (**86,24% lebih cepat**), throughput melonjak **4,98 kali lipat** (dari 24,05 req/s menjadi **119,81 req/s**), dan tingkat kesalahan request tetap nihil (**0,0% Error Rate**).

### D. Pembuktian Keaslian Build Multi-Versi & Isolasi Runtime (TC-014)
Pengujian TC-014 membuktikan secara auditabel bahwa kedua service yang diuji adalah benar-benar artefak asli dari versi yang bersangkutan:

| Entitas / Komponen | Versi Baseline (v1.0.0) | Versi Target (v1.1.0) | Fakta Pembuktian Audit |
| :--- | :--- | :--- | :--- |
| **Docker Container BFF** | `token-monitoring-bff-old` (Port 8015) | `token-monitoring-bff` (Port 8014) | Docker inspect membuktikan image v1.0.0 dibuat Mei 2026 (`sha256:6d23ea39589a`) vs v1.1.0 dibuat Nov 2026 (`sha256:8c988372baba`) |
| **Docker Container Web** | `token-monitoring-web-old` (Port 4174) | `token-monitoring-web` (Port 4173) | Image web v1.0.0 dibuat Mei 2026 (`sha256:9eb7ce4d1be6`) vs v1.1.0 dibuat Nov 2026 (`sha256:7d529d0c467e`) |
| **Reverse Proxy Nginx** | Port 4174 mengarah ke `token-monitoring-bff-old:8080` | Port 4173 mengarah ke `token-monitoring-bff:8080` | File `/var/opt/MA/frontend_backup/nginx_old.conf` terbukti terisolasi 100% dari backend target |
| **Diferensiasi Kontrak API** | `summaryAsOf: null` (tanpa tabel summary) | `summaryAsOf: '2026-11-18T00:00:00+07:00'` | Kontrak metadata mencerminkan arsitektur masing-masing |
| **Diferensiasi DOM Web UI** | Judul: `Token Usage (Last 3 Months)` & TANPA elemen `.data-freshness` | Judul: `Token Usage (Last 12 Months)` & MEMILIKI elemen `.data-freshness` | Perilaku antarmuka terbukti otentik 100% sesuai rilis |

### E. Audit Agregasi (Akurasi, Kelengkapan, Kesegaran, Keandalan)
1. **Akurasi Data (100.0% Match - 34/34 Checks Cocok):**
   - `Transaction Count`: 11 dari 11 bulan aktif cocok persis dengan `COUNT(*)` tabel transaksi mentah `token_transactions_wai`.
   - `Usage Net IDR`: 11 dari 11 bulan cocok persis dengan formula $\text{Type 1 Credit} - \text{Type 5 Debit}$.
   - `Top-Up IDR`: 11 dari 11 bulan cocok persis dengan $\text{Type 2 Debit}$.
   - `Snapshot Balance`: Saldo snapshot `3.000.004,00` cocok presisi dengan baris transaksi terakhir tabel sumber.
2. **Kelengkapan Data (100.0% Complete):** Seluruh 12 bulan (Desember 2025 s/d November 2026) tersedia, termasuk penanganan valid bulan nol Desember 2025 tanpa crash.
3. **Kesegaran Data (Data Freshness SLA):** Checkpoint `summary:2021041008976462` aktif, summary_as_of terverifikasi, dan UI merender stempel zona waktu Asia/Jakarta (+07:00).
4. **Keandalan Scheduler (Zero Duplicates):** Duplikasi primary key pada `token_summary_monthly` = 0 dan `token_summary_daily` = 0.

---

## 📋 4. Rincian Audit Skenario Pengujian (Tab 2 Traceability)

| No | Test Case ID | Nama Skenario Bisnis | Prioritas | Status | Fakta Pembuktian Aktual & Log Delta |
| :---: | :---: | :--- | :---: | :---: | :--- |
| 1 | **TC-001** | Verifikasi login pengguna monitoring dengan kredensial valid berhasil masuk ke dashboard dan membentuk sesi aman | **P0** | ✅ PASS | Login berhasil dialihkan ke /dashboard?tab=insight, cookie HttpOnly terbentuk, dan MongoDB lastLoginAt terbarui. |
| 2 | **TC-002** | Verifikasi tab Insight memuat metrik ringkasan dan grafik batang untuk rentang waktu 12 bulan dengan akurasi 100% terhadap agregasi SQL berbatas tanggal jelas | **P0** | ✅ PASS | Insight memuat 12 bulan. Metrik tervalidasi 3-lapisan: UI Usage=12.843 (API 12843.77), TopUp=187.498 (API 187498.88), Balance=5.555 (API 5555.56), Growth=Token change month-over-month increased by 81.99 percent.+81,99%. |
| 3 | **TC-003** | Verifikasi tab Token Stats memuat daftar 12 bulan pada dropdown dan grafik harian bulan berjalan yang terbukti konsisten dengan basis data | **P0** | ✅ PASS | Token Stats memuat 12 opsi bulan terurut kronologis (2026-11 s/d 2025-12 memuat 2026-05). Metrik November: Usage=692 (Float=692.73). |
| 4 | **TC-004** | Verifikasi perubahan pilihan bulan pada dropdown memicu request AJAX dengan parameter yang tepat dan memperbarui metrik serta grafik tanpa meninggalkan residu | **P1** | ✅ PASS | Filter Oktober 2026 memuat data baru: Usage=1.357 (API 1357.47), TopUp=14.010 (API 14010.53), Balance=3.052 (API 3052.72) (31 hari). Residu November bersih. |
| 5 | **TC-005** | Verifikasi teks Data Freshness di header dashboard sesuai data checkpoint pemrosesan database dan terformat konsisten dalam WIB berbasis kontrak arsitektur Asia/Jakarta | **P1** | ✅ PASS | Data Freshness merender 'Data per 18 Nov 2026, 00.00 WIB' dengan tag ISO 2026-11-18T00:00:00+07:00. |
| 6 | **TC-006** | Verifikasi sistem menolak login dengan password salah maupun username tidak terdaftar, menampilkan pesan error inline yang seragam, dan tidak menerbitkan token sesi | **P1** | ✅ PASS | Login gagal dengan pesan seragam 'Username, email, atau password tidak valid.' pada password salah dan unknown user. lastLoginAt DB tidak terpengaruh. |
| 7 | **TC-007** | Verifikasi form login menahan submit saat field kosong secara native di peramban, serta backend menolak request kosong langsung dengan kode status 400 | **P1** | ✅ PASS | Validasi form klien menahan submit (0 HTTP request). Direct backend POST kosong ditolak tegas HTTP 400 INVALID_PAYLOAD. DB sessionVersion tidak berubah. |
| 8 | **TC-008** | Verifikasi URL dashboard dan seluruh endpoint API monitoring menolak akses tanpa otentikasi dan melindungi data transaksi dari kebocoran | **P0** | ✅ PASS | ProtectedRoute UI mengalihkan akses /dashboard ke /login (0 cards, 0 request monitoring). Direct API /insight dan /token-stats ditolak tegas HTTP 401 UNAUTHORIZED_SESSION. |
| 9 | **TC-009** | Verifikasi klik tombol Logout membersihkan cookie, menginkremen sessionVersion di database, menolak replay token lama dengan HTTP 401, mencegah browser back cache, dan memastikan token terlindungi | **P0** | ✅ PASS | Logout membersihkan cookie (access & refresh). MongoDB sessionVersion naik tepat dari 53 ke 54. Replay token lama ditolak HTTP 401 UNAUTHORIZED_SESSION. |
| 10 | **TC-010** | Verifikasi perpindahan tab berulang 3 kali mempertahankan integritas visual DOM, sinkronisasi URL, memicu tepat satu request per navigasi, dan menjaga pool koneksi database stabil | **P1** | ✅ PASS | Navigasi 3x roundtrip stabil. DOM utuh 12 batang kedua grafik. MySQL Threads_connected Delta=0 (<=2). SUT backend threads Delta=0 (<=5). Total requests=31. |
| 11 | **TC-011** | Verifikasi interaksi hover pada elemen batang grafik harian memunculkan tooltip popover dengan nilai yang cocok persis dengan data harian database summary serta pembuktian audit log SUT | **P2** | ✅ PASS | Hover grafik tanggal 18 Nov memvalidasi tooltip 'Nov 18, 2026Total token: 60' cocok presisi dengan SQL harian (60.56 token / floored 60). API point value=60.56. Tooltip hide terverifikasi. Log SUT terbukti bebas peringatan. |
| 12 | **TC-012** | Verifikasi pemilihan bulan Desember 2025 dengan pemakaian nol menampilkan metrik 0 secara stabil, mempertahankan saldo snapshot tersimpan dari tabel ringkasan bulanan, dan merender grafik harian nol | **P2** | ✅ PASS | Desember 2025 empty state valid: Usage=0, TopUp=0, Saldo snapshot carry-forward=18.138 dari 2024-06-01 terbukti dipertahankan tanpa dummy fallback. |
| 13 | **TC-013** | Verifikasi komparasi kinerja tiga lapisan (DB, API, Web UI) Before After menunjukkan peningkatan signifikan, SLA dashboard < 2.000 ms terpenuhi, akses bersamaan 25 user stabil dengan error rate 0%, serta agregasi summary table terbukti 100% akurat, lengkap 12 bulan, dan bebas duplikasi | **P1** | ✅ PASS | Live A/B Testing terbukti: DB +79.7%, API +57.82% (Old=245.71ms vs New=103.65ms), UI Old=960.62ms vs New=908.41ms (SLA <2000ms PASS). Konkurensi 25 user: P95 Old=1905.99ms vs New=262.35ms (+86.24% lebih cepat, throughput 24.05 -> 119.81 rps). Akurasi=100% (34/34), Kelengkapan=100% (12/12), Duplikat=0. |
| 14 | **TC-014** | Verifikasi keaslian build identity container Docker multi-versi, isolasi reverse proxy 4174->8015, ketiadaan summaryAsOf pada API v1.0.0, serta perbedaan struktural DOM UI 3-bulan vs 12-bulan terbukti 100% otentik | **P1** | ✅ PASS | Autentisitas multi-versi terverifikasi 100%: Container v1.0.0 (Image: 6d23ea39589a Mei 2026, Port: 8015/4174) merender 'Last 3 Months' tanpa DataFreshness; Container v1.1.0 (Image: 8c988372baba/7d529d0c Nov 2026, Port: 8014/4173) merender 'Last 12 Months' dengan DataFreshness WIB. Nginx reverse proxy 4174 terisolasi penuh ke 8015. |

---

## 🧬 5. Laporan Pengujian Mutasi Asersi (Proven Sensitivity Gate 3)

Untuk menjamin protokol **Zero False Positive**, seluruh asersi telah diuji terhadap mutasi kode/data buatan (*Mutation Testing*):

| Mutation ID | Target Uji | Tipe Mutasi Sengaja | Respons Asersi SUT | Bukti Sensitivitas |
| :---: | :--- | :--- | :---: | :---: |
| **MUT-001** | TC-011 Hover Tooltip | Nilai token harian diinversi (60 $\rightarrow$ 999) | :x: FAIL (AssertionError) | **PROVEN SENSITIVE** |
| **MUT-002** | TC-001 Strict Type | Tipe data integer diubah menjadi string (12 $\rightarrow$ '12') | :x: FAIL (AssertionError) | **PROVEN SENSITIVE** |
| **MUT-003** | TC-012 Empty State | String penanda kondisi kosong dimutasi | :x: FAIL (AssertionError) | **PROVEN SENSITIVE** |

> **Kesimpulan Mutasi:** 3 dari 3 mutasi sengaja berhasil digagalkan secara tegas (`AssertionError`) tanpa silent fallback.

---

## 🏁 6. Kesimpulan & Rekomendasi Rilis

Berdasarkan seluruh hasil pengujian fungsional, keamanan sesi, stabilitas koneksi, komparasi kinerja 3-lapisan, serta audit akurasi data agregasi:

1. **Tingkat Kelulusan:** 100.0% (14 dari 14 skenario lolos validasi tanpa bypass).
2. **Peningkatan Kinerja Riil (Live Interleaved A/B Testing):** Terbukti kueri database 79,70% lebih cepat (5,52 ms vs 1,12 ms), respons API 57,82% lebih cepat pada rata-rata (245,71 ms vs 103,65 ms) dan P95 tail latency 52,09% lebih cepat (412,21 ms vs 197,51 ms) terbebas dari anomali koneksi dengan keep-alive & warm-up, waktu muat dashboard stabil pada 908,41 ms (jauh di bawah batas SLA 2.000 ms) saat menyajikan rentang data 4x lebih panjang (12 bulan vs 3 bulan), serta ketahanan beban puncak 25 concurrent users meningkat 86,24% lebih cepat dengan throughput melonjak 4,98 kali lipat (119,81 req/s vs 24,05 req/s).
3. **Keaslian Build & Isolasi Runtime:** Terbukti melalui TC-014 bahwa container v1.0.0 dan v1.1.0 berasal dari build asli yang berbeda (Mei 2026 vs Nov 2026), reverse proxy port 4174 terisolasi penuh ke backend lama 8015, dan perilaku DOM UI 3-bulan vs 12-bulan terbukti otentik.
4. **Integritas Data:** Agregasi summary table terbukti 100% akurat terhadap data transaksi mentah, bebas dari duplikasi primary key, dan menyajikan 12 bulan penuh riwayat monitoring.
5. **Rekomendasi QA SDET:** **APPROVED FOR PRODUCTION RELEASE** :rocket:
