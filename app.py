from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///meubanco.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# =========================
# MODELOS
# =========================

class Usuario(db.Model):
    email = db.Column(db.String(120), unique=True, nullable=False, primary_key=True)
    senha = db.Column(db.String(200), nullable=False)
    nome = db.Column(db.String(100), nullable=False)


class Problema(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(200), nullable=False)
    gravidade = db.Column(db.String(200), nullable=False)
    localizacao = db.Column(db.String(200), nullable=False)


class Instituicao(db.Model):
    cnpj = db.Column(db.String(18), unique=True, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)


# =========================
# ROTA PRINCIPAL
# =========================

@app.route("/")
def index():
    return render_template("index.html")


# ==================================================
# CRUD USUARIO
# ==================================================

# READ - listar usuários
@app.route("/usuarios")
def listar_usuarios():
    usuarios = Usuario.query.all()
    return render_template("usuarios.html", usuarios=usuarios)


# CREATE - criar usuário
@app.route("/usuarios/novo", methods=["GET", "POST"])
def criar_usuario():

    if request.method == "POST":

        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        usuario = Usuario(
            nome=nome,
            email=email,
            senha=senha
        )

        db.session.add(usuario)
        db.session.commit()

        return redirect(url_for("listar_usuarios"))

    return render_template("usuario_form.html")


# UPDATE - editar usuário
@app.route("/usuarios/editar/<email>", methods=["GET", "POST"])
def editar_usuario(email):

    usuario = Usuario.query.get_or_404(email)

    if request.method == "POST":

        usuario.nome = request.form["nome"]
        usuario.email = request.form["email"]
        usuario.senha = request.form["senha"]

        db.session.commit()

        return redirect(url_for("listar_usuarios"))

    return render_template("usuario_form.html", usuario=usuario)


# DELETE - excluir usuário
@app.route("/usuarios/excluir/<email>", methods=["POST"])
def excluir_usuario(email):

    usuario = Usuario.query.get_or_404(email)

    db.session.delete(usuario)
    db.session.commit()

    return redirect(url_for("listar_usuarios"))


# ==================================================
# CRUD PROBLEMA
# ==================================================

# READ
@app.route("/problemas")
def listar_problemas():

    problemas = Problema.query.all()

    return render_template(
        "problemas.html",
        problemas=problemas
    )


# CREATE
@app.route("/problemas/novo", methods=["GET", "POST"])
def criar_problema():

    if request.method == "POST":

        status = request.form["status"]
        gravidade = request.form["gravidade"]
        localizacao = request.form["localizacao"]

        problema = Problema(
            status=status,
            gravidade=gravidade,
            localizacao=localizacao
        )

        db.session.add(problema)
        db.session.commit()

        return redirect(url_for("listar_problemas"))

    return render_template("problema_form.html")


# UPDATE
@app.route("/problemas/editar/<int:id>", methods=["GET", "POST"])
def editar_problema(id):

    problema = Problema.query.get_or_404(id)

    if request.method == "POST":

        problema.status = request.form["status"]
        problema.gravidade = request.form["gravidade"]
        problema.localizacao = request.form["localizacao"]

        db.session.commit()

        return redirect(url_for("listar_problemas"))

    return render_template(
        "problema_form.html",
        problema=problema
    )


# DELETE
@app.route("/problemas/excluir/<int:id>", methods=["POST"])
def excluir_problema(id):

    problema = Problema.query.get_or_404(id)

    db.session.delete(problema)
    db.session.commit()

    return redirect(url_for("listar_problemas"))


# ==================================================
# CRUD INSTITUICAO
# ==================================================

# READ
@app.route("/instituicoes")
def listar_instituicoes():

    instituicoes = Instituicao.query.all()

    return render_template(
        "instituicoes.html",
        instituicoes=instituicoes
    )


# CREATE
@app.route("/instituicoes/nova", methods=["GET", "POST"])
def criar_instituicao():

    if request.method == "POST":

        cnpj = request.form["cnpj"]
        nome = request.form["nome"]
        telefone = request.form["telefone"]

        instituicao = Instituicao(
            cnpj=cnpj,
            nome=nome,
            telefone=telefone
        )

        db.session.add(instituicao)
        db.session.commit()

        return redirect(url_for("listar_instituicoes"))

    return render_template("instituicao_form.html")


# UPDATE
@app.route("/instituicoes/editar/<cnpj>", methods=["GET", "POST"])
def editar_instituicao(cnpj):

    instituicao = Instituicao.query.get_or_404(cnpj)

    if request.method == "POST":

        instituicao.nome = request.form["nome"]
        instituicao.telefone = request.form["telefone"]

        db.session.commit()

        return redirect(url_for("listar_instituicoes"))

    return render_template(
        "instituicao_form.html",
        instituicao=instituicao
    )


# DELETE
@app.route("/instituicoes/excluir/<cnpj>", methods=["POST"])
def excluir_instituicao(cnpj):

    instituicao = Instituicao.query.get_or_404(cnpj)

    db.session.delete(instituicao)
    db.session.commit()

    return redirect(url_for("listar_instituicoes"))


# ==================================================
# BANCO DE DADOS
# ==================================================

if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(debug=True)