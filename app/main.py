from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import psycopg2
import os

app = FastAPI(title="Vikas User Manager UI")

# 1. Mount the 'static' folder so your HTML/CSS/JS is accessible
# This expects a folder named 'static' to exist in your Docker image
app.mount("/static", StaticFiles(directory="static"), name="static")

# Database connection helper
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database="postgres",
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        sslmode='require'
    )

# 2. Create the table automatically on startup
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

# 3. Serve the UI (Dashboard) at the root URL
@app.get("/")
def read_index():
    return FileResponse('static/index.html')

# 4. API Route: Add a user
@app.get("/add")
def add_user(name: str):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name) VALUES (%s) RETURNING id;", (name,))
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return {"message": f"User {name} added!", "id": new_id}

# 5. API Route: Delete a user
@app.get("/delete")
def delete_user(id: int):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id = %s;", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return {"message": f"User {id} deleted."}

# 6. API Route: List all users
@app.get("/users")
def get_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, created_at FROM users ORDER BY id ASC;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return {"database_records": rows}
# 7. API Route: Search all users
@app.get("/search")
def search_user(name: str):
    conn = get_db_connection()
    cur = conn.cursor()
    # Use ILIKE for case-insensitive searching
    cur.execute("SELECT id, name, created_at FROM users WHERE name ILIKE %s;", (f"%{name}%",))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return {"results": rows}