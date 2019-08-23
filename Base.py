import os
import sqlite3
import io
import datetime
import csv
import random


class Connect(object):

    def __init__(self, db_name):
        try:
            # conectando...
            self.conn = sqlite3.connect(db_name)
            self.cursor = self.conn.cursor()
            print("Banco:", db_name)
            self.cursor.execute('SELECT SQLITE_VERSION()')
            self.data = self.cursor.fetchone()
            print("SQLite version: %s" % self.data)
        except sqlite3.Error:
            print("Erro ao abrir banco.")
            return False

    def CommitDb(self):
        if self.conn:
            self.conn.commit()

    def CloseDb(self):
        if self.conn:
            self.conn.close()
            print("Conexão fechada.")


class NutrifDb(object):

    tb_name = 'nutrif'

    def __init__(self):
        self.db = Connect('db_nufrif.db') #exemplo de DB

    def ContarDadosDaTabela(self):
        r = self.db.cursor.execute(
            'SELECT COUNT(*) FROM tb_cpf')
        return r.fetchone()[0]

    def LocalizarporID(self, id):
        r = self.db.cursor.execute(
            'SELECT cpf FROM tb_cpf WHERE id = ?', (id,))
        return r.fetchone()

    def Atualizar(self,id,cpf):
        c = self.LocalizarporID(id)
        if c:
            # solicitando os dados ao usuário
            # se for no python2.x digite entre aspas simples
            self.novo_cpf = cpf
            self.db.cursor.execute("""
            UPDATE tb_cpf
            SET cpf = ?
            WHERE id = ?
            """, (self.novo_cpf, id,))
            # gravando no bd
            self.db.CommitDb()
            print("Dados atualizados com sucesso.")
        else:
            print('Não existe cliente com o id informado.')

    def CpfAleatorio(self):
        for i in range(self.ContarDadosDaTabela()):
            cpf = ''
            for j in range(11):
                k = random.randint(0,9)
                cpf+=str(k)
            self.Atualizar(i+1,cpf)



    def CloseConnection(self):
        self.db.CloseDb()

if __name__ == '__main__':
    n = NutrifDb()
    n.CpfAleatorio()
    n.CloseConnection()
