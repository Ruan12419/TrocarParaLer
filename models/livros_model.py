from app import db

class Livros(db.Model):
    __tablename__ = 'livros'
    id_livros = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(15), nullable=False)
    titulo = db.Column(db.String(120), nullable=False)
    sinopse = db.Column(db.String(5000), nullable=True)
    ano_publicacao = db.Column(db.Integer, nullable=False)
    capa = db.Column(db.String(5000), nullable=True)
    idioma = db.Column(db.String(6), nullable=True)
    edicao = db.Column(db.String(45), nullable=True)
