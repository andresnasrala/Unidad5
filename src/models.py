from __main__ import app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy(app)

#Modelado de clases a partir de la base de datos con sus respectivas tablas.
class Preceptor(db.Model):
    __tablename__ = "preceptor"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    apellido = db.Column(db.String(80), nullable=False)
    correo = db.Column(db.String(80), unique=True, nullable=False)
    clave = db.Column(db.String(80), nullable=True)
    cursos = db.relationship("Curso", backref="preceptor", cascade="all, delete-orphan") #define una relación de uno a muchos


class Curso(db.Model):
    __tablename__ = 'curso'
    id = db.Column(db.Integer, primary_key=True)
    anio = db.Column(db.Integer, nullable=False)
    division = db.Column(db.Integer, nullable=False)
    idpreceptor = db.Column(db.Integer, db.ForeignKey('preceptor.id'), nullable=False)
    estudiantes = db.relationship('Estudiante', backref='curso', cascade="all, delete-orphan")

class Estudiante(db.Model):
    __tablename__ = 'estudiante'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    apellido = db.Column(db.String(80), nullable=False)
    dni = db.Column(db.String(80), nullable=False)
    idcurso = db.Column(db.Integer, db.ForeignKey('curso.id'), nullable=False)
    idpadre = db.Column(db.Integer, db.ForeignKey('padre.id'))
    asistencias = db.relationship('Asistencia', backref='estudiante', cascade="all, delete-orphan") 

class Asistencia(db.Model):
    __tablename__ = 'asistencia'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    codigoclase = db.Column(db.Integer, nullable=False)
    asistio = db.Column(db.String(1), nullable=False)
    justificacion = db.Column(db.String(80), nullable=True)
    idestudiante = db.Column(db.Integer, db.ForeignKey('estudiante.id'), nullable=False)

class Padre(db.Model):
    __tablename__ = 'padre'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    apellido = db.Column(db.String(80), nullable=False)
    correo = db.Column(db.String(80), unique=True, nullable=False)
    clave = db.Column(db.String(80), nullable=True)
    estudiantes = db.relationship('Estudiante', backref='padre', cascade="all, delete-orphan")

with app.app_context():
    db.create_all()