from flask import Flask, render_template, request, redirect, url_for
import pyodbc
from config import Config

app = Flask(__name__)

def get_db_connection():
    conn = pyodbc.connect(Config.CONNECTION_STRING)
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Productos')
    productos = cursor.fetchall()
    conn.close()
    return render_template('index.html', productos=productos)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        nombre = request.form['nombre']
        stock = request.form['stock']
        precio = request.form['precio']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO Productos (nombre, stock, precio) VALUES (?, ?, ?)', (nombre, stock, precio))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Productos WHERE id = ?', (id,))
    producto = cursor.fetchone()
    conn.close()
    if request.method == 'POST':
        nombre = request.form['nombre']
        stock = request.form['stock']
        precio = request.form['precio']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE Productos SET nombre = ?, stock = ?, precio = ? WHERE id = ?', (nombre, stock, precio, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('edit.html', producto=producto)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Productos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
