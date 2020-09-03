from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from DAO.cadastroDAO import Imovel


class Ui_janelaVisualizacao(object):
    def preencher_informacoes(self):
        '''
            Método responsável por preencher as informações dos campos editáveis com as informações do imóvel contidas
            no banco de dados SQL.
         '''

        imovel = Imovel
        query = imovel.PesquisarImovelPorId(imovel, self.id)
        query.next()

        endereco = f"{str(query.value(1))} {str(query.value(2))} {str(query.value(3))}"
        self.label_endereco.setText(endereco)  # endereco
        self.label_bairro.setText(str(query.value(4)))
        self.label_estado.setText(str(query.value(6)))
        self.label_cidade.setText(str(query.value(5)))
        self.label_tipo.setText(str(query.value(8)))
        self.label_area.setText(f"{str(query.value(9))} m²")
        self.label_preco.setText(f"R${query.value(10):.2f}")
        self.label_banheiros.setText(f"{query.value(11)} banheiro(s)")
        self.label_quartos.setText(f"{query.value(12)} quarto(s)")
        self.label_garagem.setText(f"{query.value(13)} vaga(s) garagem")

        locais = ["Shopping", "Supermercado", "Farmácia", "Academia", "Hospital", "Estação de Metrô"]
        try:
            distancias = str(query.value(14)).split(';')
            for row in range(len(distancias)):
                self.label_distancias.setText(self.label_distancias.text() + "\n" + locais[row] + ": " + distancias[row])
        except:
            pass

        outros = ["Academia", "Churrasqueira", "Jardim", "Piscina", "Playground", "Quadra", "Quintal",
                  "Salão de Festas", "Salão de Jogos", "Aquecimento", "Ar Condicionado", "Elevador",
                  "Vigia", "Área de Serviço", "Escritório", "Varanda"]
        outros_bool = str(query.value(15))
        for idx in range(len(outros_bool)):
            if outros_bool[idx] == '1':
                self.label_outros.setText(self.label_outros.text() + "\n" + outros[idx])


    def passar_foto(self):
        pass

    def setupUi(self, MainWindow, id):

        # SETUP GERADO PELO QTDESINGER

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(941, 409)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_fotos = QtWidgets.QLabel(self.centralwidget)
        self.label_fotos.setGeometry(QtCore.QRect(0, 0, 421, 341))
        self.label_fotos.setObjectName("label_fotos")
        self.button_proximo = QtWidgets.QPushButton(self.centralwidget)
        self.button_proximo.setGeometry(QtCore.QRect(210, 350, 41, 31))
        self.button_proximo.setObjectName("button_proximo")
        self.button_anterior = QtWidgets.QPushButton(self.centralwidget)
        self.button_anterior.setGeometry(QtCore.QRect(170, 350, 41, 31))
        self.button_anterior.setObjectName("button_anterior")
        self.label_endereco = QtWidgets.QLabel(self.centralwidget)
        self.label_endereco.setGeometry(QtCore.QRect(450, 20, 291, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_endereco.setFont(font)
        self.label_endereco.setObjectName("label_endereco")
        self.label_bairro = QtWidgets.QLabel(self.centralwidget)
        self.label_bairro.setGeometry(QtCore.QRect(450, 50, 111, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_bairro.setFont(font)
        self.label_bairro.setObjectName("label_bairro")
        self.label_cidade = QtWidgets.QLabel(self.centralwidget)
        self.label_cidade.setGeometry(QtCore.QRect(570, 50, 120, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_cidade.setFont(font)
        self.label_cidade.setObjectName("label_cidade")
        self.label_estado = QtWidgets.QLabel(self.centralwidget)
        self.label_estado.setGeometry(QtCore.QRect(690, 50, 30, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_estado.setFont(font)
        self.label_estado.setObjectName("label_estado")
        self.label_preco = QtWidgets.QLabel(self.centralwidget)
        self.label_preco.setGeometry(QtCore.QRect(450, 120, 111, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_preco.setFont(font)
        self.label_preco.setObjectName("label_preco")
        self.label_area = QtWidgets.QLabel(self.centralwidget)
        self.label_area.setGeometry(QtCore.QRect(450, 150, 111, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_area.setFont(font)
        self.label_area.setObjectName("label_area")
        self.label_tipo = QtWidgets.QLabel(self.centralwidget)
        self.label_tipo.setGeometry(QtCore.QRect(450, 90, 111, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_tipo.setFont(font)
        self.label_tipo.setObjectName("label_tipo")
        self.label_garagem = QtWidgets.QLabel(self.centralwidget)
        self.label_garagem.setGeometry(QtCore.QRect(580, 150, 141, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_garagem.setFont(font)
        self.label_garagem.setObjectName("label_garagem")
        self.label_quartos = QtWidgets.QLabel(self.centralwidget)
        self.label_quartos.setGeometry(QtCore.QRect(580, 90, 131, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_quartos.setFont(font)
        self.label_quartos.setObjectName("label_quartos")
        self.label_banheiros = QtWidgets.QLabel(self.centralwidget)
        self.label_banheiros.setGeometry(QtCore.QRect(580, 120, 131, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_banheiros.setFont(font)
        self.label_banheiros.setObjectName("label_banheiros")
        self.label_distancias = QtWidgets.QLabel(self.centralwidget)
        self.label_distancias.setGeometry(QtCore.QRect(450, 190, 201, 161))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_distancias.setFont(font)
        self.label_distancias.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_distancias.setObjectName("label_distancias")
        self.label_outros = QtWidgets.QLabel(self.centralwidget)
        self.label_outros.setGeometry(QtCore.QRect(760, 20, 161, 321))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_outros.setFont(font)
        self.label_outros.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_outros.setObjectName("label_outros")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 941, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        # CODIGO ESCRITO
        pixmap = QPixmap('Imagens\semfoto.jpg')
        self.label_fotos.setPixmap(pixmap)

        self.id = id
        self.preencher_informacoes()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Visualizar Imóvel"))
        self.button_proximo.setText(_translate("MainWindow", ">"))
        self.button_anterior.setText(_translate("MainWindow", "<"))
