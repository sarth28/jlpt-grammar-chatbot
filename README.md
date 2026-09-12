#  JLPT Chatbot (Sensei-AI)

A Japanese Language Proficiency Test (JLPT) assistant chatbot built using **FastAPI**, **Streamlit**, and **Sentence Transformers**.
It helps users understand Japanese grammar patterns and provides intelligent responses based on semantic similarity.

---

##  Features

*  Chatbot interface for JLPT queries
*  Semantic search using Sentence Transformers
*  FastAPI backend for handling requests
*  Streamlit frontend for interactive UI
*  MySQL database integration
*  Environment-based configuration using `.env`

---

## 🛠️ Tech Stack

* **Backend:** FastAPI
* **Frontend:** Streamlit
* **Machine Learning:** Sentence Transformers
* **Database:** MySQL
* **Other Tools:** SQLAlchemy, Pandas, NumPy

---

## 📂 Project Structure

```
.
├── main.py            # FastAPI backend
├── app.py             # Streamlit frontend
├── requirements.txt   # Dependencies
├── .env               # Environment variables (not included)
├── jlpt.csv           # Dataset (not included)
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/sarth28/jlpt-grammar-chatbot.git
cd jlpt-grammar-chatbot
```

---

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
# or
source venv/bin/activate  # Mac/Linux
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure environment variables

Create a `.env` file:

```
OPENAI_API_KEY=your_api_key_here
```

---

### 5. Run the backend (FastAPI)

```bash
uvicorn main:app --reload
```

---

### 6. Run the frontend (Streamlit)

```bash
streamlit run app.py
```

---

## ⚠️ Dataset Notice

The dataset (`jlpt.csv`) is **not included** in this repository due to licensing uncertainty.
You may use any publicly available JLPT dataset or create your own.

---

##  Future Improvements

*  Add authentication
*  Deploy on cloud (Streamlit Cloud / Render)
*  Improve NLP accuracy with fine-tuned models

---
