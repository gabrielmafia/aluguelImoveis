from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QTableWidgetItem
from View.janelaCadastro import Ui_janelaCadastro
from View.janelaVisualizacao import Ui_janelaVisualizacao
from DAO.cadastroDAO import Imovel
from View.mensagens import Mensagem

class Ui_janelaPrincipal(object):
    def cadastrar_novo_imovel(self):
        '''
        abre uma janela em que será cadastrado um novo imóvel
        '''
        self.jCadastro = QtWidgets.QMainWindow()
        self.ui_jCadastro = Ui_janelaCadastro()
        self.ui_jCadastro.setupUi(self.jCadastro, 'inserir', None, self)
        self.jCadastro.show()

    def editar_imovel(self, row):
        '''
        abre uma janela em que as informações do imovel selecionado poderão ser modificados
        '''
        if row >= 0:
            imovel_id = self.table_imoveis.item(row, 0).text()
            self.jCadastro = QtWidgets.QMainWindow()
            self.ui_jCadastro = Ui_janelaCadastro()
            self.ui_jCadastro.setupUi(self.jCadastro, 'editar', imovel_id, self)
            self.jCadastro.show()

    def deletar_imovel(self, row):
        '''
        remove um imovel da tabela e do banco de dados
        '''
        if row >= 0:
            imovel_id = self.table_imoveis.item(row, 0).text()
            imovel = Imovel
            imovel.ExcluirImovel(imovel, imovel_id)
            self.table_imoveis.removeRow(row)


    def vizualizar_imovel(self, row):
        '''
        abre janela de visualização de um imovel da tabela
        '''
        if row >= 0:
            imovel_id = self.table_imoveis.item(row, 0).text()
            self.jVizualizacao = QtWidgets.QMainWindow()
            self.ui_jVizualizacao = Ui_janelaVisualizacao()
            self.ui_jVizualizacao.setupUi(self.jVizualizacao, imovel_id)
            self.jVizualizacao.show()

    def pesquisar_imoveis(self):
        '''
        metodo que busca no banco de dados todos os imoveis no cadastro e os adiciona à tabela
        '''

        imoveis = Imovel
        query = imoveis.PesquisarImovel(imoveis)
        if query.lastError().type() > 0:
            msg = Mensagem
            msg.erroAoPesquisarDB(msg)
        else:
            for row in range(self.table_imoveis.rowCount()):
                self.table_imoveis.removeRow(0)

            row = 0
            while query.next():
                self.table_imoveis.insertRow(row)
                self.table_imoveis.setItem(row, 0, QTableWidgetItem(str(query.value(0))))   # id
                endereco = f"{str(query.value(1))} {str(query.value(2))} {str(query.value(3))}"
                self.table_imoveis.setItem(row, 1, QTableWidgetItem(endereco))              # endereco
                self.table_imoveis.setItem(row, 2, QTableWidgetItem(str(query.value(4))))   # bairro
                self.table_imoveis.setItem(row, 3, QTableWidgetItem(str(query.value(5))))   # cidade
                self.table_imoveis.setItem(row, 4, QTableWidgetItem(str(query.value(6))))   # estado
                self.table_imoveis.setItem(row, 5, QTableWidgetItem(str(query.value(12))))  # quartos
                self.table_imoveis.setItem(row, 6, QTableWidgetItem(str(query.value(11))))  # banheiros
                self.table_imoveis.setItem(row, 7, QTableWidgetItem(str(query.value(13))))  # garagem
                self.table_imoveis.setItem(row, 8, QTableWidgetItem(str(query.value(8))))   # tipo imovel
                self.table_imoveis.setItem(row, 9, QTableWidgetItem(str(query.value(9))))   # area
                self.table_imoveis.setItem(row, 10, QTableWidgetItem(str(query.value(10))))  # preco aluguel

                row += 1
        self.filtrar_tabela()

    def filtrar_tabela(self):
        '''
        função responsável por filtrar a tabela. Seu funcionamento consiste em pegar os valores dos filtros e
        esconder as linhas que não atendem ao requerido.
        '''
        filtro_estado = self.combo_estado.currentText()
        filtro_cidade = self.edt_cidade.text()
        filtro_bairro = self.edt_bairro.text()
        filtro_tipo_imovel = self.combo_tipo.currentText()
        filtro_area_min = self.spin_area_min.value()
        filtro_area_max = self.spin_area_max.value()
        filtro_preco_min = self.spin_preco_min.value()
        filtro_preco_max = self.spin_preco_max.value()
        filtro_quartos = self.spin_quartos.value()
        filtro_banheiros = self.spin_banheiros.value()
        filtro_garagem = self.spin_garagem.value()

        for row in range(self.table_imoveis.rowCount()):
            bairro = self.table_imoveis.item(row, 2).text()
            cidade = self.table_imoveis.item(row, 3).text()
            estado = self.table_imoveis.item(row, 4).text()
            quartos = int(self.table_imoveis.item(row, 5).text())
            banheiros = int(self.table_imoveis.item(row, 6).text())
            garagem = int(self.table_imoveis.item(row, 7).text())
            tipo_imovel = self.table_imoveis.item(row, 8).text()
            area = int(self.table_imoveis.item(row, 9).text())
            preco = float(self.table_imoveis.item(row, 10).text())

            if filtro_bairro.lower() not in bairro.lower() \
                    or filtro_cidade.lower() not in cidade.lower() \
                    or filtro_estado not in estado \
                    or filtro_tipo_imovel.lower() not in tipo_imovel\
                    or filtro_quartos > quartos\
                    or filtro_banheiros > banheiros\
                    or filtro_garagem > garagem\
                    or filtro_area_min > area\
                    or filtro_area_max < area\
                    or filtro_preco_min > preco\
                    or filtro_preco_max < preco:
                self.table_imoveis.setRowHidden(row, True)
            else:
                self.table_imoveis.setRowHidden(row, False)

    def setupUi(self, MainWindow):
        '''
        setup da janela principal em que serão exibidos todos os imoveis em uma tabela alem de opções de filtragem
        parte deste codigo foi gerado com o QtDesigner https://doc.qt.io/qt-5/qtdesigner-manual.html
        '''
        # SETUP GERADO PELO QTDESINGER ==========================================================

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1151, 871)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 1151, 101))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label_image = QtWidgets.QLabel(self.frame)
        self.label_image.setGeometry(QtCore.QRect(-40, -20, 1201, 131))
        self.label_image.setObjectName("label_image")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(0, 100, 1151, 101))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.combo_estado = QtWidgets.QComboBox(self.frame_2)
        self.combo_estado.setGeometry(QtCore.QRect(10, 30, 69, 22))
        self.combo_estado.setObjectName("combo_estado")
        self.edt_cidade = QtWidgets.QLineEdit(self.frame_2)
        self.edt_cidade.setGeometry(QtCore.QRect(90, 30, 113, 20))
        self.edt_cidade.setObjectName("edt_cidade")
        self.edt_bairro = QtWidgets.QLineEdit(self.frame_2)
        self.edt_bairro.setGeometry(QtCore.QRect(220, 30, 113, 20))
        self.edt_bairro.setObjectName("edt_bairro")
        self.spin_quartos = QtWidgets.QSpinBox(self.frame_2)
        self.spin_quartos.setGeometry(QtCore.QRect(890, 10, 42, 22))
        self.spin_quartos.setObjectName("spin_quartos")
        self.spin_banheiros = QtWidgets.QSpinBox(self.frame_2)
        self.spin_banheiros.setGeometry(QtCore.QRect(890, 40, 42, 22))
        self.spin_banheiros.setObjectName("spin_banheiros")
        self.spin_garagem = QtWidgets.QSpinBox(self.frame_2)
        self.spin_garagem.setGeometry(QtCore.QRect(890, 70, 42, 22))
        self.spin_garagem.setObjectName("spin_garagem")
        self.spin_preco_min = QtWidgets.QDoubleSpinBox(self.frame_2)
        self.spin_preco_min.setGeometry(QtCore.QRect(731, 30, 81, 22))
        self.spin_preco_min.setMaximum(999999.99)
        self.spin_preco_min.setObjectName("spin_preco_min")
        self.spin_preco_max = QtWidgets.QDoubleSpinBox(self.frame_2)
        self.spin_preco_max.setGeometry(QtCore.QRect(731, 60, 81, 22))
        self.spin_preco_max.setMaximum(99999.0)
        self.spin_preco_max.setObjectName("spin_preco_max")
        self.spin_area_min = QtWidgets.QSpinBox(self.frame_2)
        self.spin_area_min.setGeometry(QtCore.QRect(591, 30, 61, 22))
        self.spin_area_min.setMaximum(99999)
        self.spin_area_min.setObjectName("spin_area_min")
        self.spin_area_max = QtWidgets.QSpinBox(self.frame_2)
        self.spin_area_max.setGeometry(QtCore.QRect(591, 60, 61, 22))
        self.spin_area_max.setMaximum(9999)
        self.spin_area_max.setObjectName("spin_area_max")
        self.combo_tipo = QtWidgets.QComboBox(self.frame_2)
        self.combo_tipo.setGeometry(QtCore.QRect(360, 30, 111, 22))
        self.combo_tipo.setObjectName("combo_tipo")
        self.combo_tipo.addItem("")
        self.combo_tipo.setItemText(0, "")
        self.combo_tipo.addItem("")
        self.combo_tipo.addItem("")
        self.combo_tipo.addItem("")
        self.combo_tipo.addItem("")
        self.combo_tipo.addItem("")
        self.combo_tipo.addItem("")
        self.combo_tipo.addItem("")
        self.label = QtWidgets.QLabel(self.frame_2)
        self.label.setGeometry(QtCore.QRect(10, 10, 47, 13))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.frame_2)
        self.label_2.setGeometry(QtCore.QRect(90, 10, 47, 13))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.frame_2)
        self.label_3.setGeometry(QtCore.QRect(220, 10, 47, 13))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.frame_2)
        self.label_4.setGeometry(QtCore.QRect(520, 30, 71, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.frame_2)
        self.label_5.setGeometry(QtCore.QRect(520, 60, 61, 16))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.frame_2)
        self.label_6.setGeometry(QtCore.QRect(660, 30, 71, 16))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.frame_2)
        self.label_7.setGeometry(QtCore.QRect(660, 60, 71, 16))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.frame_2)
        self.label_8.setGeometry(QtCore.QRect(830, 10, 47, 13))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.frame_2)
        self.label_9.setGeometry(QtCore.QRect(830, 40, 51, 16))
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.frame_2)
        self.label_10.setGeometry(QtCore.QRect(830, 70, 47, 13))
        self.label_10.setObjectName("label_10")
        self.button_adcionar = QtWidgets.QPushButton(self.frame_2)
        self.button_adcionar.setGeometry(QtCore.QRect(1009, 5, 121, 70))
        self.button_adcionar.setObjectName("button_adcionar")
        self.button_remover = QtWidgets.QPushButton(self.frame_2)
        self.button_remover.setGeometry(QtCore.QRect(1069, 75, 61, 23))
        self.button_remover.setObjectName("button_remover")
        self.button_editar = QtWidgets.QPushButton(self.frame_2)
        self.button_editar.setGeometry(QtCore.QRect(1010, 75, 61, 23))
        self.button_editar.setObjectName("button_editar")
        self.label_11 = QtWidgets.QLabel(self.frame_2)
        self.label_11.setGeometry(QtCore.QRect(360, 10, 111, 16))
        self.label_11.setObjectName("label_11")
        self.frame_3 = QtWidgets.QFrame(self.centralwidget)
        self.frame_3.setGeometry(QtCore.QRect(0, 200, 1151, 641))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.table_imoveis = QtWidgets.QTableWidget(self.frame_3)
        self.table_imoveis.setGeometry(QtCore.QRect(0, 0, 1151, 631))
        self.table_imoveis.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table_imoveis.setAlternatingRowColors(True)
        self.table_imoveis.setObjectName("table_imoveis")
        self.table_imoveis.setColumnCount(11)
        self.table_imoveis.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.table_imoveis.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_imoveis.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_imoveis.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_imoveis.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_imoveis.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_imoveis.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_imoveis.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_imoveis.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_imoveis.setHorizontalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_imoveis.setHorizontalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_imoveis.setHorizontalHeaderItem(10, item)
        self.table_imoveis.horizontalHeader().setStretchLastSection(True)
        self.table_imoveis.verticalHeader().setVisible(False)
        self.table_imoveis.verticalHeader().setDefaultSectionSize(40)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1151, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # CODIGO ESCRITO =============================================================
        estados = ["", "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA",
                    "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]
        for uf in estados:
            self.combo_estado.addItem(uf)

        pixmap = QPixmap("Imagens\\banner.png")
        self.label_image.setPixmap(pixmap)

        self.table_imoveis.hideColumn(0)
        column_widths = [0, 300, 120, 120, 60, 60, 60, 60, 100, 80, 120]
        for col, width in enumerate(column_widths):
            self.table_imoveis.setColumnWidth(col, width)

        self.button_adcionar.clicked.connect(lambda: self.cadastrar_novo_imovel())
        self.button_editar.clicked.connect(lambda: self.editar_imovel(self.table_imoveis.currentRow()))
        self.button_remover.clicked.connect(lambda: self.deletar_imovel(self.table_imoveis.currentRow()))
        self.table_imoveis.doubleClicked.connect(lambda: self.vizualizar_imovel(self.table_imoveis.currentRow()))

        self.combo_estado.activated.connect(lambda: self.filtrar_tabela())
        self.edt_cidade.editingFinished.connect(lambda: self.filtrar_tabela())
        self.edt_cidade.editingFinished.connect(lambda: self.filtrar_tabela())
        self.combo_tipo.activated.connect(lambda: self.filtrar_tabela())
        self.spin_area_min.editingFinished.connect(lambda: self.filtrar_tabela())
        self.spin_area_max.editingFinished.connect(lambda: self.filtrar_tabela())
        self.spin_preco_min.editingFinished.connect(lambda: self.filtrar_tabela())
        self.spin_preco_max.editingFinished.connect(lambda: self.filtrar_tabela())
        self.spin_banheiros.editingFinished.connect(lambda: self.filtrar_tabela())
        self.spin_quartos.editingFinished.connect(lambda: self.filtrar_tabela())
        self.spin_garagem.editingFinished.connect(lambda: self.filtrar_tabela())

        self.spin_area_max.setValue(self.spin_area_max.maximum())
        self.spin_preco_max.setValue(self.spin_preco_max.maximum())

        self.pesquisar_imoveis()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.combo_tipo.setItemText(1, _translate("MainWindow", "Apartamento"))
        self.combo_tipo.setItemText(2, _translate("MainWindow", "Casa"))
        self.combo_tipo.setItemText(3, _translate("MainWindow", "Cobertura"))
        self.combo_tipo.setItemText(4, _translate("MainWindow", "Chácara"))
        self.combo_tipo.setItemText(5, _translate("MainWindow", "Flat"))
        self.combo_tipo.setItemText(6, _translate("MainWindow", "Kitnet"))
        self.combo_tipo.setItemText(7, _translate("MainWindow", "Lote"))
        self.label.setText(_translate("MainWindow", "Estado"))
        self.label_2.setText(_translate("MainWindow", "Cidade"))
        self.label_3.setText(_translate("MainWindow", "Bairro"))
        self.label_4.setText(_translate("MainWindow", "Área Mínima"))
        self.label_5.setText(_translate("MainWindow", "Área Máxima"))
        self.label_6.setText(_translate("MainWindow", "Preço Mínimo"))
        self.label_7.setText(_translate("MainWindow", "Preço Máximo"))
        self.label_8.setText(_translate("MainWindow", "Quartos"))
        self.label_9.setText(_translate("MainWindow", "Banheiros"))
        self.label_10.setText(_translate("MainWindow", "Garagem"))
        self.button_adcionar.setText(_translate("MainWindow", "+"))
        self.button_remover.setText(_translate("MainWindow", "-"))
        self.button_editar.setText(_translate("MainWindow", "Editar"))
        self.label_11.setText(_translate("MainWindow", "Tipo de Imóvel"))
        self.table_imoveis.setSortingEnabled(True)
        item = self.table_imoveis.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "id"))
        item = self.table_imoveis.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Endereço"))
        item = self.table_imoveis.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Bairro"))
        item = self.table_imoveis.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Cidade"))
        item = self.table_imoveis.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Estado"))
        item = self.table_imoveis.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Quartos"))
        item = self.table_imoveis.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Banheiros"))
        item = self.table_imoveis.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "Garagem"))
        item = self.table_imoveis.horizontalHeaderItem(8)
        item.setText(_translate("MainWindow", "Imóvel"))
        item = self.table_imoveis.horizontalHeaderItem(9)
        item.setText(_translate("MainWindow", "Área"))
        item = self.table_imoveis.horizontalHeaderItem(10)
        item.setText(_translate("MainWindow", "Aluguel"))
