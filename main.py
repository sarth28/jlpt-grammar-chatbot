import os
import pandas as pd
from sqlalchemy import create_engine, text
from fastapi import FastAPI
import mysql.connector
from sentence_transformers import SentenceTransformer
from openai import OpenAI
import numpy as np
from dotenv import load_dotenv
#following line is frontend based:
from fastapi.middleware.cors import CORSMiddleware

load_dotenv() # Reads .env and sets env variables

DB_PASSWORD = os.getenv("DB_PASSWORD")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# 1. Clean the data (same as before)
df = pd.read_csv('JLPT.csv', header=None)
df = df.iloc[:, [0, 2, 3, 4]] 
df.columns = ['level', 'grammar_point', 'romaji', 'meaning']

# FIX: add id column so SQL query works
df.reset_index(inplace=True)
df.rename(columns={"index": "id"}, inplace=True)

# 2. Connect to MySQL 
# Format: mysql+mysqlconnector://[user]:[password]@[host]/[database]
# Connect to MySQL server (no database selected yet)

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=DB_PASSWORD
)

cursor = conn.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS sensei_db")

conn.close()

# 2. Connect to the newly ensured database
engine = create_engine(f'mysql+mysqlconnector://root:{DB_PASSWORD}@localhost/sensei_db')

# 3. Push to MySQL
df.to_sql('grammar_table', engine, if_exists='replace', index=False)

print("MySQL Database successfully populated with JLPT grammar!")


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"], 
    allow_methods=["*"],
    allow_headers=["*"],
)
# 1. Setup
# IBM Course Link: NLP & Word Embeddings (AI Fundamentals)
encoder = SentenceTransformer('all-MiniLM-L6-v2')

# FIX: new OpenAI client + env variable
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=DB_PASSWORD,  # FIXED
        database="sensei_db"
    )

# 2. Pre-load embeddings for semantic search
# In a real internship project, you'd store these in a 'vector' column in MySQL

conn = get_db_connection()
cursor = conn.cursor(dictionary=True)
cursor.execute("SELECT id, grammar_point, meaning FROM grammar_table")
rows = cursor.fetchall()
#meanings = [r['meaning'] for r in rows]
#meanings = [r['meaning'] if r['meaning'] is not None else "" for r in rows]
#encoded_meanings = encoder.encode(meanings)
combined_text = [
    f"{r['grammar_point']} {r['meaning'] if r['meaning'] else ''}"
    for r in rows
]

encoded_meanings = encoder.encode(combined_text)

@app.get("/ask")
async def ask_sensei(question: str):
    # STEP A: Find the right grammar point (Retrieval)
    question_vec = encoder.encode([question])
    question_vec = question_vec.flatten()

    similarities = np.dot(encoded_meanings, question_vec) / (
    np.linalg.norm(encoded_meanings, axis=1) * np.linalg.norm(question_vec) + 1e-8
    )

    #best_match_idx = np.argmax(similarities)
    #context = rows[best_match_idx]
    top_k = 3
    top_indices = np.argsort(similarities)[-top_k:][::-1]

    candidates = [rows[i] for i in top_indices]

    # smarter selection
    context = None
    for c in candidates:
        if c['grammar_point'] in question:
            context = c
            break

    if not context:
        context = candidates[0]

    # STEP B: Generate the "Sensei" response (Generation)
    # IBM Course Link: Empathy & Clarity (Professional Skills/Customer Experience)
    prompt = f"""
    You are a Japanese language teacher.

    IMPORTANT:
    - Only explain the given grammar point.
    - Do NOT introduce or explain any other grammar.

    Student question: {question}

    Grammar point: {context['grammar_point']}
    Meaning: {context['meaning']}

    Explain clearly with:
    - Simple explanation
    - One example sentence (Japanese + English)
    """

    # FIX: updated API call
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": "You are a helpful Japanese tutor."},
                  {"role": "user", "content": prompt}],
        max_tokens=150
    )

    return {
        "sensei_says": response.choices[0].message.content.replace("\\n", "\n"),
        "source_grammar": context['grammar_point']
    }
