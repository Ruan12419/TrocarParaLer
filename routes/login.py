from flask import request, render_template, redirect, url_for, session
from app import app, db, get_uuid
from models import *


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
