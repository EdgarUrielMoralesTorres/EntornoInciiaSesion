from flask import Flask,render_template,request,redirect,url_for,flash, session


app = Flask(__name__)
app.config['SECRET_KEY']='una_clave_secreta_muy_larga_y_dificil_de_advinar'

USUARIOS_REGISTRADOS = {}

@app.route('/')
def main():
    return render_template('base.html')

@app.route('/animales')
def ani():
    return render_template('animales.html')

@app.route('/Vehiculos')
def vei():
    return render_template('vehiculos.html')

@app.route('/Maravillas')
def mav():
    return render_template('Maravillas.html')

@app.route('/AcercaDe')
def Ace():
    return render_template('AcercaDe.html')

@app.route('/registrate')
def Regi():
    return render_template('registrate.html')

@app.route('/iniciaSes')
def iniciaSes():
    if session.get('logueado'):
        nombre = session.get('usuario', 'Usuario')
        session.clear()
        flash(f'Sesión cerrada correctamente {nombre}', 'success')
        return redirect(url_for('main'))

    return render_template("iniciaSes.html")


@app.route('/validaSes', methods=['GET', 'POST'])
def validaSes():
    if request.method == 'POST':
        email = request.form.get('email', '')
        Contra = request.form.get('Contra', '')

        if not email or not Contra:
            flash('Por favor ingresa un email y contraseña', 'error')

        elif email in USUARIOS_REGISTRADOS:
            usuario = USUARIOS_REGISTRADOS[email]

            if usuario['password'] == Contra:
                session['usuario_email'] = email
                session['usuario'] = usuario['nombre']
                session['logueado'] = True

                return redirect(url_for('main'))
            else:
                flash('Contraseña incorrecta', 'error')
        else:
            flash('Usuario no encontrado', 'error')

    return render_template('iniciaSes.html')


@app.route('/obtenerinfo', methods=("GET", "POST"))
def Obt():
    error = None
    if request.method == "POST":
        NombreCompleto = request.form["NombreCompleto"]
        email = request.form["email"]
        Contra = request.form["Contra"]
        ContraPru = request.form["ContraPru"]
        Año = int(request.form["Año"])

        if Contra != ContraPru:
            error = "Las contraseñas no coinciden"
        elif Año > 2006:
            error = "Eres menor de edad"
        elif email in USUARIOS_REGISTRADOS:
            error = "Este correo ya está registrado"

        if error:
            flash(error, "error")
            return render_template("registrate.html")
        else:
            USUARIOS_REGISTRADOS[email] = {
                'password': Contra,
                'nombre': NombreCompleto,
                'año': Año
            }

            flash(f"Registro exitoso para el usuario: {NombreCompleto}", "success")
            return redirect(url_for("iniciaSes"))

if __name__ == '__main__':
    app.run(debug=True)