import sqlite3 as sql

con = sql.connect('form_db.db')
cur = con.cursor()
cur.execute('DROP TABLE IF EXISTS users')

sql = '''
CREATE TABLE "USERS" (
    "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
    "NOME" TEXT,
    "EMAIL" TEXT,
    "MODALIDADE" TEXT,
    "ENDERECO" TEXT,
    "CIDADE" TEXT
)
'''


cur.execute(sql)
con.commit()
con.close()
