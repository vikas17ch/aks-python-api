from fastapi import FastAPI
import psycopg2
import os

app = FastAPI(title="Vikas User Manager")

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
def home():
    return {
        "status": "Online 🚀",
        "commands": {
            "View Users": "/users",
            "Add User": "/add?name=Vikas",
            "Delete User": "/delete?id=1"
        }
    }

# NEW: Add a user via GET (Easy for browser testing)
@app.get("/add")
def add_user(name: str):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name) VALUES (%s) RETURNING id;", (name,))
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return {"message": f"User {name} added with ID {new_id} ✅"}

# NEW: Delete a user by ID
@app.get("/delete")
def delete_user(id: int):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id = %s;", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return {"message": f"User ID {id} deleted 🗑️"}

@app.get("/users")
def get_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, created_at FROM users ORDER BY id ASC;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return {"database_records": rows}