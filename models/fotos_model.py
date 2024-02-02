from app import db
from models.usuarios_model import *

    
class Fotos(db.Model):
    __tablename__ = "fotos"
    id_fotos = db.Column(db.Integer, primary_key=True)
    foto_base64 = db.Column(db.String(64000), nullable=False)
    caminho = db.Column(db.String(1000), nullable=False)
    estado_livros_id_estado_livros = db.Column(db.Integer, db.ForeignKey("estado_livros.id_estado_livros"), nullable=False)
