import sqlite3
from contextlib import contextmanager


@contextmanager
def conectar_banco():
    conexao = sqlite3.connect("cinema.db")
    conexao.row_factory = sqlite3.Row
    cursor = conexao.cursor()
    try:
        yield cursor
    finally:
        conexao.commit()
        cursor.close()
        conexao.close()


def criar_tabela():
    with conectar_banco() as cursor:
        cursor.execute(""" CREATE TABLE IF NOT EXISTS ingressos 
                       (ID INTEGER PRIMARY KEY, 
                       poltrona INTEGER, 
                       sessao INTEGER, 
                       meia INTEGER)""")

        cursor.execute(""" CREATE TABLE IF NOT EXISTS filmes
                       (ID INTEGER PRIMARY KEY,
                       nome TEXT, 
                       sinopse TEXT, 
                       classificacao INTEGER,
                       capa TEXT)""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS conta 
                       (ID INTEGER PRIMARY KEY,
                       email TEXT UNIQUE,
                       nome TEXT,
                       senha TEXT)""")

        cursor.execute("""CREATE TABLE IF NOT EXISTS sessoes 
                       (ID INTEGER PRIMARY KEY,
                       horario TEXT,
                       filme INTEGER
                       )""")


def adicionar_filme(nome: str, sinopse: str, classificacao: int, capa: str):
    with conectar_banco() as cursor:
        cursor.execute(
            """ INSERT INTO filmes (nome,sinopse,classificacao,capa) VALUES (?,?,?,?)""", (nome, sinopse, classificacao, capa))


def pegar_filmes():
    with conectar_banco() as cursor:
        cursor.execute("""SELECT * FROM filmes """)
        return cursor.fetchall()


def criar_conta(email, nome, senha):
    with conectar_banco() as cursor:
        cursor.execute(
            """INSERT INTO conta (email,nome,senha) VALUES (?,?,?)""", (email, nome, senha))


def pegar_conta(email):
    with conectar_banco() as cursor:
        cursor.execute("""SELECT * FROM conta WHERE email=? """, (email,))
        return cursor.fetchone()


if __name__ == "__main__":
    criar_tabela()
