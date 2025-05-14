from flask import Flask, redirect, render_template, session, request
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


if __name__ == "__main__":
    app.run(debug=True)
