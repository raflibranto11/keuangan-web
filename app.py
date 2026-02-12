from flask import Flask, render_template, request, redirect
import os
import csv

app = Flask(__name__)

BASE_DIR = os.getcwd()
FILE = os.path.join(BASE_DIR, "data.csv")


def ensure_file():
    if not os.path.exists(FILE):
        with open(FILE, "w", newline="") as f:
            pass


@app.route("/")
def index():
    ensure_file()
    rows = []
    total = 0

    with open(FILE, newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    for row in rows:
        try:
            jumlah = int(row[1])
            tipe = row[2]

            if tipe == "expense":
                total -= jumlah
            else:
                total += jumlah

        except:
            pass

    return render_template("index.html", data=rows, total=total)



@app.route("/tambah", methods=["POST"])
def tambah():
    ensure_file()

    ket = request.form.get("keterangan")
    jumlah = int(request.form.get("jumlah"))
    tipe = request.form.get("tipe")

    with open(FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([ket, jumlah, tipe])

    return redirect("/")



@app.route("/hapus/<int:index>")
def hapus(index):
    ensure_file()

    rows = []
    with open(FILE, newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    if 0 <= index < len(rows):
        rows.pop(index)

    with open(FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)