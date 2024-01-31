from flask import request, render_template, redirect, url_for, session
from app import app, db
from models import *
from sqlalchemy.orm import aliased
import uuid
import base64
import os



@app.route('/')
def home():
    if 'user_id' in session:
        livros = Livros.query.all()
        return render_template('index.html', livros=livros)
    return render_template('index.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        usuarios = Usuarios.query.filter_by(email=request.form['email']).first()
        if usuarios and usuarios.check_password(request.form['senha']):
            session['user_id'] = usuarios.id_usuarios
            return redirect(url_for("home"))
        else:
            return render_template("login.html", erro="Email ou senha incorreto!")
    return render_template("login.html")

@app.route("/logout", methods=['POST'])
def logout():
    session.pop('user_id', None)
    return redirect(url_for("home"))

@app.route('/cadastrar_usuario', methods=['POST'])
def add_usuario():
    nome = request.form['nome']
    data_nasc = request.form['data_nasc']
    sexo = request.form['sexo']
    email = request.form['email']
    senha = request.form['senha']
    confirma_senha = request.form['confirmacao_senha']
    if senha != confirma_senha:
        return render_template("login.html", erro="As senhas não correspondem!")
    id_usuarios = int(get_uuid(1))
    usuario = Usuarios(id_usuarios=id_usuarios, nome=nome, data_nasc=data_nasc, sexo=sexo, email=email)
    usuario.set_password(senha)
    db.session.add(usuario)
    db.session.commit()
    session['user_id'] = usuario.id_usuarios
    return redirect(url_for("home"))

@app.route("/meus_livros", methods=['GET'])
def meus_livros():
    if 'user_id' in session:
        """
        livros = db.session.query(Livros.id_livros)\
            .join(Estado_Livros, Livros.id_livros == Estado_Livros.livros_id_livros)\
            .filter(Estado_Livros.usuarios_id_usuarios == session['user_id']).all()
        """
        #db.session.refresh()
        livros = db.session.query(
            Livros.isbn,
            Livros.titulo,
            Autores.nome,
            Livros.ano_publicacao
        ).join(
            Autores_Livro, Livros.id_livros == Autores_Livro.livros_id_livros
        ).join(
            Autores, Autores_Livro.autores_id_autores == Autores.id_autores
        ).join(
            Estado_Livros, Livros.id_livros == Estado_Livros.livros_id_livros
        ).filter(
            Estado_Livros.usuarios_id_usuarios == session['user_id']
        ).all()
        
        fotos = db.session.query(
            Fotos.foto_base64, 
            Fotos.caminho
        ).join(
            Estado_Livros, Fotos.estado_livros_id_estado_livros == Estado_Livros.id_estado_livros
        ).filter(
            Estado_Livros.usuarios_id_usuarios == session['user_id']
        ).all()
        
        if fotos is not None:
            foto_paths = []
            for foto in fotos:
                foto_string = foto.foto_base64
                foto_data = base64.b64decode(foto_string)
                foto_path = 'static/fotos-tmp/' + str(foto.caminho) + '.jpg'
                
                os.makedirs(os.path.dirname(foto_path), exist_ok=True)
                
                if not os.path.exists(foto_path):
                    with open(foto_path, 'wb') as f:
                        f.write(foto_data)
                foto_paths.append(foto_path)
            return render_template('meus_livros.html', livros=livros, foto_paths=foto_paths)
        return render_template("meus_livros.html", livros=livros)


    return redirect(url_for("login"))


LivrosOfertado = aliased(Livros)
LivrosDesejado = aliased(Livros)
UsuariosOfertante = aliased(Usuarios)
UsuariosReceptor = aliased(Usuarios)

@app.route("/minhas_ofertas", methods=['GET'])
def minhas_ofertas():
    if 'user_id' in session:
        #mLivros = Livros.query.filter_by(id_usuario=session['user_id']).all()
        mLivros = db.session.query(Livros).\
            join(Estado_Livros, Livros.id_livros == Estado_Livros.livros_id_livros).\
            join(Usuarios, Estado_Livros.usuarios_id_usuarios == Usuarios.id_usuarios).\
            filter(Usuarios.id_usuarios == session['user_id']).all()
        
        livros = db.session.query(Livros).\
            join(Estado_Livros, Livros.id_livros == Estado_Livros.livros_id_livros).\
            join(Usuarios, Estado_Livros.usuarios_id_usuarios == Usuarios.id_usuarios).\
            filter(Usuarios.id_usuarios != session['user_id']).all()

        ofertas = db.session.query(
            Ofertas.id_ofertas,
            LivrosOfertado.titulo.label('tituloO'),
            LivrosDesejado.titulo.label('tituloD'),
            UsuariosOfertante.nome.label('usuarioO'),
            UsuariosReceptor.nome.label('usuarioR'),
            Ofertas.id_usuario_receptor.label('receptor'),
            Ofertas.status
        ).join(LivrosOfertado, Ofertas.id_livro_ofertado == LivrosOfertado.id_livros)\
        .join(LivrosDesejado, Ofertas.id_livro_desejado == LivrosDesejado.id_livros)\
        .join(UsuariosOfertante, Ofertas.id_usuario_ofertante == UsuariosOfertante.id_usuarios)\
        .join(UsuariosReceptor, Ofertas.id_usuario_receptor == UsuariosReceptor.id_usuarios)\
        .filter((Ofertas.id_usuario_ofertante == session['user_id']) | (Ofertas.id_usuario_receptor == session['user_id'])).all()
        return render_template("minhas_ofertas.html", mLivros=mLivros, livros=livros, ofertas=ofertas)
    return redirect(url_for("login"))

@app.route("/add_livro", methods=['POST'])
def add_livro():
    isbn = request.form['isbn']
    titulo = request.form['titulo']
    sinopse = request.form['sinopse']
    ano = request.form['ano']
    capa = request.form['capa']
    autor_nome = request.form['autor']
    biografia = request.form['biografia']
    editora_nome = request.form['editora']
    website = request.form['website']
    estado = request.form['estado']
    tempo_compra = request.form['tempo_compra']
    motivo_troca = request.form['motivo_troca']
    opiniao = request.form['opiniao']
    usuario = request.form['fcation']
    fotos = request.files.getlist('fotos')
    
    uuid_livro = get_uuid(1)
    uuid_autor = get_uuid(1)
    uuid_editora = get_uuid(1)
    uuid_estado_livro = get_uuid(1)
    
    
    livro = Livros(id_livros=uuid_livro, isbn=isbn, titulo=titulo, sinopse=sinopse, capa=capa, ano_publicacao=ano)
    autor = Autores(id_autores=uuid_autor, nome=autor_nome, biografia=biografia)
    autor_livro = Autores_Livro(autores_id_autores=uuid_autor, livros_id_livros=uuid_livro)
    editora = Editoras(id_editoras=uuid_editora, nome=editora_nome, website=website)
    editora_livro = Editoras_Livro(editoras_id_editoras=uuid_editora, livros_id_livros=uuid_livro)
    estado_livro = Estado_Livros(id_estado_livros=uuid_estado_livro, estado=estado, tempo_compra=tempo_compra, motivo_troca=motivo_troca, 
                                 opiniao_livro=opiniao, usuarios_id_usuarios=usuario, livros_id_livros=uuid_livro)
    
    
    db.session.add(livro)
    db.session.commit()
    db.session.add(autor)
    db.session.commit()
    db.session.add(autor_livro)
    db.session.commit()
    db.session.add(editora)
    db.session.commit()
    db.session.add(editora_livro)
    db.session.commit()
    db.session.add(estado_livro)
    db.session.commit()
    
    for foto in fotos:
        foto_string = base64.b64encode(foto.read())
        uuid_fotos = get_uuid(1)
        caminho = get_uuid(0)
        imagens = Fotos(id_fotos=uuid_fotos, foto_base64=foto_string, caminho=caminho, estado_livros_id_estado_livros=uuid_estado_livro)
        db.session.add(imagens)
        db.session.commit()

    return redirect(url_for("home"))

@app.route("/atualizar_livro", methods=['POST'])
def atualizar_livro():
    isbn = request.form['isbn_att']
    titulo = request.form['titulo']
    if isbn and titulo:
        try:
            livro = Livros.query.filter_by(isbn=isbn).first()
            livro.titulo = titulo
            db.session.commit()
            return redirect(url_for("meus_livros"))
        except Exception:
            return render_template("meus_livros.html", erro="Não foi possível atualizar o livro!")
    else:
        return render_template("meus_livros.html", erro="Valores inválidos!")

@app.route("/deletar_livro", methods=['POST'])
def deletar_livro():
    isbn = request.form['isbn_del']
    if isbn:
        try:
            Livros.query.filter_by(isbn=isbn).delete()
            db.session.commit()
            return redirect(url_for("meus_livros"))
        except Exception as e:
            print(e)
            return render_template("meus_livros.html", erro="Não foi possível deletar o livro!")
    else:
        return render_template("meus_livros.html", erro="Valor inválidos!")

@app.route("/add_oferta", methods=['POST'])
def add_oferta():
    oferta = request.form['oferta']
    desejo = request.form['desejo']
    usuarioO = request.form['fcation']
    status = "Aberta"
    contato = request.form['contato']
    if type(oferta) != str or type(desejo) != str:
        return redirect(url_for("minhas_ofertas"))
    
    
    usuarioR = db.session.query(Usuarios.id_usuarios).\
        join(Estado_Livros, Usuarios.id_usuarios == Estado_Livros.usuarios_id_usuarios).\
        join(Livros, Estado_Livros.livros_id_livros == Livros.id_livros).\
        filter(Livros.id_livros == desejo).first()

    
    if Ofertas.query.filter_by(id_usuario_receptor=usuarioR, id_usuario_ofertante=usuarioO).first():
        return redirect(url_for("minhas_ofertas"))
    
    oferta = Ofertas(id_ofertas=get_uuid(1),id_livro_ofertado=oferta, id_livro_desejado=desejo, id_usuario_ofertante=usuarioO, id_usuario_receptor=usuarioR[0], status=status)
    db.session.add(oferta)
    db.session.commit()
    return redirect(url_for("minhas_ofertas"))

@app.route("/aceitar_oferta", methods=['POST'])
def aceitar_oferta():
    id = request.form['status']
    oferta = Ofertas.query.filter_by(id_ofertas=id).first()
    oferta.status = 'Aceita'
    db.session.commit()
    return redirect(url_for("minhas_ofertas"))

@app.route("/recusar_oferta", methods=['POST'])
def recusar_oferta():
    id = request.form['status']
    oferta = Ofertas.query.filter_by(id_ofertas=id).first()
    oferta.status = 'Recusada'
    db.session.commit()
    return redirect(url_for("minhas_ofertas"))

def get_uuid(n):
    if n:
        uuid_aleatorio = uuid.uuid4()    
        return uuid_aleatorio.int/100000000000000000000000000000000
    uuid_aleatorio = uuid.uuid4()
    return uuid_aleatorio
