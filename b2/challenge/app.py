from flask import Flask, request, redirect, url_for
import sqlite3

app = Flask(__name__)
database = 'database.db'

@app.route('/')
def index():
    id = request.args.get('id')
    if id is None:
        return redirect(url_for('index', id=1))
    with sqlite3.connect(database) as con:
        cur = con.cursor()
        try:
            cur.execute('SELECT * FROM mytable WHERE id='+id)
        except sqlite3.OperationalError:
            return 'Error'
        return 'What did that query return? It is a mystery ¯\_(ツ)_/¯'