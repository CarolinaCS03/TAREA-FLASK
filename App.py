 
#------------------------------------
#EVA CAROLINA CEVALLOS SANCHEZ
#------------------------------------

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL


app = Flask(__name__)

#settings
app.secret_key = 'clave_secreta_segura'

#coneccion de mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'opticatriem'
mysql = MySQL(app)


@app.route('/')
def carolina():
  cur = mysql.connection.cursor()
  cur.execute('SELECT * FROM usuario')
  usuarios = cur.fetchall()
  cur.execute('SELECT * FROM compra')
  compras = cur.fetchall()
  return render_template('index.html', usuarios=usuarios, compras=compras)


@app.route('/add_usuario', methods=['POST'])
def add_usuario():
    if request.method == 'POST':
        Cedula = request.form['Cedula']
        Nombre1 = request.form['Nombre1']
        Nombre2 = request.form['Nombre2']
        Apellido1 = request.form['Apellido1']
        Apellido2 = request.form['Apellido2']
        Telefono = request.form['Telefono']
        Direccion = request.form['Direccion']
        Correo = request.form['Correo']
        tipousuario = request.form['tipousuario']
        cur = mysql.connection.cursor()
        cur.execute('''
            INSERT INTO usuario 
            (Cedula, Nombre1, Nombre2, Apellido1, Apellido2, Telefono, Direccion, Correo, tipoUsuario) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (Cedula, Nombre1, Nombre2, Apellido1, Apellido2, Telefono, Direccion, Correo, tipousuario))
        mysql.connection.commit()
        flash('Se guardo completamente el registro')
        return redirect(url_for('carolina'))
    


@app.route('/add_compra', methods=['POST'])  
def add_compra():
    if request.method == 'POST':
        Distribuidor = request.form['Distribuidor']
        Empresa = request.form['Empresa']
        Descp = request.form['Descp']
        Costo = request.form['Costo']

        cur = mysql.connection.cursor()
        cur.execute('''
            INSERT INTO compra 
            (Distribuidor, Empresa, Descp, Costo) 
            VALUES (%s, %s, %s, %s)
        ''', (Distribuidor, Empresa, Descp, Costo))

        mysql.connection.commit()
        flash('Se guardó completamente la compra')
        return redirect(url_for('carolina'))

    
@app.route('/update_usuario/<int:id>', methods=['POST'])
def update_usuario(id):
    cedula = request.form['Cedula']
    nombre1 = request.form['Nombre1']
    nombre2 = request.form['Nombre2']
    apellido1 = request.form['Apellido1']
    apellido2 = request.form['Apellido2']
    telefono = request.form['Telefono']
    direccion = request.form['Direccion']
    correo = request.form['Correo']
    tipousuario = request.form['tipousuario']

    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE usuario SET
        Cedula=%s, Nombre1=%s, Nombre2=%s, Apellido1=%s,
        Apellido2=%s, Telefono=%s, Direccion=%s, Correo=%s,
        tipoUsuario=%s WHERE id=%s
    """, (cedula, nombre1, nombre2, apellido1, apellido2,
          telefono, direccion, correo, tipousuario, id))
    mysql.connection.commit()
    flash('Usuario actualizado correctamente')
    return redirect(url_for('carolina'))


@app.route('/update_compra/<int:id>', methods=['POST'])
def update_compra(id):
    distribuidor = request.form['Distribuidor']
    empresa = request.form['Empresa']
    descp = request.form['Descp']
    costo = request.form['Costo']

    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE compra SET
        Distribuidor=%s, Empresa=%s, Descp=%s,
        Costo=%s WHERE id=%s
    """, (distribuidor, empresa, descp, costo, id))
    mysql.connection.commit()
    flash('Compra actualizada correctamente')
    return redirect(url_for('carolina'))


       

@app.route('/edit_usuario/<id>')
def get_usuario(id):
  cur = mysql.connection.cursor()
  cur.execute('SELECT * FROM usuario WHERE id = %s', (id,))
  data = cur.fetchall()
  return render_template('edit_usuario.html', usuario = data[0])
 


@app.route('/delete_usuario/<string:id>')
def delete_usuario(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM usuario WHERE id = %s', (id,))
    mysql.connection.commit()
    flash('Usuario eliminado')
    return redirect(url_for('carolina'))


@app.route('/edit_compra/<id>')
def get_compra(id):
  cur = mysql.connection.cursor()
  cur.execute('SELECT * FROM compra WHERE id = %s', (id,))
  data = cur.fetchall()
  return render_template('edit_compra.html', compra = data[0])

@app.route('/delete_compra/<string:id>')
def delete_compra(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM compra WHERE id = %s', (id,))
    mysql.connection.commit()
    flash('Compra eliminada')
    return redirect(url_for('carolina'))

if __name__ == '__main__':
  app.run(port = 5000, debug = True)
