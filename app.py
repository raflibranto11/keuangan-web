from flask import Flask, render_template, request, redirect
import csv
import os

app = Flask(__name__)
FILE = "data_keuangan.csv"


def init_file():
    if not os.path.exists(FILE):
        with open(FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["keterangan", "jumlah", "tipe"])


def read_data():
    data = []
    total = 0

    with open(FILE) as f:
        reader = csv.DictReader(f)
        for row in reader:
            jumlah = int(row["jumlah"])

            if row["tipe"] == "income":
                total += jumlah
            else:
                total -= jumlah

            data.append(row)

    return data, total


@app.route("/")
def index():
    data, total = read_data()
    return render_template("index.html", data=data, total=total)


@app.route("/add", methods=["POST"])
def add():
    ket = request.form["ket"]
    jumlah = request.form["jumlah"].replace(".", "").replace(",", "")
    tipe = request.form["tipe"]

    with open(FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([ket, jumlah, tipe])

    return redirect("/")

@app.route("/hapus/<int:index>")
def hapus(index):
    data = baca_data()

    if 0 <= index < len(data):
        data.pop(index)
        simpan_data(data)

    return redirect("/")


init_file()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
