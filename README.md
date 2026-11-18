# Robot Framework Automation Suite: Mahkamah Agung Token WABA Monitoring (PB192644862601YA & PB192644872602YA)

Suite otomasi pengujian **Robot Framework** berbasis **True Web UI Testing** untuk aplikasi **Mahkamah Agung - Token WABA Monitoring Web UI & BFF**.

---

## 📌 Informasi Proyek
- **Tiket JIRA / CRD**:
  - `PB192644862601YA` (Update Scheduler Query - Add Summary Tables)
  - `PB192644872602YA` (Update Dashboard Mahkamah Agung - 12 Months Summary & Chart)
- **SUT (System Under Test)**: Mahkamah Agung Token WABA Monitoring Web (React 18) & BFF (Go 1.22)
- **Target URL Web UI**: `http://192.168.181.115:4173/`
- **Target URL BFF API**: `http://192.168.181.115:8014/`
- **Cakupan Pengujian**: 12 Test Cases (`TC-001` s/d `TC-012`)
- **Kaidah Utama**:
  - **Clean BDD Murni**: *Zero Dollar Signs* (`${...}`) pada blok `*** Test Cases ***`.
  - **True Web UI Testing**: 100% aksi bisnis dipicu melalui browser Chromium via Playwright CDP (bukan direct API bypass).
  - **Heads-Up Display (HUD) & Spotlight Box Overlay**: Visualisasi interaktif real-time saat eksekusi browser berjalan.
  - **Multi-Layer Observability**: Verifikasi 4 lapisan pembuktian: DOM Visual + Intersepsi Jaringan AJAX + Database Real (MySQL 58 & MongoDB 106) + Audit Delta Log SUT via SSH (115).
  - **Zero False Positive Protocol**: Strict assertions berlandaskan data aktual yang terverifikasi (fail-fast, anti-truncation).

---

## 📂 Struktur Direktori
```text
rf_token_monitoring_ma/
├── sut_profile.yaml          # Spesifikasi profil SUT, target deployment, akun uji, dan regex audit log
├── testcase.csv              # Desain 12 test case terstandarisasi (12 kolom wajib + baris META-SUT)
├── run_tests.sh              # Runner utama Robot Framework (symlink ke scripts/run_tests.sh)
├── run_headed.sh             # Shortcut runner mode foreground/headed dengan HUD overlay
├── run_poc_journey.sh        # Runner perjalanan uji PoC
├── automation/               # Injected HUD & Spotlight visual runner
│   └── spotlight_hud_runner.py
├── libraries/                # Custom Python test libraries & listeners
│   ├── TokenMonitoringLibrary.py   # Driver utama Playwright, DB MySQL, MongoDB, SSH delta log, network interceptor
│   ├── CsvListener.py              # Listener resmi untuk auto-update 12 kolom testcase.csv
│   ├── LogHelper.py                # Standardized chunked logging (_log_chunked) anti-truncation
│   ├── SutRemoteLogLibrary.py      # SSH log baseline & delta collector
│   └── mock_events_queue.py        # Thread-safe queue helper
├── resources/                # Resource & Clean BDD Keyword Definitions
│   └── keywords/
│       └── token_monitoring_keywords.robot
├── tests/                    # File suite pengujian Robot Framework
│   └── test_token_monitoring_web.robot
├── scripts/                  # Shell runner scripts & static audit quality gates
│   ├── check_duplicate_keywords.sh
│   ├── check_keyword_collision.sh
│   ├── check_missing_keywords.sh
│   ├── run_tests.sh
│   ├── run_headed.sh
│   └── run_poc_journey.sh
├── tools/                    # Tool generator laporan Word (.docx)
│   └── generate_summary_docx.py
├── docs/                     # Dokumentasi spesifikasi CRD
│   └── CRD_PB192644862601YA_PB192644872602YA.txt
├── README.md                 # Dokumentasi proyek otomasi QA
└── .gitignore                # File ignores (results, screenshots, pycache)
```

---

## 🚀 Cara Menjalankan Pengujian (Execution Guide)

### 1. Prasyarat Lingkungan
Pastikan dependensi berikut sudah terpasang pada mesin penguji:
- **Python**: Versi 3.10+
- **Robot Framework**: Versi 5.0.1+
- **Playwright**: Versi 1.40+ beserta browser Chromium
- **Library Python**: `pymysql`, `pymongo`, `paramiko`
- **Variabel Lingkungan (Opsional jika ingin override kredensial)**:
  ```bash
  export MA_AUTH_PASSWORD="<password_web_ui>"     # Default: jatis123
  export MA_MYSQL_PASSWORD="<password_mysql>"     # Default: jatis123
  export MA_MONGO_PASSWORD="<password_mongo>"     # Default: mongoadmin
  export MA_SSH_PASSWORD="<password_ssh_root>"    # Default: sit110jatis123new
  ```

