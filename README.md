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
- **Cakupan Pengujian**: 12 Test Cases (TC-001 s/d TC-012)
- **Kaidah Utama**:
  - **Clean BDD Murni**: *Zero Dollar Signs* (`${...}`) pada blok `*** Test Cases ***`.
  - **True Web UI Testing**: 100% aksi pemicu bisnis dilakukan melalui antarmuka Web UI.
  - **Multi-Layer Observability**: Verifikasi menyeluruh pada DOM, respons jaringan, MySQL summary table (58), MongoDB (106), dan log BFF JSON via SSH (115).
  - **Zero False Positive Protocol**: Strict assertions berlandaskan data aktual yang terverifikasi.

---

## 📂 Struktur Direktori
```text
rf_token_monitoring_ma/
├── sut_profile.yaml          # Spesifikasi profil SUT, target deployment, akun uji, dan regex audit log
├── testcase.csv              # Desain 12 test case terstandarisasi (12 kolom wajib + baris META-SUT)
├── docs/                     # Dokumentasi spesifikasi CRD
│   └── CRD_PB192644862601YA_PB192644872602YA.txt
├── README.md                 # Dokumentasi proyek otomasi QA
└── .gitignore                # File ignores
```

---

## 🔒 Protokol Keamanan Kredensial & Token Masking
- **Kredensial Sensitif**: Password akun pengujian tidak disimpan dalam repositori publik. Seluruh kredensial diinjeksi via variabel lingkungan:
  ```bash
  export MA_AUTH_PASSWORD="<password_anda>"
  ```
- **Masking Token JWT**: Sesuai protokol pengujian sesi (TC-009), token JWT yang ditangkap selama siklus hidup pengujian wajib disamarkan (*masked*) pada seluruh log dan report Robot Framework (`eyJhbGciOi...***`) untuk mencegah kebocoran kredensial sesi.

---

## 📋 Status Kesiapan QA (Tahap 1 Gate Passed - Ready for RF)
- **Gate 0 (Deployment & Environment Readiness)**: PASSED (HTTP 200 OK pada Web UI & BFF).
- **Gate 1 (Test Analysis & Testcase Design)**: APPROVED (`READY_FOR_RF`) dengan 4-Lapisan Pembuktian (DOM, Network, SQL/DB, Log Contract) dan audit rentang eksplisit SQL serta kontrak zona waktu Asia/Jakarta.
