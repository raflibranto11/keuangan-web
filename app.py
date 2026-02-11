@app.route("/hapus/<int:index>")
def hapus(index):
    import csv
    from flask import redirect

    rows = []

    # baca file CSV
    with open("data.csv", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    # hapus data sesuai index
    if 0 <= index < len(rows):
        rows.pop(index)

    # simpan ulang
    with open("data.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    return redirect("/")
