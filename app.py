from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3 as sql
from login_database import create_login_tables

app = Flask(__name__)
app.secret_key = "admin123"

# Chamar a função para criar as tabelas de login
create_login_tables()

# Função para verificar o login do usuário
def verify_login(username, password):
    with sql.connect("login_db.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM ATHLETES WHERE USERNAME=? AND PASSWORD=?", (username, password))
        user = cur.fetchone()
        if user:
            return user, "athlete"
        else:
            cur.execute("SELECT * FROM COACHES WHERE USERNAME=? AND PASSWORD=?", (username, password))
            user = cur.fetchone()
            if user:
                return user, "coach"
            else:
                return None, None

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user, user_type = verify_login(username, password)
        if user:
            flash("Login bem-sucedido!", "success")
            return redirect(url_for("index"))
        else:
            flash("Nome de usuário ou senha incorretos", "error")

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            flash("As senhas não coincidem", "error")
            return redirect(url_for("register"))

        # Verificar se o usuário já existe
        with sql.connect("login_db.db") as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM ATHLETES WHERE USERNAME=?", (username,))
            existing_user = cur.fetchone()
            if existing_user:
                flash("Nome de usuário já em uso", "error")
                return redirect(url_for("register"))
            else:
                cur.execute("INSERT INTO ATHLETES (USERNAME, PASSWORD) VALUES (?, ?)", (username, password))
                con.commit()
                flash("Usuário cadastrado com sucesso", "success")
                return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/")
def redirect_to_login():
    return redirect(url_for("login"))

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
    app.run(debug=True)
