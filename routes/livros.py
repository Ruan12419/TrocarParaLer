from flask import request, render_template, redirect, url_for, session
from app import app, db, get_uuid, db_add
from sqlalchemy import text
from routes.index import *
from routes.login import *
from models.livros_model import *
from models.autores_model import *
from models.editoras_model import *
from models.fotos_model import *
import base64
import os


@app.route("/meus_livros", methods=['GET'])
def meus_livros():
    if 'user_id' in session:
        
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
    fotos = request.files.getlist('fotos')
    
    usuario = request.form['fcation']
    
    uuid_livro = get_uuid(1)
    uuid_autor = get_uuid(1)
    uuid_editora = get_uuid(1)
    uuid_estado_livro = get_uuid(1)
    uuid_fotos = get_uuid(1)
    
    fotos_string = ','.join([base64.b64encode(foto.read()).decode('utf-8') for foto in fotos])

    params = {"isbn": isbn,
        "titulo": titulo,
        "sinopse": sinopse,
        "ano": ano,
        "capa": capa,
        "autor_nome": autor_nome,
        "biografia": biografia,
        "editora_nome": editora_nome,
        "website": website,
        "estado": estado,
        "tempo_compra": tempo_compra,
        "motivo_troca": motivo_troca,
        "opiniao": opiniao,
        "usuario": usuario,
        "fotos_string": fotos_string,
        "uuid_livro": uuid_livro,
        "uuid_autor": uuid_autor,
        "uuid_editora": uuid_editora,
        "uuid_estado_livro": uuid_estado_livro,
        "uuid_fotos": uuid_fotos
    }
    
    stmt = text("CALL AddLivro(:isbn, :titulo, :sinopse, :ano, :capa, :autor_nome, :biografia, :editora_nome, :website, :estado, "
                +":tempo_compra, :motivo_troca, :opiniao, :usuario, :fotos_string, :uuid_livro, :uuid_autor, :uuid_editora, :uuid_estado_livro, :uuid_fotos)")
    db.session.execute(stmt, params)
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
            app.limpar_imagens_antigas()
            return redirect(url_for("meus_livros"))
        except Exception as e:
            print(e)
            return render_template("meus_livros.html", erro="Não foi possível deletar o livro!")
    else:
        return render_template("meus_livros.html", erro="Valor inválidos!")
