from PyQt5.QtSql import QSqlDatabase

class ConectarSQLServer:
    '''
    Responsável por estabelecer a conexão com o banco de dados em SQLite.
    '''
    def getConexao():
        db = QSqlDatabase.addDatabase("QODBC3")
        db.setDatabaseName("DRIVER={SQL Server Native Client 11.0};"
                           "Server=(LocalDb)\\testedb;"
                           "Database=CadastroImovel;")
        return db


