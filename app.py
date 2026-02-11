from flask import Flask, render_template, request, redirect
import csv
import os

app = Flask(__name__)

FILE = "data.csv"


# ========================
# helper: pastikan file ada
# ========================
def ensure_file():
    if not os.path.exists(FILE):
        open(FILE, "w").close()


# ========================
# HOME (lihat data)
# ========================
@app.route("/")
def index():
    ensure_file()

    rows = []
    with open(FILE, newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    return render_template("index.html", data=rows)


# ========================
# TAMBAH DATA
# ========================
@app.route("/tambah", methods=["POST"])
def tambah():
    ensure_file()

    ket = request.form["keterangan"]
    jumlah = request.form["jumlah"]
    tipe = request.form["tipe"]

    # ubah jadi minus kalau pengeluaran
