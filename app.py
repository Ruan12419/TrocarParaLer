from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "N@ur"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Ruan16anos@localhost:3306/trocalivros'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


if __name__ == '__main__':
    from models import *
    from routes import *
    with app.app_context():
        db.create_all()
    app.run(debug=True)
