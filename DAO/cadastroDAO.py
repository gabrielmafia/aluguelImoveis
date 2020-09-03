from PyQt5.QtSql import QSqlQuery
from database.ConectarSQL import ConectarSQLServer

class Imovel:
    def __init__(self):
        self.id = None

        self.rua = ''
        self.numero = ''
        self.complemento = ''
        self.bairro = ''
        self.cidade = ''
        self.estado = ''
        self.cep = ''

        self.tipo_imovel = ''
        self.area = 0
        self.valor_aluguel = 0
        self.n_banheiros = 0
        self.n_quartos = 0
        self.n_vagas_garagem = 0

        self.distancias = ''
        self.outros = ''


    def CadastrarImovel(self):
        conn = ConectarSQLServer
        db = conn.getConexao()
        if not db.open():
            print('nao abriu base de dados', db.lastError().text())

        query = QSqlQuery()
        query.prepare("INSERT INTO Cadastro"
                      "([rua], [numero], [complemento], [bairro], [cidade], [estado], [cep], "
                      " [tipo_imovel], [area], [valor_aluguel], "
                      " [n_banheiros], [n_quartos], [n_vagas_garagem],"
                      " [vetor_distancias], [vetor_outros])"
                      "VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")

        query.addBindValue(self.rua)
        query.addBindValue(self.numero)
        query.addBindValue(self.complemento)
        query.addBindValue(self.bairro)
        query.addBindValue(self.cidade)
        query.addBindValue(self.estado)
        query.addBindValue(self.cep)

        query.addBindValue(self.tipo_imovel)
        query.addBindValue(self.area)
        query.addBindValue(self.valor_aluguel)
        query.addBindValue(self.n_banheiros)
        query.addBindValue(self.n_quartos)
        query.addBindValue(self.n_vagas_garagem)

        query.addBindValue(self.distancias)
        query.addBindValue(self.outros)


        query.exec_()
        db.commit()
        print('-', query.lastError().text())

        return query


    def AlterarImovel(self):
        conn = ConectarSQLServer
        db = conn.getConexao()
        db.open()

        query = QSqlQuery()
        query.prepare(f"UPDATE Cadastro SET "
                      f"[rua] = '{self.rua}', "
                      f"[numero] = '{self.numero}', "
                      f"[complemento] = '{self.complemento}',"
                      f"[bairro] = '{self.bairro}', "
                      f"[cidade] = '{self.cidade}', "
                      f"[estado] = '{self.estado}', "
                      f"[cep] = '{self.cep}', "
                      f"[tipo_imovel] = '{self.tipo_imovel}', "
                      f"[area] = {self.area}, "
                      f"[valor_aluguel] = {self.valor_aluguel}, "
                      f"[n_banheiros] = {self.n_banheiros}, "
                      f"[n_quartos] = {self.n_quartos}, "
                      f"[n_vagas_garagem] = {self.n_vagas_garagem},"
                      f"[vetor_distancias] = '{self.distancias}', "
                      f"[vetor_outros] = '{self.outros}' "
                      f"WHERE id = {self.id}")

        query.exec_()
        db.commit()
        return query


    def ExcluirImovel(self, id):
        conn = ConectarSQLServer
        db = conn.getConexao()
        db.open()

        query = QSqlQuery()
        query.prepare("DELETE FROM Cadastro WHERE id=:id")
        query.bindValue(":id", id)
        query.exec_()
        db.commit()


    def PesquisarImovel(self):
        conn = ConectarSQLServer
        db = conn.getConexao()
        db.open()

        sql = f"SELECT * FROM Cadastro "
        query = QSqlQuery(sql)

        return query

    def PesquisarImovelPorId(self, id):
        conn = ConectarSQLServer
        db = conn.getConexao()
        db.open()

        sql = f"SELECT * FROM Cadastro WHERE id = {id}"
        query = QSqlQuery(sql)

        return query

