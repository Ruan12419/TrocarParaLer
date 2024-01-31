from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import time
import threading


app = Flask(__name__)
app.secret_key = "N@ur"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Ruan16anos@localhost:3306/trocalivros'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


def limpar_imagens_antigas():
    while True:
        agora = time.time()
        for f in os.listdir('static/fotos-tmp/'):
            f = os.path.join('static/fotos-tmp/', f)
            if os.stat(f).st_mtime < agora - 2 * 60:
                os.remove(f)
        time.sleep(60)


threading.Thread(target=limpar_imagens_antigas).start()



if __name__ == '__main__':
    from models import *
    from routes import *
    with app.app_context():
        db.create_all()
    app.run(debug=True)
