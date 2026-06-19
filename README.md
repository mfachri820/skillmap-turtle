# SkillMap AI

SkillMap AI adalah aplikasi Streamlit untuk menjelajah jalur karier berbasis graf semantik dan job posting. Aplikasi ini menggabungkan:

- dataset RDF / TTL untuk job posting dan skill
- Apache Jena Fuseki sebagai backend SPARQL
- OpenRouter AI untuk menerjemahkan input bebas pengguna menjadi skill terstandardisasi
- antarmuka percakapan AI yang membantu merumuskan minat dan jalur karier

## Fitur Utama

- `Search`: masukkan skill, minat, atau pengalaman dengan bahasa sehari-hari dan temukan job posting terkait
- `View Jobs`: lihat koleksi job posting yang tersedia beserta skill yang dibutuhkan
- `AI Assistant`: berdiskusi dengan bot tentang apa yang kamu sukai dan dapatkan saran arah karier
- dukungan pencocokan skill dengan data RDF melalui SPARQL

## Struktur Proyek

- `app.py` - entry point Streamlit
- `config.py` - pengaturan tema dan daftar skill
- `sparql_client.py` - koneksi dan query ke Fuseki
- `services/ai_client.py` - helper OpenRouter AI untuk decode skill
- `ui/` - tampilan Streamlit untuk user, admin, dan assistant
- `data/` - dataset TTL contoh, seperti `career_data.ttl`

## Prasyarat

- Python 3.10+ atau lingkungan Python yang kompatibel
- Apache Jena Fuseki (local server) berjalan dan dataset terpasang
- OpenRouter API key

## Instalasi

1. Buka terminal di folder proyek:

```powershell
cd "e:\CodeToolsD\Semester 6\Semantik Web\skillmap-ai-semweb"
```

2. Siapkan virtual environment (direkomendasikan):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install dependency:

```powershell
pip install -r requirements.txt
```

4. Siapkan file `.env` di root proyek dengan OpenRouter key:

```text
OPENROUTER_API_KEY=your_openrouter_key_here
```

> Jika `.env` hanya berisi kunci saja, `services/ai_client.py` akan tetap membacanya.

5. Pastikan Apache Jena Fuseki berjalan dan dataset `skillmap-ai` tersedia di endpoint:

```text
http://localhost:3030/skillmap-ai/query
```

Jika endpoint atau nama dataset berbeda, perbarui `FUSEKI_ENDPOINT` di `sparql_client.py`.

## Menjalankan Aplikasi

Jalankan Streamlit dari folder `skillmap-ai-semweb`:

```powershell
streamlit run app.py
```

Buka browser ke alamat yang ditampilkan oleh Streamlit, biasanya `http://localhost:8501`.

Jangan lupa untuk menjalankan Fuseki melalui server anda.

```powershell
cd "your directory/apache-jena-fuseki-6.1.0"
.\fuseki-server.bat
```

## Catatan

- `AI Assistant` dibuat untuk berdiskusi tentang apa yang kamu sukai, bukan sekadar mesin pencari job.
- Gunakan input yang berfokus pada ketertarikan, pengalaman, dan aktivitas yang memberi energi.
- Jika Fuseki tidak bisa dihubungi, pastikan servernya menyala dan dataset sudah di-load.

## Author
- 140810230023 | Muhammad Fachri
- 140810230003 | Adelia Felisha

## Troubleshooting

- `ConnectionError` saat mengakses Fuseki: periksa `FUSEKI_ENDPOINT` dan status Fuseki
- AI decoding gagal: pastikan `.env` berisi kunci OpenRouter yang valid
- Jika ingin mengganti port atau dataset Fuseki, edit `sparql_client.py`

---

SkillMap AI dibuat untuk membantu eksplorasi karier dengan pendekatan percakapan dan graf pengetahuan. Selamat mencoba!