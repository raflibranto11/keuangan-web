from flask import Flask, render_template, request, redirect
import csv

# WAJIB PALING ATAS
app = Flask(__name__)


# ========================
# ROUTES
# ========================

@app.route("/")
def index():
    rows = []
    with open("data.csv", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    return render_template("index.html", data=rows)


@app.route("/hapus/<int:index>")
def hapus(index):
    rows = []

    with open("data.csv", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    if 0 <= index < len(rows):
        rows.pop(index)

    with open("data.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    return redirect("/")


# ========================
# RUN
# ========================

if __name__ == "__main__":
    app.run(debug=True)
