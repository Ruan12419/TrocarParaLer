from app import db
from models.usuarios_model import *
from models.livros_model import *

class Ofertas(db.Model):
    __tablename__ = 'ofertas'
    id_ofertas = db.Column(db.Integer, primary_key=True)
    id_usuario_ofertante = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuarios'), nullable=False)
    id_usuario_receptor = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuarios'), nullable=False)
    id_livro_ofertado = db.Column(db.Integer, db.ForeignKey('livros.id_livros'), nullable=False)
    id_livro_desejado = db.Column(db.Integer, db.ForeignKey('livros.id_livros'), nullable=False)
    status = db.Column(db.String(80), nullable=False)
