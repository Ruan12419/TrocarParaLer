from app import db
from models.livros_model import *

class Editoras(db.Model):
    __tablename__ = "editoras"
    id_editoras = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(45), nullable=False)
    website = db.Column(db.String(5000), nullable=True)

class Editoras_Livro(db.Model):
    __tablename__ = "editoras_has_livros"
    editoras_id_editoras = db.Column(db.Integer, db.ForeignKey("editoras.id_editoras"), primary_key=True, nullable=False)
    livros_id_livros = db.Column(db.Integer, db.ForeignKey("livros.id_livros"), primary_key=True, nullable=False)

