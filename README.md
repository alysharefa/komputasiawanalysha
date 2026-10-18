# Simple App - Praktikum Komputasi Awan (Jenkins + Docker + MySQL)

Aplikasi catatan sederhana (Flask) yang menyimpan data ke database MySQL,
dibangun dan dijalankan otomatis oleh pipeline Jenkins.

## Struktur

```
simple-app/
├── app.py                 # aplikasi Flask + koneksi MySQL
├── templates/index.html   # tampilan web
├── requirements.txt
├── Dockerfile             # image aplikasi
├── docker-compose.yml     # aplikasi + database MySQL
└── Jenkinsfile            # pipeline: Checkout > Build > Docker build > Push > Deploy > Verifikasi
```

## Menjalankan manual (tanpa Jenkins)

```
docker compose up -d --build
```

Buka http://localhost:5000 . Cek kesehatan: http://localhost:5000/health

Menghentikan: `docker compose down` (tambah `-v` untuk menghapus data database).

## Catatan

- Username/password database di `docker-compose.yml` hanya untuk keperluan lab.
- Pada `Jenkinsfile`, ganti `ganti-username` dengan username Docker Hub.
