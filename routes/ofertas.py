from flask import request, render_template, redirect, url_for, session
from app import app, db, get_uuid, db_add
from routes.login import *
from models import *
from sqlalchemy.orm import aliased


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
    db_add(oferta)
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

