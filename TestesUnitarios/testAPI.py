import unittest
from Controller.calculadorDistancia import encontrar_locais_de_interesse_mais_proximos as funcao_api

locais = ['Hospital', 'Farmácia']
resposta_vazia = {'Hospital': '0 m', 'Farmácia': '0 m'}

class TestAPI(unittest.TestCase):
    def test_endereco_vazio(self):
        self.assertEqual(funcao_api('', locais), resposta_vazia)

    def test_endereco_valido(self):
        endereco = 'R. Teixeira de Freitas 478 Santo Antonio Belo Horizonte MG'
        resposta = {'Hospital': '0.9 km', 'Farmácia': '0.2 km'}

        self.assertEqual(funcao_api(endereco, locais), resposta)

    def test_endereco_invalido(self):
        self.assertEqual(funcao_api('ahs98da8d8ajdp88 a 89vh', locais), resposta_vazia)


unittest.main()
