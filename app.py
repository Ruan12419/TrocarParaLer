from flask import Flask, g, request, render_template, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "N@ur"
DATABASE = 'dados.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def home():
    if 'user_id' in session:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT isbn, titulo, autor, ano, id_usuario FROM Livros;")
        livros = [dict(isbn=row[0], titulo=row[1], autor=row[2], ano=row[3], id_usuario=row[4]) for row in cursor.fetchall()]
        return render_template('index.html', livros=livros)
    return render_template('index.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Usuarios WHERE email = ? AND senha = ?;", (request.form['email'], request.form['senha']))
        linhas = cursor.fetchall()
        if len(linhas) == 1:
            session['user_id'] = linhas[0][0]
            return redirect(url_for("home"))
    return render_template("login.html")

@app.route("/logout", methods=['POST'])
def logout():
    session['user_id'] = False
    return redirect(url_for("home"))


@app.route('/cadastrar_usuario', methods=['POST'])
def add_usuario():
    db = get_db()
    cursor = db.cursor()

    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']
    confirma_senha = request.form['confirmacao_senha']

    if senha != confirma_senha:
        return render_template("login.html", erro="As senhas não correspondem!")

    cursor.execute("INSERT INTO Usuarios (Nome, Email, Senha) VALUES (?, ?, ?)", (nome, email, senha))
    db.commit()
    
    cursor.execute("SELECT * FROM Usuarios WHERE email = ? AND senha = ?;", (request.form['email'], request.form['senha']))
    linhas = cursor.fetchall()
    if len(linhas) == 1:
        session['user_id'] = linhas[0][0]
        return redirect(url_for("home"))

    return redirect(url_for("login"))

@app.route("/meus_livros", methods=['GET'])
def meus_livros():
    db = get_db()
    cursor = db.cursor()
    if session['user_id']:
        cursor.execute("SELECT isbn, titulo, autor, ano FROM Livros where id_usuario = ?;", (session['user_id'],))
        livros = [dict(isbn=row[0], titulo=row[1], autor=row[2], ano=row[3]) for row in cursor.fetchall()]
        return render_template("meus_livros.html", livros=livros)
    return redirect(url_for("login"))

@app.route("/minhas_ofertas", methods=['GET'])
def minhas_ofertas():
    db = get_db()
    cursor = db.cursor()
    if session['user_id']:
        cursor.execute("SELECT id, isbn, titulo, autor, ano FROM Livros where id_usuario = ?;", (session['user_id'],))
        mLivros = [dict(id=row[0], isbn=row[1], titulo=row[2], autor=row[3], ano=row[4]) for row in cursor.fetchall()]
        
        cursor.execute("SELECT * FROM Livros;")
        livros = [dict(id=row[0], titulo=row[1], autor=row[2], ano=row[3], id_usuario=row[4], isbn=row[5]) for row in cursor.fetchall()]
        
        cursor.execute("""
            SELECT 
                Ofertas.id, 
                LivrosO.titulo as tituloO, 
                LivrosD.titulo as tituloD, 
                UsuariosO.nome as usuarioO, 
                UsuariosR.nome as usuarioR,
                Ofertas.id_usuario_receptor as receptor,
                Ofertas.status, 
                Ofertas.contato 
            FROM Ofertas 
            JOIN Livros as LivrosO ON Ofertas.id_livro_ofertado = LivrosO.id
            JOIN Livros as LivrosD ON Ofertas.id_livro_desejado = LivrosD.id
            JOIN Usuarios as UsuariosO ON Ofertas.id_usuario_ofertante = UsuariosO.id
            JOIN Usuarios as UsuariosR ON Ofertas.id_usuario_receptor = UsuariosR.id
            WHERE Ofertas.id_usuario_ofertante = ? OR Ofertas.id_usuario_receptor = ?;
        """, (session['user_id'],session['user_id'],))
        ofertas = [dict(id=row[0], tituloO=row[1], tituloD=row[2], usuarioO=row[3], usuarioR=row[4], receptor=row[5], status=row[6], contato=row[7]) for row in cursor.fetchall()]
        
        return render_template("minhas_ofertas.html", mLivros=mLivros, livros=livros, ofertas=ofertas)
    
    return redirect(url_for("login"))



@app.route("/add_livro", methods=['POST'])
def add_livro():
    db = get_db()
    cursor = db.cursor()
    
    isbn = request.form['isbn']
    titulo = request.form['titulo']
    autor = request.form['autor']
    ano = request.form['ano']
    usuario = request.form['fcation']
    cursor.execute("INSERT INTO Livros (isbn, titulo, autor, ano, id_usuario) VALUES (?, ?, ?, ?, ?);", (isbn, titulo, autor, ano, usuario))
    db.commit()
    
    return redirect(url_for("home"))

@app.route("/atualizar_livro", methods=['POST'])
def atualizar_livro():
    db = get_db()
    cursor = db.cursor()
    
    isbn = request.form['isbn']
    titulo = request.form['titulo']
    
    if isbn and titulo:
        try:
            cursor.execute("UPDATE Livros SET titulo = ? WHERE isbn = ?;", (titulo, isbn,))
            db.commit()
            return redirect(url_for("meus_livros"))
        except Exception:
            print("Erro ao tentar atualizar livro!")
            return render_template("meus_livros.html", erro="Não foi possível atualizar o livro!")
    else:
        return render_template("meus_livros.html", erro="Valores inválidos!")
    
@app.route("/deletar_livro", methods=['POST'])
def deletar_livro():
    db = get_db()
    cursor = db.cursor()
    
    isbn = request.form['isbn']
    if isbn:
        try:
            cursor.execute("DELETE FROM Livros WHERE isbn = ?;", (isbn,))
            db.commit()
            return redirect(url_for("meus_livros"))
        except Exception:
            print("Erro ao tentar deletar livro!")
            return render_template("meus_livros.html", erro="Não foi possível deletar o livro!")
    else:
        return render_template("meus_livros.html", erro="Valor inválidos!")
    

@app.route("/add_oferta", methods=['POST'])
def add_oferta():
    db = get_db()
    cursor = db.cursor()
    
    oferta = request.form['oferta']
    desejo = request.form['desejo']
    usuarioO = request.form['fcation']
    status = "Aberta"
    contato = request.form['contato']
    print(type(oferta))
    print(type(desejo))
    if type(oferta) != str or type(desejo) != str:
        return redirect(url_for("minhas_ofertas"))
        
    
    cursor.execute("SELECT u.id FROM Usuarios u JOIN Livros l ON u.id = l.id_usuario WHERE l.id = ?;", (desejo,))
    usuarioR = cursor.fetchall()
    usuarioR = usuarioR[0][0]
    
    cursor.execute("SELECT id FROM Ofertas WHERE id_usuario_receptor = ? AND id_usuario_ofertante = ?;", (usuarioR, usuarioO))
    linhas = cursor.fetchall()
    if linhas:
        return redirect(url_for("minhas_ofertas"))
    
    cursor.execute("INSERT INTO Ofertas(id_livro_ofertado, id_livro_desejado, id_usuario_ofertante, id_usuario_receptor, status, contato) VALUES (?, ?, ?, ?, ?, ?);", (oferta, desejo, usuarioO, usuarioR, status,contato,))
    db.commit()
    return redirect(url_for("minhas_ofertas"))


@app.route("/aceitar_oferta", methods=['POST'])
def aceitar_oferta():
    db = get_db()
    cursor = db.cursor()
    
    id = request.form['status']
    
    cursor.execute("UPDATE Ofertas SET status = 'Aceita' WHERE id = ?;", (id,))
    db.commit()
    
    return redirect(url_for("minhas_ofertas"))

@app.route("/recusar_oferta", methods=['POST'])
def recusar_oferta():
    db = get_db()
    cursor = db.cursor()
    
    id = request.form['status']
    
    cursor.execute("UPDATE Ofertas SET status = 'Recusada' WHERE id = ?;", (id,))
    db.commit()
    
    return redirect(url_for("minhas_ofertas"))




if __name__ == '__main__':
    app.run(debug=True)
