import sqlite3
from flask import Flask, jsonify

app = Flask(__name__)
DB_NAME = "praktikum.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mahasiswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            matakuliah TEXT NOT NULL,
            status TEXT NOT NULL
        )
    ''')
    cursor.execute('SELECT COUNT(*) FROM mahasiswa')
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO mahasiswa (nama, matakuliah, status)
            VALUES ('Shandy Okta Ramadhani', 'Komputasi Awan', 'Berhasil Terhubung ke Database & Docker')
        ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    try:
        init_db()
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('SELECT id, nama, matakuliah, status FROM mahasiswa')
        rows = cursor.fetchall()
        conn.close()

        data = [
            {"id": row[0], "nama": row[1], "matakuliah": row[2], "status": row[3]}
            for row in rows
        ]
        return jsonify({
            "message": "Halo dari Flask + Database SQLite + Docker + Jenkins!",
            "database_connection": "CONNECTED",
            "data_mahasiswa": data
        })
    except Exception as e:
        return jsonify({
            "database_connection": "FAILED",
            "error": str(e)
        }), 500

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
