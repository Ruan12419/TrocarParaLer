from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from models.livros_model import *

class Usuarios(db.Model):
    __tablename__ = 'usuarios'
    id_usuarios = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    data_nasc = db.Column(db.String(80), nullable=False)
    sexo = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(45), nullable=False)

    def set_password(self, password):
        self.senha = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.senha, password)


class Estado_Livros(db.Model):
    __tablename__ = "estado_livros"
    id_estado_livros = db.Column(db.Integer, primary_key=True)
    estado = db.Column(db.String(45), nullable=False)
    tempo_compra = db.Column(db.String(45), nullable=False)
    motivo_troca = db.Column(db.String(45), nullable=False)
    opiniao_livro = db.Column(db.String(45), nullable=False)
    usuarios_id_usuarios = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuarios'), nullable=False)
    livros_id_livros = db.Column(db.Integer, db.ForeignKey('livros.id_livros'), nullable=False)
