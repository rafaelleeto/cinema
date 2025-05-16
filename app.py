from flask import Flask, redirect, render_template, session, request, flash, url_for
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


@app.route("/comprar_filme/<id>")
def comprar(id):
    if not session:
        return redirect("/login")
    filme = db.pegar_filme(id)
    sessoes = db.pegar_sessoes(id)

    return render_template("comprar_filme.html", filme=filme, sessoes=sessoes)


@app.route("/criar_sessoes/<id>", methods=["GET", "POST"])
def criar_sessao(id):
    if request.method == "GET":
        return render_template("criar_sessao.html")
    horario = request.form["horario"]
    db.criar_sessao(horario, id)
    return redirect(f"/criar_sessoes/{id}")


@app.route("/comprar_ingresso/<sessao>")
def comprar_ingresso(sessao):
    print(sessao)
    ingressos = db.pegar_ingresso(sessao)
    poltronas_ocupadas = [ingresso["poltrona"] for ingresso in ingressos]
    print(poltronas_ocupadas)
    return render_template("ingresso.html", sessao=sessao, ingressos=poltronas_ocupadas)


@app.route("/cadeira/<sessao>/<cadeira>", methods=["GET", "POST"])
def comprar_cadeira(sessao, cadeira):
    if request.method == "GET":
        return render_template("comprar_cadeira.html")
    meia = request.form["meia"]
    if meia == "sim":
        meia = 1
    else:
        meia = 0

    db.criar_ingresso(cadeira, sessao, meia)
    flash("Compra efetuada com sucesso!")
    return redirect("/")


@app.route("/ver_sessao/<id>")
def ver_sessao(id):
    sessoes = db.pegar_sessoes(id)
    return render_template("ver_sessao.html", sessoes=sessoes)


@app.route("/excluir/<id>")
def excluir_sessao(id):
    sessao = db.pegar_sessao_do_filme(id)
    filme_id = sessao["filme"]
    db.deletar_sessao(id)
    return redirect(url_for("ver_sessao", id=filme_id))


@app.route("/editar/<id>", methods=["GET", "POST"])
def editar_sessao(id):
    if request.method == "GET":
        horario = db.pegar_horario_sessao(id)
        return render_template("editar_sessao.html", horario=horario)
    novo_horario = request.form["horario"]
    db.atualizar_horario_sessao(novo_horario, id)
    sessao = db.pegar_sessao_do_filme(id)
    filme_id = sessao["filme"]
    return redirect(url_for("ver_sessao", id=filme_id))


@app.route("/listar_filmes")
def listar_filmes():
    if request.method == "GET":
        filmes = db.pegar_filmes()
        print(filmes)
        return render_template("listar_filmes.html", filmes=filmes)


@app.route("/excluir_filme/<id>")
def excluir_filme(id):
    db.excluir_filme(id)
    return redirect("/listar_filmes")


@app.route("/editar_filme/<id>", methods=["GET", "POST"])
def editar_filme(id):
    if request.method == "GET":
        filmes = db.pegar_filme(id)
        print(filmes)
        return render_template("editar_filme.html", filmes=filmes)

    nome = request.form["nome"]
    sinopse = request.form["sinopse"]
    classificacao = request.form["classificacao"]
    capa = request.form["capa"]
    db.atualizar_filme(nome, sinopse, classificacao, capa, id)
    return redirect("/listar_filmes")


if __name__ == "__main__":
    app.run(debug=True)
