from flask import Flask, redirect, render_template, session, request, flash
from werkzeug.security import check_password_hash, generate_password_hash
import db

app = Flask(__name__)
app.secret_key = "Chave_Secreta"


@app.route("/")
def index():
    filmes = db.pegar_filmes()
    return render_template("index.html", filmes=filmes)


@app.route("/criar_filmes", methods=["GET", "POST"])
def criar_filmes():
    if request.method == "GET":
        return render_template("criar_filme.html")
    nome = request.form["nome"]
    sinopse = request.form["sinopse"]
    classificacao = request.form["classificacao"]
    capa = request.form["capa"]
    db.adicionar_filme(nome, sinopse, classificacao, capa)
    return redirect("/criar_filmes")


@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "GET":
        return render_template("registro.html")

    nome = request.form["nome"]
    senha1 = request.form["senha1"]
    senha2 = request.form["senha2"]
    email = request.form["email"]

    if senha1 != senha2:
        flash("Senhas diferentes, tente novamente")
        return redirect("/registro")

    senha_criptografada = generate_password_hash(senha1)
    db.criar_conta(email, nome, senha_criptografada)
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form["email"]
    senha = request.form["senha"]
    conta = db.pegar_conta(email)
    if not check_password_hash(conta["senha"], senha):
        flash("Email ou senha inválidos")
        return redirect("/login")
    session["usuario"] = conta["id"]
    return redirect("/")


@app.route("/sair")
def sair():
    session.pop("usuario", None)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
