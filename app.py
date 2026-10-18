import os
import time

import pymysql
from flask import Flask, jsonify, redirect, render_template, request, url_for

app = Flask(__name__)

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "db"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "appuser"),
    "password": os.getenv("DB_PASSWORD", "apppass"),
    "database": os.getenv("DB_NAME", "praktikum"),
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor,
}


def get_connection(retries=20, delay=3):
    """Koneksi ke MySQL. Mencoba ulang karena database butuh waktu untuk siap."""
    last_error = None
    for _ in range(retries):
        try:
            return pymysql.connect(**DB_CONFIG)
        except pymysql.MySQLError as exc:
            last_error = exc
            time.sleep(delay)
    raise last_error


def init_db():
    """Buat tabel catatan jika belum ada."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS catatan (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    judul VARCHAR(100) NOT NULL,
                    isi TEXT,
                    dibuat_pada TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
        conn.commit()
    finally:
        conn.close()


@app.route("/", methods=["GET"])
def index():
    conn = get_connection(retries=3, delay=1)
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, judul, isi, dibuat_pada FROM catatan ORDER BY id DESC")
            rows = cur.fetchall()
    finally:
        conn.close()
    return render_template("index.html", catatan=rows, db_host=DB_CONFIG["host"])


@app.route("/tambah", methods=["POST"])
def tambah():
    judul = request.form.get("judul", "").strip()
    isi = request.form.get("isi", "").strip()
    if judul:
        conn = get_connection(retries=3, delay=1)
        try:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO catatan (judul, isi) VALUES (%s, %s)", (judul, isi))
            conn.commit()
        finally:
            conn.close()
    return redirect(url_for("index"))


@app.route("/hapus/<int:catatan_id>", methods=["POST"])
def hapus(catatan_id):
    conn = get_connection(retries=3, delay=1)
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM catatan WHERE id = %s", (catatan_id,))
        conn.commit()
    finally:
        conn.close()
    return redirect(url_for("index"))


@app.route("/health")
def health():
    """Dipakai Jenkins untuk memastikan aplikasi dan database hidup."""
    try:
        conn = get_connection(retries=1, delay=0)
        with conn.cursor() as cur:
            cur.execute("SELECT 1 AS ok")
            cur.fetchone()
        conn.close()
        return jsonify(status="ok", database="connected"), 200
    except Exception as exc:  # noqa: BLE001
        return jsonify(status="error", database=str(exc)), 500


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
