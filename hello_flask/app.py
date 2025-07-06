# app.py
from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Example DB function
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS hello (id INTEGER PRIMARY KEY, message TEXT)')
    c.execute('INSERT INTO hello (message) VALUES (?)', ('Hello, Flask!',))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
