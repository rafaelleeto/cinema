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
                       meia INTEGER,
                       conta_id INTEGER,
                       nome_filme,
                       capa)""")

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
        cursor.execute(""" INSERT INTO filmes (nome,sinopse,classificacao,capa) VALUES
                       (?,?,?,?)""", (nome, sinopse, classificacao, capa))


def pegar_filmes():
    with conectar_banco() as cursor:
        cursor.execute("""SELECT * FROM filmes """)
        return cursor.fetchall()


def pegar_filme(id):
    with conectar_banco() as cursor:
        cursor.execute(""" SELECT * FROM filmes where id=? """, (id,))
        return cursor.fetchone()


def criar_conta(email, nome, senha):
    with conectar_banco() as cursor:
        cursor.execute(
            """INSERT INTO conta (email,nome,senha) VALUES (?,?,?)""", (email, nome, senha))


def pegar_conta(email):
    with conectar_banco() as cursor:
        cursor.execute("""SELECT * FROM conta WHERE email=? """, (email,))
        return cursor.fetchone()


def criar_sessao(horario, filme):
    with conectar_banco() as cursor:
        cursor.execute(
            """INSERT INTO  sessoes (horario,filme) VALUES (?,?) """, (horario, filme))


def pegar_sessoes(filme_id):
    with conectar_banco() as cursor:
        cursor.execute("""SELECT * FROM sessoes WHERE filme=?""", (filme_id,))
        return cursor.fetchall()


def criar_ingresso(poltrona, sessao, meia, conta, nome, capa):
    with conectar_banco() as cursor:
        cursor.execute(
            """INSERT INTO  ingressos (poltrona,sessao,meia,conta_id,nome_filme,capa) VALUES (?,?,?,?,?,?) """, (poltrona, sessao, meia, conta, nome, capa))


def pegar_ingresso(id):
    with conectar_banco() as cursor:
        cursor.execute(
            """SELECT * FROM ingressos WHERE sessao=?""", (id,))
        return cursor.fetchall()


def deletar_sessao(id):
    with conectar_banco() as cursor:
        cursor.execute(
            """DELETE  FROM sessoes WHERE id=?""", (id,))
        cursor.execute(
            """DELETE  FROM ingressos WHERE sessao=?""", (id,))


def pegar_sessao_do_filme(id):
    with conectar_banco() as cursor:
        cursor.execute(
            """SELECT  filme FROM sessoes WHERE id=?""", (id,))
        return cursor.fetchone()


def pegar_horario_sessao(id):
    with conectar_banco() as cursor:
        cursor.execute(
            """SELECT horario FROM sessoes WHERE id=?""", (id,))
        return cursor.fetchone()


def atualizar_horario_sessao(horario, id):
    with conectar_banco() as cursor:
        cursor.execute(
            """UPDATE sessoes SET horario=? WHERE id=?""", (horario, id))


def pegar_id_sessao(filme_id):
    with conectar_banco() as cursor:
        cursor.execute("""SELECT id FROM sessoes WHERE filme=?""", (filme_id,))
        return cursor.fetchall()


def excluir_filme(id):
    with conectar_banco() as cursor:
        cursor.execute(
            """DELETE  FROM filmes WHERE id=?""", (id,))
        sessoes = pegar_id_sessao(id)

        if sessoes:
            for sessao in sessoes:
                sessao_id = sessao[0]
                cursor.execute(
                    """DELETE  FROM sessoes WHERE filme=?""", (id,))

                cursor.execute(
                    """DELETE  FROM ingressos WHERE sessao=?""", (sessao_id,))


def atualizar_filme(nome, sinopse, classificacao, capa, id):
    with conectar_banco() as cursor:
        cursor.execute(
            """UPDATE filmes SET nome=?,sinopse=?,classificacao=?,capa=? WHERE id=?""", (nome, sinopse, classificacao, capa, id))


def pegar_ingressos_conta(conta_id):
    with conectar_banco() as cursor:
        cursor.execute(
            """SELECT * FROM ingressos WHERE conta_id=?""", (conta_id,))
        return cursor.fetchall()


def excluir_ingresso(id):
    with conectar_banco() as cursor:
        cursor.execute("""DELETE FROM ingressos WHERE poltrona=?""", (id,))


def pegar_sessao_com_id_da_sessao(id_sessao):
    with conectar_banco() as cursor:
        cursor.execute("""SELECT * FROM sessoes WHERE id=?""", (id_sessao,))
        return cursor.fetchall()


if __name__ == "__main__":
    criar_tabela()
