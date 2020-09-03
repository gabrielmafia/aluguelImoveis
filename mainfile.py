from View.janelaPrincipal import *
import sys

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    janelaPrincipal = QtWidgets.QMainWindow()
    ui = Ui_janelaPrincipal()
    ui.setupUi(janelaPrincipal)
    janelaPrincipal.show()
    sys.exit(app.exec_())

