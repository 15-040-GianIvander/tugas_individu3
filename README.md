# Product Review Analyzer

Aplikasi full-stack untuk menganalisis review produk menggunakan **Hugging Face Sentiment Analysis** dan **Google Gemini Key Point Extraction**.  
Hasil analisis ditampilkan pada **frontend React** dan disimpan ke database **PostgreSQL**.

---

## ✨ Fitur Aplikasi

- 📝 User dapat memasukkan review produk (teks)
- 😊 Analisis sentimen (positive / negative / neutral) menggunakan Hugging Face API
- 🔍 Ekstraksi poin-poin penting menggunakan Google Gemini
- 🗂 Menyimpan hasil analisis ke database PostgreSQL
- 💻 Menampilkan daftar hasil analisis di frontend React
- ⚡ Memiliki loading state dan error handling
- 🔗 Backend terhubung ke frontend melalui REST API

---

## 📁 Struktur Folder Project

```
tugas_individu3/
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── services/
│   │   ├── sentiment.py
│   │   └── keypoints.py
│   ├── requirements.txt
│   ├── .env.example
│   └── README_BACKEND.md
│
├── frontend/
│   ├── index.html
│   ├── package.json
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       └── styles.css
│
└── README.md
```

---

## 🚀 Teknologi yang Digunakan

### **Backend**
- FastAPI
- SQLAlchemy ORM
- PostgreSQL
- Hugging Face API
- Google Gemini API
- Uvicorn (server)

### **Frontend**
- React JS
- Vite
- Axios

---

# 🛠 Instalasi Backend

## 1. Masuk ke folder backend

```bash
cd backend
```

## 2. Buat virtual environment & aktifkan

### PowerShell
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## 3. Install dependency backend

```bash
pip install -r requirements.txt
```

## 4. Buat file `.env`

Salin dari `.env.example`:

```bash
cp .env.example .env
```

Isi file `.env`:

```env
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/reviewdb
HF_API_KEY=your_huggingface_api_key
GEMINI_API_KEY=your_gemini_api_key
```

Jika ingin pakai SQLite:

```env
DATABASE_URL=sqlite:///./test.db
```

## 5. Jalankan backend

```bash
python -m uvicorn main:app --reload
```

Backend berjalan pada:
👉 http://localhost:8000

---

# 🔌 Dokumentasi API

## **POST /api/analyze-review**
Menganalisis review baru dan menyimpan hasilnya.

### Request Body
```json
{
  "text": "Produk ini bagus sekali, kualitasnya mantap!"
}
```

### Response
```json
{
  "id": 1,
  "text": "Produk ini bagus sekali, kualitasnya mantap!",
  "sentiment": "positive",
  "key_points": "- kualitas bagus\n- pengiriman cepat\n- recommended"
}
```

---

## **GET /api/reviews**
Mengambil semua review yang sudah disimpan.

### Response

```json
[
  {
    "id": 1,
    "text": "Produk bagus!",
    "sentiment": "positive",
    "key_points": "- kualitas baik\n- harga terjangkau"
  }
]
```

---

# 🖥 Instalasi Frontend

## 1. Masuk ke folder frontend

```bash
cd frontend
```

## 2. Install dependency frontend

```bash
npm install
```

## 3. Jalankan frontend

```bash
npm run dev
```

Frontend berjalan pada:
👉 http://localhost:5173

---

# ⚠ Error Handling & Loading State

### Backend:
- Jika API Hugging Face error → fallback sentiment otomatis
- Jika API Gemini error → fallback keypoint otomatis
- Jika database gagal → mengembalikan HTTP 500

### Frontend:
- Menampilkan loading saat analisis berjalan
- Disable tombol selama proses
- Alert jika terjadi error jaringan/API

---

# 📸 Screenshot (Opsional)
Tambahkan screenshot berikut untuk laporan:
- Tampilan frontend <img width="1918" height="1070" alt="Screenshot 2025-12-12 221814" src="https://github.com/user-attachments/assets/8b87822e-edd3-4f10-a56a-d686680d6d03" />

- Postman test <img width="1910" height="1194" alt="Screenshot 2025-12-12 200146" src="https://github.com/user-attachments/assets/9470f868-e98a-4238-8101-f05fa401af33" />

- Tampilan tabel PostgreSQL <img width="1470" height="385" alt="image" src="https://github.com/user-attachments/assets/516e83fe-a7a1-49dd-b041-50556255f09d" />

