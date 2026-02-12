from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

BASE_DIR = os.getcwd()
DB_PATH = os.path.join(BASE_DIR, "database.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transaksi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keterangan TEXT NOT NULL,
            jumlah INTEGER NOT NULL,
            tipe TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def index():
    init_db()

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM transaksi ORDER BY id DESC")
    rows = cursor.fetchall()

    total = 0
    for row in rows:
        if row["tipe"] == "expense":
            total -= row["jumlah"]
        else:
            total += row["jumlah"]

    conn.close()

    return render_template("index.html", data=rows, total=total)


@app.route("/tambah", methods=["POST"])
def tambah():
    keterangan = request.form.get("keterangan")
    jumlah = int(request.form.get("jumlah"))
    tipe = request.form.get("tipe")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO transaksi (keterangan, jumlah, tipe) VALUES (?, ?, ?)",
        (keterangan, jumlah, tipe)
    )

    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/hapus/<int:id>")
def hapus(id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM transaksi WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
