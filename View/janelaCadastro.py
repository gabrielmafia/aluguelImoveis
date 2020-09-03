from PyQt5 import QtCore, QtGui, QtWidgets
from DAO.cadastroDAO import Imovel
from Controller.RequestThread import ThreadUF, ThreadDistancias
from View.mensagens import Mensagem


class Ui_janelaCadastro(object):
    def buscar_cidades_por_uf(self, UF):
        '''
        Método que chama a função responsável pelo request dos municípios de acordo com o estado desejado.
        '''

        url = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{UF}/municipios"
        thread_uf = ThreadUF(url)
        thread_uf.sinal.connect(self.on_data_ready_uf)
        thread_uf.sinal_erro.connect(self.mensagem_erro_conexao)
        self.thread_uf = thread_uf
        thread_uf.start()

    def on_data_ready_uf(self, json_data):
        '''
        Método reponsavel por preencher a combobox dos municípios;
        '''
        self.combo_cidade.clear()
        for municipio in json_data:
            self.combo_cidade.addItem(municipio['nome'])

    def mensagem_erro_conexao(self):
        '''
        Exibe mensagem de erro de conexão.
        '''
        msg = Mensagem
        msg.erroConexao(msg)

    def calcular_distancias(self):
        '''
        Chama a função responsável por encontrar a distancias de um endereço desejado a locais de interesse.
        '''
        endereco = f"{self.edt_rua.text()} {self.edt_numero.text()} {self.edt_bairro.text()} " \
            f"{self.combo_cidade.currentText()} {self.combo_estado.currentText()}"
        locais = [self.table_distancias.verticalHeaderItem(row).text()
                  for row in range(self.table_distancias.rowCount())]

        thread_distancias = ThreadDistancias(endereco, locais)
        thread_distancias.sinal.connect(self.on_data_ready_distancias)
        thread_distancias.sinal_erro.connect(self.mensagem_erro_conexao)
        self.thread_distancias = thread_distancias
        thread_distancias.start()

    def on_data_ready_distancias(self, distancias):
        '''
        Responsável por preencher a tabela de distancias com os valores encontrados pela função calcular_distancias.
        '''
        for row in range(self.table_distancias.rowCount()):
            dist = distancias[self.table_distancias.verticalHeaderItem(row).text()]
            self.table_distancias.setItem(row, 0, QtWidgets.QTableWidgetItem(dist))


    def preencher_informacoes(self):
        '''
        Método responsável por preencher as informações dos campos editáveis com as informações do imóvel contidas
        no banco de dados SQL.
        '''

        imovel = Imovel
        query = imovel.PesquisarImovelPorId(imovel, self.id)
        query.next()

        self.edt_rua.setText(str(query.value(1)))
        self.edt_numero.setText(str(query.value(2)))
        self.edt_complemento.setText(str(query.value(3)))
        self.edt_bairro.setText(str(query.value(4)))

        index = self.combo_estado.findText(str(query.value(6)), QtCore.Qt.MatchCaseSensitive)
        if index >= 0:
            self.combo_estado.setCurrentIndex(index)

        self.combo_cidade.addItem(str(query.value(5)))

        index = self.combo_tipo.findText(str(query.value(8)), QtCore.Qt.MatchCaseSensitive)
        if index >= 0:
            self.combo_tipo.setCurrentIndex(index)

        self.spin_area.setValue(query.value(9))
        self.spin_aluguel.setValue(query.value(10))
        self.spin_banheiros.setValue(query.value(11))
        self.spin_quartos.setValue(query.value(12))
        self.spin_garagem.setValue(query.value(13))

        try:
            distancias = str(query.value(14)).split(';')
            for row in range(self.table_distancias.rowCount()):
                self.table_distancias.setItem(row, 0, QtWidgets.QTableWidgetItem(distancias[row]))
        except:
            pass


        outros = str(query.value(15))
        for row in range(self.table_outros.rowCount()):
            if outros[row] == '1':
                self.table_outros.item(row, 0).setCheckState(QtCore.Qt.Checked)
            else:
                self.table_outros.item(row, 0).setCheckState(QtCore.Qt.Unchecked)


    def salvar(self):
        '''
        Método responsável por salvar as informações do imóvel. Seja inserirndo um novo cadastro ou editando
        um cadastro já existente.
        '''

        imovel = Imovel

        imovel.rua = self.edt_rua.text()
        imovel.numero = self.edt_numero.text()
        imovel.complemento = self.edt_complemento.text()
        imovel.bairro = self.edt_bairro.text()
        imovel.cidade = self.combo_cidade.currentText()
        imovel.estado = self.combo_estado.currentText()
        imovel.cep = ''

        imovel.tipo_imovel = self.combo_tipo.currentText()
        imovel.area = self.spin_area.value()
        imovel.valor_aluguel = self.spin_aluguel.value()
        imovel.n_banheiros = self.spin_banheiros.value()
        imovel.n_quartos = self.spin_quartos.value()
        imovel.n_vagas_garagem = self.spin_garagem.value()

        imovel.distancias = ''
        try:
            for row in range(self.table_distancias.rowCount()):
                imovel.distancias += self.table_distancias.item(row, 0).text() + ';'
            imovel.distancias = imovel.distancias[:-1]
        except:
            pass

        imovel.outros = ''
        for row in range(self.table_outros.rowCount()):
            if self.table_outros.item(row, 0).checkState() == QtCore.Qt.Checked:
                imovel.outros += '1'
            else:
                imovel.outros += '0'

        if self.validar_imovel(imovel):
            if self.modo == 'inserir':
                self.inserir_imovel(imovel)

            elif self.modo == 'editar':
                self.editar_imovel(imovel)

            self.janelaPrincipal.pesquisar_imoveis()

    def validar_imovel(self, imovel):
        if imovel.rua == '' or imovel.numero == '' or imovel.estado == '' or imovel.cidade == '' \
                or imovel.area == 0 or imovel.valor_aluguel == 0:
            msg = Mensagem
            msg.camposIncompletos(msg)
            return False
        else:
            return True

    def inserir_imovel(self, imovel):
        '''
        Métodos responsável por inserir o cadastro de um novo imóvel no banco de dados.
        '''
        query = imovel.CadastrarImovel(imovel)

        msg = Mensagem
        if query.lastError().type() > 0:
            msg.erroBancoDados(msg, query.lastError().text())
        else:
            self.modo = 'editar'
            self.id = str(query.lastInsertId())
            msg.novoCadastro(msg)

    def editar_imovel(self, imovel):
        '''
        Métodos responsável por editar um imóvel ja existente no banco de dados.
        '''
        imovel.id = self.id
        query = imovel.AlterarImovel(imovel)

        msg = Mensagem
        if query.lastError().type() > 0:
            msg.erroBancoDados(msg, query.lastError().text())
        else:
            msg.alteraCadastro(msg)

    def setupUi(self, MainWindow, modo, id, janelaPrincipal):

        # SETUP GERADO PELO QTDESINGER

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(428, 659)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 411, 151))
        self.groupBox.setObjectName("groupBox")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(100, 80, 47, 13))
        self.label_2.setObjectName("label_2")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(20, 80, 47, 13))
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(280, 80, 47, 13))
        self.label_3.setObjectName("label_3")
        self.edt_bairro = QtWidgets.QLineEdit(self.groupBox)
        self.edt_bairro.setGeometry(QtCore.QRect(280, 100, 113, 20))
        self.edt_bairro.setObjectName("edt_bairro")
        self.combo_cidade = QtWidgets.QComboBox(self.groupBox)
        self.combo_cidade.setGeometry(QtCore.QRect(100, 100, 161, 22))
        self.combo_cidade.setObjectName("combo_cidade")
        self.edt_rua = QtWidgets.QLineEdit(self.groupBox)
        self.edt_rua.setGeometry(QtCore.QRect(20, 50, 181, 20))
        self.edt_rua.setObjectName("edt_rua")
        self.edt_numero = QtWidgets.QLineEdit(self.groupBox)
        self.edt_numero.setGeometry(QtCore.QRect(210, 50, 61, 20))
        self.edt_numero.setObjectName("edt_numero")
        self.edt_complemento = QtWidgets.QLineEdit(self.groupBox)
        self.edt_complemento.setGeometry(QtCore.QRect(280, 50, 113, 20))
        self.edt_complemento.setObjectName("edt_complemento")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(20, 30, 47, 13))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(210, 30, 47, 13))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(280, 30, 71, 16))
        self.label_6.setObjectName("label_6")
        self.combo_estado = QtWidgets.QComboBox(self.groupBox)
        self.combo_estado.setGeometry(QtCore.QRect(20, 100, 69, 22))
        self.combo_estado.setObjectName("combo_estado")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 170, 411, 441))
        self.groupBox_2.setObjectName("groupBox_2")
        self.combo_tipo = QtWidgets.QComboBox(self.groupBox_2)
        self.combo_tipo.setGeometry(QtCore.QRect(20, 40, 111, 22))
        self.combo_tipo.setObjectName("combo_tipo")
        self.spin_quartos = QtWidgets.QSpinBox(self.groupBox_2)
        self.spin_quartos.setGeometry(QtCore.QRect(70, 130, 42, 22))
        self.spin_quartos.setObjectName("spin_quartos")
        self.spin_banheiros = QtWidgets.QSpinBox(self.groupBox_2)
        self.spin_banheiros.setGeometry(QtCore.QRect(70, 160, 42, 22))
        self.spin_banheiros.setObjectName("spin_banheiros")
        self.spin_garagem = QtWidgets.QSpinBox(self.groupBox_2)
        self.spin_garagem.setGeometry(QtCore.QRect(70, 190, 42, 22))
        self.spin_garagem.setObjectName("spin_garagem")
        self.spin_area = QtWidgets.QSpinBox(self.groupBox_2)
        self.spin_area.setGeometry(QtCore.QRect(20, 90, 61, 22))
        self.spin_area.setMaximum(99999)
        self.spin_area.setObjectName("spin_area")
        self.spin_aluguel = QtWidgets.QDoubleSpinBox(self.groupBox_2)
        self.spin_aluguel.setGeometry(QtCore.QRect(110, 90, 81, 22))
        self.spin_aluguel.setMaximum(99999.99)
        self.spin_aluguel.setObjectName("spin_aluguel")
        self.label_7 = QtWidgets.QLabel(self.groupBox_2)
        self.label_7.setGeometry(QtCore.QRect(20, 20, 61, 16))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.groupBox_2)
        self.label_8.setGeometry(QtCore.QRect(20, 70, 47, 13))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.groupBox_2)
        self.label_9.setGeometry(QtCore.QRect(110, 70, 47, 13))
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.groupBox_2)
        self.label_10.setGeometry(QtCore.QRect(20, 130, 47, 13))
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.groupBox_2)
        self.label_11.setGeometry(QtCore.QRect(20, 160, 47, 13))
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.groupBox_2)
        self.label_12.setGeometry(QtCore.QRect(20, 190, 47, 13))
        self.label_12.setObjectName("label_12")
        self.button_calcular = QtWidgets.QPushButton(self.groupBox_2)
        self.button_calcular.setGeometry(QtCore.QRect(20, 230, 111, 23))
        self.button_calcular.setObjectName("button_calcular")
        self.table_distancias = QtWidgets.QTableWidget(self.groupBox_2)
        self.table_distancias.setGeometry(QtCore.QRect(20, 260, 180, 161))
        self.table_distancias.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.table_distancias.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.table_distancias.setAutoScroll(False)
        self.table_distancias.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_distancias.setTabKeyNavigation(False)
        self.table_distancias.setDragDropOverwriteMode(False)
        self.table_distancias.setShowGrid(False)
        self.table_distancias.setWordWrap(False)
        self.table_distancias.setCornerButtonEnabled(False)
        self.table_distancias.setObjectName("table_distancias")
        self.table_distancias.setColumnCount(2)
        self.table_distancias.setRowCount(6)
        item = QtWidgets.QTableWidgetItem()
        self.table_distancias.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_distancias.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_distancias.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_distancias.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_distancias.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_distancias.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_distancias.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_distancias.setHorizontalHeaderItem(1, item)
        self.table_distancias.horizontalHeader().setDefaultSectionSize(80)
        self.table_distancias.verticalHeader().setDefaultSectionSize(23)
        self.table_outros = QtWidgets.QTableWidget(self.groupBox_2)
        self.table_outros.setGeometry(QtCore.QRect(230, 50, 120, 371))
        self.table_outros.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.table_outros.setObjectName("table_outros")
        self.table_outros.setColumnCount(2)
        self.table_outros.setRowCount(16)
        item = QtWidgets.QTableWidgetItem()
        self.table_outros.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_outros.setHorizontalHeaderItem(1, item)
        self.table_outros.horizontalHeader().setVisible(False)
        self.table_outros.horizontalHeader().setDefaultSectionSize(60)
        self.table_outros.verticalHeader().setDefaultSectionSize(23)
        self.button_salvar = QtWidgets.QPushButton(self.centralwidget)
        self.button_salvar.setGeometry(QtCore.QRect(250, 620, 141, 31))
        self.button_salvar.setObjectName("button_salvar")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 428, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)


        # CODIGO ESCRITO
        outros = ["Academia", "Churrasqueira", "Jardim", "Piscina", "Playground", "Quadra", "Quintal",
                  "Salão de Festas", "Salão de Jogos", "Aquecimento", "Ar Condicionado", "Elevador",
                  "Vigia", "Área de Serviço", "Escritório", "Varanda"]
        for row in range(len(outros)):
            item = QtWidgets.QTableWidgetItem()
            self.table_outros.setHorizontalHeaderItem(row, item)
        self.table_outros.setVerticalHeaderLabels(outros)

        estados = ["", "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA",
                    "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]
        for uf in estados:
            self.combo_estado.addItem(uf)

        tipos_imoveis = ['Apartamento', 'Casa', 'Cobertura', 'Chácara', 'Flat', 'Kitnet', 'Lote']
        for tipo in tipos_imoveis:
            self.combo_tipo.addItem(tipo)

        self.janelaPrincipal = janelaPrincipal

        self.table_outros.hideColumn(1)
        self.table_distancias.hideColumn(1)
        for row in range(self.table_outros.rowCount()):
            checkBoxItem = QtWidgets.QTableWidgetItem()
            checkBoxItem.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            checkBoxItem.setCheckState(QtCore.Qt.Unchecked)
            self.table_outros.setItem(row, 0, checkBoxItem)

        self.modo = modo
        if self.modo == 'editar':
            self.id = id
            self.preencher_informacoes()

        self.button_calcular.clicked.connect(lambda: self.calcular_distancias())
        self.button_salvar.clicked.connect(lambda: self.salvar())
        self.combo_estado.activated.connect(lambda: self.buscar_cidades_por_uf(self.combo_estado.currentText()))

        self.distancias = []
        self.outros = []

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "Endereço"))
        self.label_2.setText(_translate("MainWindow", "Cidade"))
        self.label.setText(_translate("MainWindow", "Estado"))
        self.label_3.setText(_translate("MainWindow", "Bairro"))
        self.label_4.setText(_translate("MainWindow", "Rua"))
        self.label_5.setText(_translate("MainWindow", "Número"))
        self.label_6.setText(_translate("MainWindow", "Complemento"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Informações Principais"))
        self.label_7.setText(_translate("MainWindow", "Tipo Imóvel"))
        self.label_8.setText(_translate("MainWindow", "Área"))
        self.label_9.setText(_translate("MainWindow", "Aluguel"))
        self.label_10.setText(_translate("MainWindow", "Quartos"))
        self.label_11.setText(_translate("MainWindow", "Banheiros"))
        self.label_12.setText(_translate("MainWindow", "Garagem"))
        self.button_calcular.setText(_translate("MainWindow", "Calcular Distancias"))
        item = self.table_distancias.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "Shopping"))
        item = self.table_distancias.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "Supermercado"))
        item = self.table_distancias.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "Farmácia"))
        item = self.table_distancias.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "Academia"))
        item = self.table_distancias.verticalHeaderItem(4)
        item.setText(_translate("MainWindow", "Hospital"))
        item = self.table_distancias.verticalHeaderItem(5)
        item.setText(_translate("MainWindow", "Estação de Metrô"))
        item = self.table_distancias.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Distancia"))
        item = self.table_distancias.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Código"))
        item = self.table_outros.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Check"))
        item = self.table_outros.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Código"))
        self.button_salvar.setText(_translate("MainWindow", "Salvar"))

