from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3 as sql

app = Flask(__name__)
app.secret_key = "admin123"

# Função para criar as tabelas de login
def create_login_tables():
    con = sql.connect('login_db.db')
    cur = con.cursor()

    cur.execute('DROP TABLE IF EXISTS athletes')
    sql_athletes = '''
    CREATE TABLE IF NOT EXISTS "ATHLETES" (
        "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
        "USERNAME" TEXT,
        "PASSWORD" TEXT,
        "NAME" TEXT,
        "EMAIL" TEXT,
        "SPORT" TEXT
    )
    '''
    cur.execute(sql_athletes)

    cur.execute('DROP TABLE IF EXISTS coaches')
    sql_coaches = '''
    CREATE TABLE IF NOT EXISTS "COACHES" (
        "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
        "USERNAME" TEXT,
        "PASSWORD" TEXT,
        "NAME" TEXT,
        "EMAIL" TEXT,
        "SPECIALTY" TEXT
    )
    '''
    cur.execute(sql_coaches)

    con.commit()
    con.close()

# Chamada para criar as tabelas de login
create_login_tables()

# Restante do seu código Flask
@app.route("/login")
def login():
    return render_template("login.html")

# Outras rotas e funções aqui...

if __name__ == '__main__':
    app.run(debug=True)
