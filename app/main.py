from fastapi import FastAPI
import psycopg2
import os

app = FastAPI(title="Vikas Automated API")

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database="postgres",
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        sslmode='require'
    )

@app.on_event("startup")
def startup_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()

@app.get("/")
def read_root():
    return {"message": "Vikas: Senior SRE Automation Complete! 🚀"}

@app.get("/users")
def get_users():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users ORDER BY created_at DESC;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return {"users": rows}
    except Exception as e:
        return {"error": str(e)}