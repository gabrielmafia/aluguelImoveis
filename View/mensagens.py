from PyQt5.QtWidgets import QMessageBox


class Mensagem:
    '''
    função responsavel pela exibição de mensagens de erro e aviso
    '''
    def erroConexao(self):
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Warning)
        self.msg.setText("Erro de conexão")
        self.msg.setWindowTitle("Erro")
        self.__exibir(self)

    def enderecoNaoEncontrado(self):
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Warning)
        self.msg.setText("Endereço não encontrado")
        self.msg.setWindowTitle("Erro")
        self.__exibir(self)

    def localNaoEncontrado(self):
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Warning)
        self.msg.setText("Local não encontrado")
        self.msg.setWindowTitle("Erro")
        self.__exibir(self)

    def camposIncompletos(self):
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Warning)
        self.msg.setText("Existem campos incompletos")
        self.msg.setWindowTitle("Aviso")
        self.__exibir(self)

    def erroBancoDados(self, erro):
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Warning)
        self.msg.setText(f"Houve algum erro ao comunicar com o banco de dados \n {erro}")
        self.msg.setWindowTitle("Erro")
        self.__exibir(self)

    def novoCadastro(self):
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Warning)
        self.msg.setText(f"Novo cadastro criado com sucesso")
        self.__exibir(self)

    def alteraCadastro(self):
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Warning)
        self.msg.setText(f"Cadastro alterado com sucesso")
        self.__exibir(self)

    def erroAoPesquisarDB(self):
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Warning)
        self.msg.setText(f"Erro ao pesquisar cliente no banco de dados")
        self.__exibir(self)

    def __exibir(self):
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.exec_()
