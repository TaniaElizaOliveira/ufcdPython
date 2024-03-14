from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3 as sql

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    with sql.connect("form_db.db") as con:
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM users")
        data = cur.fetchall()
    return render_template("index.html", datas=data)

@app.route("/add_user", methods=["POST", "GET"])
def add_user():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        modalidade = request.form["modalidade"]
        endereco = request.form["endereco"]
        cidade = request.form["cidade"]
        
        with sql.connect("form_db.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO users(NOME, EMAIL, MODALIDADE, ENDERECO, CIDADE) VALUES (?, ?, ?, ?, ?)",
                        (nome, email, modalidade, endereco, cidade))
            con.commit()
        flash("Dados Cadastrados", "success")
        return redirect(url_for("index"))
    return render_template("add_user.html")

@app.route("/edit_user/<string:id>", methods=["POST", "GET"])
def edit_user(id):
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        modalidade = request.form["modalidade"]
        endereco = request.form["endereco"]
        cidade = request.form["cidade"]
        
        with sql.connect("form_db.db") as con:
            cur = con.cursor()
            cur.execute("UPDATE users SET NOME=?, EMAIL=?, MODALIDADE=?, ENDERECO=?, CIDADE=? WHERE ID=?",
                        (nome, email, modalidade, endereco, cidade, id))
            con.commit()
        flash("Dados Atualizados", "success")
        return redirect(url_for("index"))
    with sql.connect("form_db.db") as con:
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE ID=?", (id,))
        data = cur.fetchone()
    return render_template("edit_user.html", datas=data)

@app.route("/delete_user/<string:id>", methods=["GET"])
def delete_user(id):
    with sql.connect("form_db.db") as con:
        cur = con.cursor()
        cur.execute("DELETE FROM users WHERE id=?", (id,))
        con.commit()
    flash("Dados Deletados", "warning")
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.secret_key = "admin123"
    app.run(debug=True)
