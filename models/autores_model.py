from app import db
from models.livros_model import *


class Autores(db.Model):
    __tablename__ = "autores"
    id_autores = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    biografia = db.Column(db.String(5000), nullable=True)

class Autores_Livro(db.Model):
    __tablename__ = "autores_has_livros"
    autores_id_autores = db.Column(db.Integer, db.ForeignKey("autores.id_autores"), primary_key=True, nullable=False)
    livros_id_livros = db.Column(db.Integer, db.ForeignKey("livros.id_livros"), primary_key=True, nullable=False)
