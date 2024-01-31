from app import db
from werkzeug.security import generate_password_hash, check_password_hash

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

class Autores(db.Model):
    __tablename__ = "autores"
    id_autores = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    biografia = db.Column(db.String(5000), nullable=True)

class Autores_Livro(db.Model):
    __tablename__ = "autores_has_livros"
    autores_id_autores = db.Column(db.Integer, db.ForeignKey("autores.id_autores"), primary_key=True, nullable=False)
    livros_id_livros = db.Column(db.Integer, db.ForeignKey("livros.id_livros"), primary_key=True, nullable=False)

class Editoras(db.Model):
    __tablename__ = "editoras"
    id_editoras = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(45), nullable=False)
    website = db.Column(db.String(5000), nullable=True)

class Editoras_Livro(db.Model):
    __tablename__ = "editoras_has_livros"
    editoras_id_editoras = db.Column(db.Integer, db.ForeignKey("editoras.id_editoras"), primary_key=True, nullable=False)
    livros_id_livros = db.Column(db.Integer, db.ForeignKey("livros.id_livros"), primary_key=True, nullable=False)

class Estado_Livros(db.Model):
    __tablename__ = "estado_livros"
    id_estado_livros = db.Column(db.Integer, primary_key=True)
    estado = db.Column(db.String(45), nullable=False)
    tempo_compra = db.Column(db.String(45), nullable=False)
    motivo_troca = db.Column(db.String(45), nullable=False)
    opiniao_livro = db.Column(db.String(45), nullable=False)
    usuarios_id_usuarios = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuarios'), nullable=False)
    livros_id_livros = db.Column(db.Integer, db.ForeignKey('livros.id_livros'), nullable=False)
    
class Fotos(db.Model):
    __tablename__ = "fotos"
    id_fotos = db.Column(db.Integer, primary_key=True)
    foto_base64 = db.Column(db.String(64000), nullable=False)
    caminho = db.Column(db.String(1000), nullable=False)
    estado_livros_id_estado_livros = db.Column(db.Integer, db.ForeignKey("estado_livros.id_estado_livros"), nullable=False)

class Ofertas(db.Model):
    __tablename__ = 'ofertas'
    id_ofertas = db.Column(db.Integer, primary_key=True)
    id_usuario_ofertante = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuarios'), nullable=False)
    id_usuario_receptor = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuarios'), nullable=False)
    id_livro_ofertado = db.Column(db.Integer, db.ForeignKey('livros.id_livros'), nullable=False)
    id_livro_desejado = db.Column(db.Integer, db.ForeignKey('livros.id_livros'), nullable=False)
    status = db.Column(db.String(80), nullable=False)
