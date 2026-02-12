from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "super_secret_key_ganti_ini"

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
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transaksi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL,
            keterangan TEXT NOT NULL,
            jumlah INTEGER NOT NULL,
            tipe TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


@app.route("/register", methods=["GET", "POST"])
def register():
    init_db()

    if request.method == "POST":
        username = request.form.get("username")
        password = generate_password_hash(request.form.get("password"))

        conn = get_db()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
            conn.commit()
        except:
            return "Username sudah ada"

        conn.close()
        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    init_db()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["user"] = username
            return redirect("/")

        return "Login gagal"

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@app.route("/")
def index():
    if "user" not in session:
        return redirect("/login")

    init_db()

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM transaksi WHERE user = ? ORDER BY id DESC",
        (session["user"],)
    )

    rows = cursor.fetchall()

    total = 0
    for row in rows:
        if row["tipe"] == "expense":
            total -= row["jumlah"]
        else:
            total += row["jumlah"]

    conn.close()

    return render_template("index.html", data=rows, total=total, user=session["user"])


@app.route("/tambah", methods=["POST"])
def tambah():
    if "user" not in session:
        return redirect("/login")

    keterangan = request.form.get("keterangan")
    jumlah = int(request.form.get("jumlah"))
    tipe = request.form.get("tipe")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO transaksi (user, keterangan, jumlah, tipe) VALUES (?, ?, ?, ?)",
        (session["user"], keterangan, jumlah, tipe)
    )

    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/hapus/<int:id>")
def hapus(id):
    if "user" not in session:
        return redirect("/login")

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM transaksi WHERE id = ? AND user = ?",
        (id, session["user"])
    )

    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
