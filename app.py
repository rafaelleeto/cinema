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
        if session["usuario"] != 1:
            flash("Você não tem permissão para fazer isso")
            return redirect("/")
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
        if session["usuario"] != 1:
            flash("Você não tem permissão para fazer isso")
            return redirect("/")
        return render_template("criar_sessao.html")
    horario = request.form["horario"]
    db.criar_sessao(horario, id)
    return redirect(f"/criar_sessoes/{id}")


@app.route("/comprar_ingresso/<sessao>")
def comprar_ingresso(sessao):
    print(sessao)
    ingressos = db.pegar_ingresso(sessao)
    poltronas_ocupadas = [ingresso["poltrona"] for ingresso in ingressos]
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

    toda_sessao = db.pegar_sessao_com_id_da_sessao(sessao)
    primeira_linha = toda_sessao[0]
    filme_id = primeira_linha["filme"]
    nome_filme = db.pegar_filme(filme_id)
    print(nome_filme.keys())
    nome = nome_filme[1]
    capa = nome_filme[4]

    db.criar_ingresso(cadeira, sessao, meia,
                      session["usuario"], nome, capa)
    flash("Compra efetuada com sucesso!")
    return redirect("/")


@app.route("/ver_sessao/<id>")
def ver_sessao(id):
    if session["usuario"] != 1:
        flash("Você não tem permissão para fazer isso")
        return redirect("/")
    sessoes = db.pegar_sessoes(id)
    return render_template("ver_sessao.html", sessoes=sessoes)


@app.route("/excluir/<id>")
def excluir_sessao(id):
    if session["usuario"] != 1:
        flash("Você não tem permissão para fazer isso")
        return redirect("/")
    sessao = db.pegar_sessao_do_filme(id)
    filme_id = sessao["filme"]
    db.deletar_sessao(id)
    return redirect(url_for("ver_sessao", id=filme_id))


@app.route("/editar/<id>", methods=["GET", "POST"])
def editar_sessao(id):
    if session["usuario"] != 1:
        flash("Você não tem permissão para fazer isso")
        return redirect("/")
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
        if session["usuario"] != 1:
            flash("Você não tem permissão para fazer isso")
            return redirect("/")
    filmes = db.pegar_filmes()
    print(filmes)
    return render_template("listar_filmes.html", filmes=filmes)


@app.route("/excluir_filme/<id>")
def excluir_filme(id):
    if session["usuario"] != 1:
        flash("Você não tem permissão para fazer isso")
        return redirect("/")
    db.excluir_filme(id)
    return redirect("/listar_filmes")


@app.route("/editar_filme/<id>", methods=["GET", "POST"])
def editar_filme(id):
    if request.method == "GET":
        if session["usuario"] != 1:
            flash("Você não tem permissão para fazer isso")
            return redirect("/")
        filmes = db.pegar_filme(id)
        print(filmes)
        return render_template("editar_filme.html", filmes=filmes)

    nome = request.form["nome"]
    sinopse = request.form["sinopse"]
    classificacao = request.form["classificacao"]
    capa = request.form["capa"]
    db.atualizar_filme(nome, sinopse, classificacao, capa, id)
    return redirect("/listar_filmes")


# @app.route("/reembolso")
# def reembolso():
#    ingressos = db.pegar_ingressos_conta(session["usuario"])
#    poltronas_ocupadas = [ingresso["poltrona"] for ingresso in ingressos]              !!!!! FUNÇÃO DESABILITADA !!!!
#    if not poltronas_ocupadas:
#       flash("Você não tem possui nenhum ingresso comprado!")
#        return redirect("/")
#     return render_template("reembolso.html", ingressos=poltronas_ocupadas)"""


@app.route("/reembolsar/<id>")
def reembolsar(id):
    db.excluir_ingresso(id)
    flash("Ingresso reembolsado com sucesso")
    return redirect("/")


@app.route("/ver_meus_ingressos")
def ver_ingressos():
    ingressos = db.pegar_ingressos_conta(session["usuario"])
    if not ingressos:
        flash("Você não possui nenhum ingresso!")
        return redirect("/")
    return render_template("ver_ingressos.html", ingressos=ingressos,)


if __name__ == "__main__":
    app.run(debug=True)
