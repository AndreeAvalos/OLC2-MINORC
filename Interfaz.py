from PyQt5 import QtCore, QtGui, QtWidgets
from QCodeEditor import *
import Gramatica
from Traducir import Traducir

class Interfaz(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1015, 806)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.new_file = QtWidgets.QPushButton(self.centralwidget)
        self.new_file.setGeometry(QtCore.QRect(0, 0, 71, 61))
        self.new_file.setObjectName("new_file")
        self.save_file = QtWidgets.QPushButton(self.centralwidget)
        self.save_file.setGeometry(QtCore.QRect(70, 0, 71, 61))
        self.save_file.setObjectName("save_file")
        self.save_file_as = QtWidgets.QPushButton(self.centralwidget)
        self.save_file_as.setGeometry(QtCore.QRect(140, 0, 71, 61))
        self.save_file_as.setObjectName("save_file_as")
        self.ejecutar = QtWidgets.QPushButton(self.centralwidget)
        self.ejecutar.setGeometry(QtCore.QRect(240, 0, 71, 61))
        self.ejecutar.setObjectName("ejecutar")
        self.ejecutar.clicked.connect(self.traducir)
        self.depurar = QtWidgets.QPushButton(self.centralwidget)
        self.depurar.setGeometry(QtCore.QRect(310, 0, 71, 61))
        self.depurar.setObjectName("depurar")
        self.parar = QtWidgets.QPushButton(self.centralwidget)
        self.parar.setGeometry(QtCore.QRect(380, 0, 71, 61))
        self.parar.setObjectName("parar")
        self.step_step = QtWidgets.QPushButton(self.centralwidget)
        self.step_step.setGeometry(QtCore.QRect(450, 0, 71, 61))
        self.step_step.setObjectName("step_step")
        self.continuar = QtWidgets.QPushButton(self.centralwidget)
        self.continuar.setGeometry(QtCore.QRect(520, 0, 71, 61))
        self.continuar.setObjectName("continuar")
        self.tema = QtWidgets.QPushButton(self.centralwidget)
        self.tema.setGeometry(QtCore.QRect(640, 0, 71, 61))
        self.tema.setObjectName("tema")
        self.lineas = QtWidgets.QPushButton(self.centralwidget)
        self.lineas.setGeometry(QtCore.QRect(710, 0, 71, 61))
        self.lineas.setObjectName("lineas")
        self.editor = QtWidgets.QTabWidget(self.centralwidget)
        self.editor.setGeometry(QtCore.QRect(10, 80, 661, 421))
        self.editor.setObjectName("editor")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.plainTextEdit = QCodeEditor(DISPLAY_LINE_NUMBERS=True, 
                             HIGHLIGHT_CURRENT_LINE=True,
                             SyntaxHighlighter=XMLHighlighter)                
        self.plainTextEdit.setGeometry(QtCore.QRect(10, 10, 631, 371))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.plainTextEdit.setParent(self.tab)
        self.editor.addTab(self.tab, "")  
        self.editor.addTab(self.tab, "")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(690, 80, 61, 16))
        self.label.setObjectName("label")
        self.codigo_3d = QtWidgets.QListWidget(self.centralwidget)
        self.codigo_3d.setGeometry(QtCore.QRect(680, 100, 321, 401))
        self.codigo_3d.setObjectName("codigo_3d")
        self.codigo_optimizado = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.codigo_optimizado.setGeometry(QtCore.QRect(10, 530, 661, 221))
        self.codigo_optimizado.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.codigo_optimizado.setObjectName("codigo_optimizado")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 510, 111, 16))
        self.label_2.setObjectName("label_2")
        self.tabla_cuadruplos = QtWidgets.QTableWidget(self.centralwidget)
        self.tabla_cuadruplos.setGeometry(QtCore.QRect(680, 530, 321, 221))
        self.tabla_cuadruplos.setObjectName("tabla_cuadruplos")
        self.tabla_cuadruplos.setColumnCount(4)
        self.tabla_cuadruplos.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tabla_cuadruplos.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabla_cuadruplos.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabla_cuadruplos.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabla_cuadruplos.setHorizontalHeaderItem(3, item)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(690, 510, 71, 16))
        self.label_3.setObjectName("label_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1015, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuReporte = QtWidgets.QMenu(self.menubar)
        self.menuReporte.setObjectName("menuReporte")
        self.menuRun = QtWidgets.QMenu(self.menubar)
        self.menuRun.setObjectName("menuRun")
        self.menuayuda = QtWidgets.QMenu(self.menubar)
        self.menuayuda.setObjectName("menuayuda")
        MainWindow.setMenuBar(self.menubar)
        self.actionEjecutar = QtWidgets.QAction(MainWindow)
        self.actionEjecutar.setObjectName("actionEjecutar")
        self.actionDebug = QtWidgets.QAction(MainWindow)
        self.actionDebug.setObjectName("actionDebug")
        self.actionArbol_Ascendente = QtWidgets.QAction(MainWindow)
        self.actionArbol_Ascendente.setObjectName("actionArbol_Ascendente")
        self.actionDGA = QtWidgets.QAction(MainWindow)
        self.actionDGA.setObjectName("actionDGA")
        self.actionAbrir = QtWidgets.QAction(MainWindow)
        self.actionAbrir.setObjectName("actionAbrir")
        self.actionGuardar = QtWidgets.QAction(MainWindow)
        self.actionGuardar.setObjectName("actionGuardar")
        self.actionGuardar_como = QtWidgets.QAction(MainWindow)
        self.actionGuardar_como.setObjectName("actionGuardar_como")
        self.actionBuscar = QtWidgets.QAction(MainWindow)
        self.actionBuscar.setObjectName("actionBuscar")
        self.actionReemplazar = QtWidgets.QAction(MainWindow)
        self.actionReemplazar.setObjectName("actionReemplazar")
        self.actionTabla_de_Simbolos = QtWidgets.QAction(MainWindow)
        self.actionTabla_de_Simbolos.setObjectName("actionTabla_de_Simbolos")
        self.actionErrores_Lexicos_y_Sintacticos = QtWidgets.QAction(MainWindow)
        self.actionErrores_Lexicos_y_Sintacticos.setObjectName("actionErrores_Lexicos_y_Sintacticos")
        self.menuFile.addAction(self.actionAbrir)
        self.menuFile.addAction(self.actionGuardar)
        self.menuFile.addAction(self.actionGuardar_como)
        self.menuFile.addAction(self.actionBuscar)
        self.menuFile.addAction(self.actionReemplazar)
        self.menuReporte.addAction(self.actionArbol_Ascendente)
        self.menuReporte.addAction(self.actionDGA)
        self.menuReporte.addAction(self.actionTabla_de_Simbolos)
        self.menuReporte.addAction(self.actionErrores_Lexicos_y_Sintacticos)
        self.menuRun.addAction(self.actionEjecutar)
        self.menuRun.addAction(self.actionDebug)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuReporte.menuAction())
        self.menubar.addAction(self.menuRun.menuAction())
        self.menubar.addAction(self.menuayuda.menuAction())

        self.retranslateUi(MainWindow)
        self.editor.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def traducir(self):
        tab = self.editor.widget(self.editor.currentIndex())
        items = tab.children()
        codigo = items[0].toPlainText()
        print(codigo)
        ast = Gramatica.parse(codigo)
        self.codigo_3d.clear()
        traducir = Traducir(args=(ast,self.tabla_cuadruplos, self.codigo_3d),daemon=True)
        traducir.start()


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MinorC"))
        self.new_file.setText(_translate("MainWindow", "Nuevo"))
        self.save_file.setText(_translate("MainWindow", "Save"))
        self.save_file_as.setText(_translate("MainWindow", "Save as.."))
        self.ejecutar.setText(_translate("MainWindow", "Ejecutar"))
        self.depurar.setText(_translate("MainWindow", "Depurar"))
        self.parar.setText(_translate("MainWindow", "Parar"))
        self.step_step.setText(_translate("MainWindow", "->"))
        self.continuar.setText(_translate("MainWindow", "|>"))
        self.tema.setText(_translate("MainWindow", "Tema"))
        self.lineas.setText(_translate("MainWindow", "Lineas"))
        self.editor.setTabText(self.editor.indexOf(self.tab), _translate("MainWindow", "Tab 1"))
        self.label.setText(_translate("MainWindow", "Codigo 3D"))
        self.label_2.setText(_translate("MainWindow", "Codigo 3D optimizado"))
        item = self.tabla_cuadruplos.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "op"))
        item = self.tabla_cuadruplos.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "arg1"))
        item = self.tabla_cuadruplos.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "arg2"))
        item = self.tabla_cuadruplos.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "result"))
        self.label_3.setText(_translate("MainWindow", "Cuadruplos"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuReporte.setTitle(_translate("MainWindow", "Reporte"))
        self.menuRun.setTitle(_translate("MainWindow", "Run"))
        self.menuayuda.setTitle(_translate("MainWindow", "Help"))
        self.actionEjecutar.setText(_translate("MainWindow", "Ejecutar"))
        self.actionDebug.setText(_translate("MainWindow", "Debug"))
        self.actionArbol_Ascendente.setText(_translate("MainWindow", "Arbol Ascendente"))
        self.actionDGA.setText(_translate("MainWindow", "DGA"))
        self.actionAbrir.setText(_translate("MainWindow", "Abrir"))
        self.actionGuardar.setText(_translate("MainWindow", "Guardar"))
        self.actionGuardar_como.setText(_translate("MainWindow", "Guardar como.."))
        self.actionBuscar.setText(_translate("MainWindow", "Buscar"))
        self.actionReemplazar.setText(_translate("MainWindow", "Reemplazar"))
        self.actionTabla_de_Simbolos.setText(_translate("MainWindow", "Tabla de Simbolos"))
        self.actionErrores_Lexicos_y_Sintacticos.setText(_translate("MainWindow", "Errores Lexicos y Sintacticos"))
