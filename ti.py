from flask import Flask, render_template, request, redirect, url_for
import pyodbc
from config import Config

app = Flask(__name__)

def get_db_connection():
    conn = pyodbc.connect(Config.CONNECTION_STRING)
    return conn

# Rutas para Productos
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

        # Validar datos
        if not stock.isdigit():
            return "El stock debe ser un número entero", 400
        if not precio.replace('.', '', 1).isdigit():
            return "El precio debe ser un número", 400

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

        # Validar datos
        if not stock.isdigit():
            return "El stock debe ser un número entero", 400
        if not precio.replace('.', '', 1).isdigit():
            return "El precio debe ser un número", 400

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

# Rutas para Empleados
@app.route('/empleados')
def empleados():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT e.id, e.nombre, e.ap, e.am, e.usuario, e.email, r.nombre as rol FROM Empleados e JOIN Roles r ON e.rol_id = r.id')
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
        cursor.execute('INSERT INTO Empleados (nombre, ap, am, usuario, email, contraseña, rol_id) VALUES (?, ?, ?, ?, ?, ?, ?)',
                       (nombre, ap, am, usuario, email, contraseña, rol_id))
        conn.commit()
        conn.close()
        return redirect(url_for('empleados'))
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

    cursor.execute('SELECT * FROM Roles')
    roles = cursor.fetchall()
    conn.close()

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
        cursor.execute('UPDATE Empleados SET nombre = ?, ap = ?, am = ?, usuario = ?, email = ?, contraseña = ?, rol_id = ? WHERE id = ?',
                       (nombre, ap, am, usuario, email, contraseña, rol_id, id))
        conn.commit()
        conn.close()
        return redirect(url_for('empleados'))
    return render_template('empleados/edit.html', empleado=empleado, roles=roles)

@app.route('/empleados/delete/<int:id>', methods=['POST'])
def delete_empleado(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Empleados WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('empleados'))

if __name__ == '__main__':
    app.run(debug=True)

