from flask import render_template, session
from app import app
from routes.login import *
from routes.livros import *
from routes.ofertas import *


@app.route('/')
def home():
    if 'user_id' in session:
        livros = Livros.query.all()
        return render_template('index.html', livros=livros)
    return render_template('index.html')

