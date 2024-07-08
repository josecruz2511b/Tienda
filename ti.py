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


        # Guardar en la base de datos si las validaciones son correctas
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

        # Actualizar en la base de datos si las validaciones son correctas
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE Productos SET nombre = ?, stock = ?, precio = ? WHERE id = ?',
                       (nombre, stock, precio, id))
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


# Funciones y rutas para empleados

@app.route('/empleados')
def empleados_index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT Empleados.*, Roles.nombre as rol FROM Empleados JOIN Roles ON Empleados.rol_id = Roles.id')
    empleados = cursor.fetchall()
    conn.close()
    return render_template('empleados/index.html', empleados=empleados)


@app.route('/empleados/add', methods=['GET', 'POST'])
def add_empleado():
    if request.method == 'POST':
        nombre = request.form['nombre']
        ap = request.form['ap']
        am = request.form['am']
        usuario = request.form['usuario']
        email = request.form['email']
        contraseña = request.form['contraseña']
        rol_id = request.form['rol_id']


        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO Empleados (nombre, ap, am, usuario, email, contraseña, rol_id) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (nombre, ap, am, usuario, email, contraseña, rol_id))
        conn.commit()
        conn.close()
        return redirect(url_for('empleados_index'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Roles')
    roles = cursor.fetchall()
    conn.close()
    return render_template('empleados/add.html', roles=roles)


@app.route('/empleados/edit/<int:id>', methods=['GET', 'POST'])
def edit_empleado(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Empleados WHERE id = ?', (id,))
    empleado = cursor.fetchone()
    if request.method == 'POST':
        nombre = request.form['nombre']
        ap = request.form['ap']
        am = request.form['am']
        usuario = request.form['usuario']
        email = request.form['email']
        contraseña = request.form['contraseña']
        rol_id = request.form['rol_id']



        cursor.execute(
            'UPDATE Empleados SET nombre = ?, ap = ?, am = ?, usuario = ?, email = ?, contraseña = ?, rol_id = ? WHERE id = ?',
            (nombre, ap, am, usuario, email, contraseña, rol_id, id))
        conn.commit()
        conn.close()
        return redirect(url_for('empleados_index'))

    cursor.execute('SELECT * FROM Roles')
    roles = cursor.fetchall()
    conn.close()
    return render_template('empleados/edit.html', empleado=empleado, roles=roles)

@app.route('/empleados/delete/<int:id>', methods=['POST'])
def delete_empleado(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Empleados WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('empleados_index'))

if __name__ == '__main__':
    app.run(debug=True)
