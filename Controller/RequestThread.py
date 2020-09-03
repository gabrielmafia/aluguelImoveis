from PyQt5 import QtCore, QtGui, QtWidgets
import requests, json
from Controller.calculadorDistancia import encontrar_locais_de_interesse_mais_proximos


class ThreadUF(QtCore.QThread):
    '''
    Classe que cria uma nova thread em que será executado o request do site do ibge
    para obter os municípios do estado solicitado.
    '''
    sinal = QtCore.pyqtSignal(object)
    sinal_erro = QtCore.pyqtSignal(object)

    def __init__(self, url):
        QtCore.QThread.__init__(self)
        self.url = url

    def run(self):
        try:
            request = requests.get(self.url).content.decode('utf-8')
            json_data = json.loads(request)
            self.sinal.emit(json_data)
        except requests.exceptions.RequestException as e:
            self.sinal_erro.emit(e)


class ThreadDistancias(QtCore.QThread):
    '''
    classe que cria uma nova thread em que será executado a função responsável por encontrar as distancias dos locais
    de interesse mais próximos do endereço fornecido
    '''
    sinal = QtCore.pyqtSignal(object)
    sinal_erro = QtCore.pyqtSignal(object)

    def __init__(self, endereco, locais):
        QtCore.QThread.__init__(self)
        self.endereco = endereco
        self.locais = locais

    def run(self):
        distancias = encontrar_locais_de_interesse_mais_proximos(self.endereco, self.locais)
        self.sinal.emit(distancias)
