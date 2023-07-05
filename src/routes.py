from __main__ import app
import hashlib
from .models import db, Padre, Preceptor, Estudiante, Curso, Asistencia
from flask import request, render_template, session, redirect, url_for
from datetime import datetime

#Inicio de sesión 
@app.route('/', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form['email']
        contraseña = request.form['password']
        tipo = request.form['user_type']

        user = verificar_usuario(email, contraseña, tipo)

        if user:
            session['user_id'] = user.id
            session['user_type'] =tipo
            return redirect(url_for('home'))
        
        else:
            return render_template('mensaje.html', mensaje="Algun dato ingresado es incorrecto", tipo="login")
        
    return render_template('login.html')

#panel de control 

@app.route('/home')
def home():

    tipo_usuario = session.get('user_type', None) 
    preceptor_actual = None
    cursos = None

    if tipo_usuario == 'preceptor':
        preceptor_actual = Preceptor.query.get(session['user_id'])
        cursos = preceptor_actual.cursos
    
    elif tipo_usuario == 'padre':
        return render_template('mensaje.html', mensaje="Espacio para funciones del padre", tipo="login")

    return render_template('home.html', cursos=cursos)

@app.route('/logout')
def logout():

    session.pop('user_id', None)
    session.pop('user_type', None)

    return redirect(url_for('login'))

def codificar_contraseña(contraseña):
    return hashlib.md5(bytes(contraseña, encoding='utf-8')).hexdigest()

def verificar_usuario(email, contraseña, tipo):
    user = None

    if tipo == 'preceptor':
        user = db.session.query(Preceptor).filter_by(correo=email).first()

    elif tipo == 'padre':
        user = db.session.query(Padre).filter_by(correo=email).first()

    if user and user.clave == codificar_contraseña(contraseña):
        return user
    
    return None

@app.route('/asistencia', methods=['GET', 'POST'])
def asistencia():

    preceptor = Preceptor.query.get(session['user_id'])
    curso_id = request.args.get('curso_id', None)
    curso = Curso.query.filter_by(id=curso_id, idpreceptor=preceptor.id).first()
    estudiantes_con_asistencia = set()
    
    if request.method == 'POST':
        clase = int(request.form['clase'])
        fecha = request.form['fecha']
        fecha_objeto = datetime.strptime(fecha, "%Y-%m-%d")

        verificar_asistencia = Asistencia.query\
            .join(Estudiante)\
            .filter(
                Estudiante.idcurso == curso_id,
                Asistencia.fecha == fecha_objeto,
                Asistencia.codigoclase == clase
            )\
            .first()
        
        if verificar_asistencia is not None:
            return render_template("mensaje.html", mensaje="Ya existe una asistencia registrada", tipo="")
        
        else:
            
            for estudiante in curso.estudiantes:
                if estudiante.id in estudiantes_con_asistencia:
                    continue
                else:
                    asistencia = request.form.get(f'asistencia_{estudiante.id}') 
                    justificacion = request.form.get(f'justificacion_{estudiante.id}', '')
                    registro_asistencia = Asistencia(
                        idestudiante=estudiante.id,
                        fecha= fecha_objeto,
                        codigoclase=clase,
                        asistio=asistencia,
                        justificacion=justificacion if asistencia == 'n' else ''
                    )

                    db.session.add(registro_asistencia)
                    db.session.commit()
                    estudiantes_con_asistencia.add(estudiante.id)
                return render_template("mensaje.html", mensaje="Asistencia registrada con exito", tipo="")

    estudiantes = Estudiante.query.filter_by(idcurso=curso_id).order_by(Estudiante.nombre, Estudiante.apellido).all()
    return render_template('asistencia.html', curso=curso, estudiantes=estudiantes)

@app.route('/informe', methods=['GET'])
def informe():

    preceptor = Preceptor.query.get(session['user_id'])
    if not preceptor:
        return redirect(url_for('login'))

    curso_id = request.args.get('curso_id', None)
    estudiantes = Estudiante.query.filter_by(idcurso=curso_id).order_by(Estudiante.nombre, Estudiante.apellido).all()
    informe = []
    
    for estudiante in estudiantes:
        asistencias = Asistencia.query.filter_by(idestudiante=estudiante.id).all()

        a_p = a_a_j = a_a_i = 0
        e_p = e_a_j = e_a_i = 0

        for asistencia in asistencias:
            if asistencia.codigoclase == 1:
                if asistencia.asistio == 's':
                    a_p += 1
                elif asistencia.asistio == 'n':
                    if asistencia.justificacion:
                        a_a_j += 1
                    else:
                        a_a_i += 1
                        
            elif asistencia.codigoclase == 2:
                if asistencia.asistio == 's':
                   e_p += 1
                elif asistencia.asistio == 'n':
                    if asistencia.justificacion:
                        e_a_j += 1
                    else:
                        e_a_i += 1

        total = a_a_i + a_a_j + (
            e_a_i + e_a_j) / 2
        
        informe.append({
            'estudiante': estudiante,
            'aula_presente': a_p,
            'aula_ausente_justificada': a_a_j,
            'aula_ausente_injustificada': a_a_i,
            'edu_fisica_presente':e_p,
            'edu_ausente_justificada': e_a_j,
            'edu_ausente_injustificada': e_a_i,
            'total': total
        })

    return render_template('informe.html', informe=informe)
