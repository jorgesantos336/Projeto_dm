from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///meubanco.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Usuario(db.Model):
    senha = db.Column(db.Integer, nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, primary_key=True)
    
class Problema(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    status = db.Column(db.String(200), nullable=False)
    gravidade = db.Column(db.String(200), nullable=False)
    localização = db.Column(db.String(200), nullable=False)
    
class Instituição(db.Model):
    cnpj = db.Column(db.Integer, unique=True, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)

@app.route("/")
def index():
    usuarios = Usuario.query.all()
    return render_template("index.html", usuarios=usuarios)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        
        Usuario1 = Usuario(senha=1234, nome="João", email="joao@Gmail.com")
        db.session.add(Usuario1)
        db.session.commit()
        
        Problema1 = Problema(id=1, status="Aberto", gravidade="Alta", localização="Rua A")
        db.session.add(Problema1)
        db.session.commit()
        
        Instituição1 = Instituição(cnpj=123456789, nome="Prefeitura", telefone="123456789")
        db.session.add(Instituição1)
        db.session.commit()

    app.run(debug=True)