---

### 2. Menjalankan Seluruh Suite Pengujian (Headless Mode)
Jalankan skrip runner utama dari dalam direktori `rf_token_monitoring_ma`:
```bash
cd /home/gunawan/Jamob/2026/PB192644862601YA_PB192644872602YA/rf_token_monitoring_ma
./run_tests.sh
```
*Skrip ini otomatis mengaktifkan flag anti-truncation `--maxassignlength 0`, memuat library path, mendaftarkan `CsvListener.py`, dan mengeksekusi 12 test case secara headless di background.*

---

### 3. Menjalankan Mode Live Watch (Foreground / Headed Mode)
Untuk melihat browser Chromium terbuka secara nyata di layar, lengkap dengan animasi **Injected HUD Overlay & Spotlight Box**:
```bash
./run_headed.sh
```
*Atau menggunakan argumen:*
```bash
./run_tests.sh --headed
```

---

### 4. Menjalankan Test Case Spesifik (Filter by Name / Tag)
Gunakan flag `-t` (*test name pattern*) atau `-i` (*include tag*):

- **Menjalankan 1 Test Case Tertentu (misal: TC-001 Login Saja)**:
  ```bash
  ./run_tests.sh -t "TC-001*"
  ```

- **Menjalankan Verifikasi Tab Insight (TC-002)**:
  ```bash
  ./run_tests.sh -t "TC-002*"
  ```

- **Menjalankan Lebih dari 1 Test Case Spesifik**:
  ```bash
  ./run_tests.sh -t "TC-003*" -t "TC-004*"
  ```

- **Menjalankan Skenario Berdasarkan Prioritas Tag**:
  ```bash
  # Hanya skenario prioritas P0 (Critical)
  ./run_tests.sh -i P0

  # Hanya skenario prioritas P1 (High)
  ./run_tests.sh -i P1
  ```

---

### 5. Menjalankan Skrip Audit Kualitas Statis (Gate 1 Quality Check)
Sebelum commit atau eksekusi formal, jalankan skrip audit statis untuk memastikan tidak ada duplikasi keyword, rekursi, atau keyword yang hilang:
```bash
# 1. Cek duplikasi keyword antar resource
./scripts/check_duplicate_keywords.sh

# 2. Cek benturan nama keyword (rekursi / collision)
./scripts/check_keyword_collision.sh

# 3. Cek pemanggilan keyword yang belum terdefinisi
./scripts/check_missing_keywords.sh
```

---

### 6. Menjalankan Melalui Symlink Global Robot
Suite otomasi ini telah terhubung ke direktori terpusat `/home/gunawan/Jamob/Robot/rf_token_monitoring_ma`. Anda dapat menjalankannya langsung dari sana:
```bash
cd /home/gunawan/Jamob/Robot/rf_token_monitoring_ma
./run_tests.sh
```

---

## 📊 Hasil Pengujian & Laporan (Test Evidence)

Setelah pengujian selesai, seluruh artefak hasil pengujian otomatis disimpan di:
1. **`results/log.html`**: Detail trace log lengkap per langkah, mencakup snapshot request, response, perbandingan data SQL, dan delta log SUT (bebas dari pemotongan teks).
2. **`results/report.html`**: Ringkasan visual metrik kelulusan test suite.
3. **`testcase.csv`**: File matrix pengujian 12 kolom yang otomatis diperbarui oleh `libraries/CsvListener.py` setelah setiap test selesai, memuat:
   - Kolom `Status` terisi `PASS` / `FAIL`.
   - Kolom `Actual Output` terisi deskripsi hasil nyata yang terbukti di UI & API.
   - Kolom `Log` terisi timestamp eksekusi, ringkasan bukti kueri SQL, dan status HTTP/SUT log.

---

## 🔒 Protokol Keamanan Kredensial & Token Masking
- **Kredensial Sensitif**: Password akun pengujian tidak disimpan secara hardcoded dalam repositori publik. Seluruh kredensial menggunakan mekanisme environment injection dengan fallback terenkapsulasi.
- **Masking Token JWT**: Sesuai protokol pengujian sesi (TC-009), token JWT yang ditangkap selama siklus hidup pengujian wajib disamarkan (*masked*) pada seluruh log dan report Robot Framework (`eyJhbGciOi...***`) untuk mencegah kebocoran kredensial sesi.
