from PyQt5 import QtCore, QtGui, QtWidgets
import Gramatica
import GramaticaGDA 
import GramaticaM
from Traducir import Traducir
from Depurar import Depurar
from PyQt5.Qsci import QsciLexerCPP, QsciScintilla
from augus.HilosGraficar import *
from augus.Recolectar import Recolectar
from augus.Ejecutar import Ejecutor
import augus.GramaticaA as GramaticaA
from augus.TablaSimbolosA import TablaSimbolosA as TSA
from PyQt5.QtWidgets import QInputDialog, QLineEdit,QMainWindow
from Visor import Visor
traducir = None
class PlainTextEdit(QtWidgets.QTextEdit):
    

    def keyPressEvent(self, event):
        global traducir
        if event.key() == QtCore.Qt.Key_Return:
            salida = self.toPlainText()
            lineas = salida.split("\n")
            traducir.setParams(lineas[len(lineas)-1],True)

        super(PlainTextEdit, self).keyPressEvent(event)

        

class Interfaz(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1349, 806)
        self.mw = MainWindow
        self.puntos_break = []
        self.rutaTemp = ""
        self.pestañas = {}
        self.nombre = ""
        self.gc = False

        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.PlaceholderText, brush)
        MainWindow.setPalette(palette)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.new_file = QtWidgets.QPushButton(self.centralwidget)
        self.new_file.setGeometry(QtCore.QRect(0, 0, 71, 61))
        self.new_file.setObjectName("new_file")
        self.new_file.clicked.connect(self.agregar_tab)
        self.save_file = QtWidgets.QPushButton(self.centralwidget)
        self.save_file.setGeometry(QtCore.QRect(70, 0, 71, 61))
        self.save_file.setObjectName("save_file")
        self.save_file.clicked.connect(self.guardar)
        self.save_file_as = QtWidgets.QPushButton(self.centralwidget)
        self.save_file_as.setGeometry(QtCore.QRect(140, 0, 71, 61))
        self.save_file_as.setObjectName("save_file_as")
        self.save_file_as.clicked.connect(self.guardar_como)
        #boton ejecutar
        self.ejecutar = QtWidgets.QPushButton(self.centralwidget)
        self.ejecutar.setGeometry(QtCore.QRect(240, 0, 71, 61))
        self.ejecutar.setObjectName("ejecutar")
        self.ejecutar.clicked.connect(self.Traducir_Alto_nivel)
        #end ejecutar
        #inico depurar
        self.depurar = QtWidgets.QPushButton(self.centralwidget)
        self.depurar.setGeometry(QtCore.QRect(310, 0, 71, 61))
        self.depurar.setObjectName("depurar")
        self.depurar.clicked.connect(self.Depurar_Alto_nivel)
        #end depurar
        self.parar = QtWidgets.QPushButton(self.centralwidget)
        self.parar.setGeometry(QtCore.QRect(380, 0, 71, 61))
        self.parar.setObjectName("parar")
        self.parar.clicked.connect(self.detenerEjecucion)
        #end parar
        self.step_step = QtWidgets.QPushButton(self.centralwidget)
        self.step_step.setGeometry(QtCore.QRect(450, 0, 71, 61))
        self.step_step.setObjectName("step_step")
        self.step_step.clicked.connect(self.setStep)
        #end step
        self.continuar = QtWidgets.QPushButton(self.centralwidget)
        self.continuar.setGeometry(QtCore.QRect(520, 0, 71, 61))
        self.continuar.setObjectName("continuar")
        self.continuar.clicked.connect(self.setContinuar)
        #end continuar
        self.tema = QtWidgets.QPushButton(self.centralwidget)
        self.tema.setGeometry(QtCore.QRect(640, 0, 71, 61))
        self.tema.setObjectName("tema")
        self.tema.clicked.connect(self.setLines)
        self.lineas = QtWidgets.QPushButton(self.centralwidget)
        self.lineas.setGeometry(QtCore.QRect(710, 0, 71, 61))
        self.lineas.setObjectName("lineas")
        self.lineas.clicked.connect(self.ms_help)
        self.editor = QtWidgets.QTabWidget(self.centralwidget)
        self.editor.setGeometry(QtCore.QRect(10, 80, 661, 421))
        self.editor.setObjectName("editor")
        self.editor.setTabsClosable(True)
        self.editor.tabCloseRequested.connect(self.closeTab)
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.__myFont = QtGui.QFont()
        self.__myFont.setPointSize(11)
        #Principio
        self.plainTextEdit = QsciScintilla(self.tab)
        self.plainTextEdit.setGeometry(QtCore.QRect(10, 10, 631, 371))
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.plainTextEdit.setFont(self.__myFont)
        self.plainTextEdit.setMarginType(0, QsciScintilla.NumberMargin)
        self.plainTextEdit.setMarginWidth(0,"00000")
        self.plainTextEdit.setMarginsForegroundColor(QtGui.QColor("#0C4B72"))
        self.plainTextEdit.markerDefine(QsciScintilla.RightArrow, 0)
        self.plainTextEdit.setMarginSensitivity(0,True)
        self.plainTextEdit.setWrapMode(QsciScintilla.WrapWord)
        self.plainTextEdit.setWrapVisualFlags(QsciScintilla.WrapFlagByText)
        self.plainTextEdit.setWrapIndentMode(QsciScintilla.WrapIndentIndented)
        self.plainTextEdit.setEolMode(QsciScintilla.EolWindows)
        self.plainTextEdit.setEolVisibility(False)
        self.plainTextEdit.setWrapVisualFlags(QsciScintilla.WrapFlagByText)
        self.plainTextEdit.marginClicked.connect(self.on_margin_clicked)
        self.__lexer = QsciLexerCPP(self.plainTextEdit)
        self.plainTextEdit.setLexer(self.__lexer)
        self.editor.addTab(self.tab, "")
        #end of de evangelion

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(690, 80, 171, 16))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.label.setPalette(palette)
        self.label.setObjectName("label")
        self.codigo_3d = QtWidgets.QListWidget(self.centralwidget)
        self.codigo_3d.setGeometry(QtCore.QRect(680, 100, 211, 401))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.NoBrush)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.NoBrush)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.NoBrush)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.PlaceholderText, brush)
        self.codigo_3d.setPalette(palette)
        self.codigo_3d.setObjectName("codigo_3d")
        self.consola = PlainTextEdit(self.centralwidget)
        self.consola.setGeometry(QtCore.QRect(10, 530, 661, 221))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(29, 29, 29))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(29, 29, 29))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        ###########################
        self.consola.setPalette(palette)
        self.consola.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.consola.setObjectName("consola")
        ###########################
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(890, 80, 171, 16))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.label_2.setPalette(palette)
        self.label_2.setObjectName("label_2")
        self.tabla_cuadruplos = QtWidgets.QTableWidget(self.centralwidget)
        self.tabla_cuadruplos.setGeometry(QtCore.QRect(680, 530, 431, 221))
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
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.label_3.setPalette(palette)
        self.label_3.setObjectName("label_3")
        self.tabla_simbolos = QtWidgets.QTableWidget(self.centralwidget)
        self.tabla_simbolos.setGeometry(QtCore.QRect(1120, 100, 211, 651))
        self.tabla_simbolos.setObjectName("tabla_simbolos")
        self.tabla_simbolos.setColumnCount(2)
        self.tabla_simbolos.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tabla_simbolos.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabla_simbolos.setHorizontalHeaderItem(1, item)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(10, 510, 47, 13))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.label_4.setPalette(palette)
        self.label_4.setObjectName("label_4")
        self.codigo_3d_optimizado = QtWidgets.QListWidget(self.centralwidget)
        self.codigo_3d_optimizado.setGeometry(QtCore.QRect(900, 100, 211, 401))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.NoBrush)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.NoBrush)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 128))
        brush.setStyle(QtCore.Qt.NoBrush)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.PlaceholderText, brush)
        self.codigo_3d_optimizado.setPalette(palette)
        self.codigo_3d_optimizado.setObjectName("codigo_3d_optimizado")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1349, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuReporte = QtWidgets.QMenu(self.menubar)
        self.menuReporte.setObjectName("menuReporte")
        self.menuRun = QtWidgets.QMenu(self.menubar)
        self.menuRun.setObjectName("menuRun")
        self.menuayuda = QtWidgets.QMenu(self.menubar)
        self.menuayuda.setObjectName("menuayuda")
        self.menuAUGUS = QtWidgets.QMenu(self.menubar)
        self.menuAUGUS.setObjectName("menuAUGUS")
        MainWindow.setMenuBar(self.menubar)
        self.actionEjecutar = QtWidgets.QAction(MainWindow)
        self.actionEjecutar.setObjectName("actionEjecutar")
        self.actionEjecutar.triggered.connect(self.ejecutar_optimizado)
        self.actionDebug = QtWidgets.QAction(MainWindow)
        self.actionDebug.setObjectName("actionDebug")
        self.actionArbol_Ascendente = QtWidgets.QAction(MainWindow)
        self.actionArbol_Ascendente.setObjectName("actionArbol_Ascendente")
        ############
        self.actionArbol_Ascendente.triggered.connect(self.show_ast)
        ############
        self.actionDGA = QtWidgets.QAction(MainWindow)
        self.actionDGA.setObjectName("actionDGA")
        ############
        self.actionDGA.triggered.connect(self.show_dga)
        ############
        self.actionAbrir = QtWidgets.QAction(MainWindow)
        self.actionAbrir.setObjectName("actionAbrir")
        self.actionAbrir.triggered.connect(self.abrir_archivo)
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
        ############
        self.actionTabla_de_Simbolos.triggered.connect(self.show_TS)
        ############
        self.actionErrores_Lexicos_y_Sintacticos = QtWidgets.QAction(MainWindow)
        self.actionErrores_Lexicos_y_Sintacticos.setObjectName("actionErrores_Lexicos_y_Sintacticos")
        ############
        self.actionErrores_Lexicos_y_Sintacticos.triggered.connect(self.show_errores)
        ############
        self.actionReporte_Gramatical = QtWidgets.QAction(MainWindow)
        self.actionReporte_Gramatical.setObjectName("actionReporte_Gramatical")
        ############
        self.actionReporte_Gramatical.triggered.connect(self.show_RO)
        ############
        self.actionLexicos_y_Sintacticos = QtWidgets.QAction(MainWindow)
        self.actionLexicos_y_Sintacticos.setObjectName("actionLexicos_y_Sintacticos")
        self.actionSemanticos = QtWidgets.QAction(MainWindow)
        self.actionSemanticos.setObjectName("actionSemanticos")
        self.actionTabla_de_simbolos = QtWidgets.QAction(MainWindow)
        self.actionTabla_de_simbolos.setObjectName("actionTabla_de_simbolos")
        self.actionArbol = QtWidgets.QAction(MainWindow)
        self.actionArbol.setObjectName("actionArbol")
        self.actionGramatical = QtWidgets.QAction(MainWindow)
        self.actionGramatical.setObjectName("actionGramatical")
        self.actionGramatical.triggered.connect(self.show_RG)
        self.menuFile.addAction(self.actionAbrir)
        self.menuFile.addAction(self.actionGuardar)
        self.menuFile.addAction(self.actionGuardar_como)
        self.menuFile.addAction(self.actionBuscar)
        self.menuFile.addAction(self.actionReemplazar)
        self.menuReporte.addAction(self.actionArbol_Ascendente)
        self.menuReporte.addAction(self.actionDGA)
        self.menuReporte.addAction(self.actionTabla_de_Simbolos)
        self.menuReporte.addAction(self.actionErrores_Lexicos_y_Sintacticos)
        self.menuReporte.addAction(self.actionReporte_Gramatical)
        self.menuRun.addAction(self.actionEjecutar)
        self.menuRun.addAction(self.actionDebug)
        self.menuAUGUS.addAction(self.actionLexicos_y_Sintacticos)
        self.menuAUGUS.addAction(self.actionSemanticos)
        self.menuAUGUS.addAction(self.actionTabla_de_simbolos)
        self.menuAUGUS.addAction(self.actionArbol)
        self.menuReporte.addAction(self.actionGramatical)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuReporte.menuAction())
        self.menubar.addAction(self.menuRun.menuAction())
        self.menubar.addAction(self.menuAUGUS.menuAction())
        self.menubar.addAction(self.menuayuda.menuAction())

        self.retranslateUi(MainWindow)
        self.editor.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)



    def on_margin_clicked(self, nmargin, nline, modifiers):
        tab = self.editor.widget(self.editor.currentIndex())
        items = tab.children()

        if items[0].markersAtLine(nline) != 0:
            items[0].markerDelete(nline, 0)
            
        else:
            items[0].markerAdd(nline, 0)
    
    def Depurar_Alto_nivel(self):
        global traducir
        try:
            self.consola.clear()
            
            tab = self.editor.widget(self.editor.currentIndex())
            items = tab.children()
            codigo = items[0].text()
            ast = Gramatica.parse(codigo)
            lst_errores = Gramatica.lst_errores
            errores = GraficarError(args=(lst_errores,"Errores"),daemon = True)
            errores.start()
            gda = GramaticaGDA.parse(codigo)
            nodo = GramaticaM.parse(codigo)
            g_ast = GraficarArbol(args=(nodo,"AST"),daemon = True)
            g_ast.start()
            g_gda = GraficarGDA(args=(gda,"GDA"),daemon=True)
            g_gda.start()


        
            self.codigo_3d.clear()
            self.codigo_3d_optimizado.clear()
            #self.tabla_cuadruplos.clear()
            traducir = Depurar(args=(ast,self.tabla_cuadruplos, self.codigo_3d,self.consola,self.tabla_simbolos,items[0],self.codigo_3d_optimizado),daemon=True)
            traducir.start()
        except:
            print("ERROR EN DEPURACION")

    
    def ms_help(self):
        msg = QtWidgets.QMessageBox(self.mw)
        msg.setIcon(QtWidgets.QMessageBox.Information)
        msg.setText("201408580")
        msg.setInformativeText("Andree Avalos")
        msg.setWindowTitle("Help")
        msg.setDetailedText("Proyecto realizado para Compiladores 2 \n https://github.com/AndreeAvalos/OLC2-MINORC")
        msg.exec_()

    def setStep(self):
        try:
            traducir.step = True
        except:
            em = QtWidgets.QErrorMessage(self.mw)
            em.setWindowTitle("ERROR!!!")
            em.showMessage("No se ha iniciado ningun proceso")
        
    def setContinuar(self):
        try:
            traducir.continuar = True
            traducir.step = True
        except:
            em = QtWidgets.QErrorMessage(self.mw)
            em.setWindowTitle("ERROR!!!")
            em.showMessage("No se ha iniciado ningun proceso")
    
    def detenerEjecucion(self):
        try:
            traducir.stop()
        except:
            em = QtWidgets.QErrorMessage(self.mw)
            em.setWindowTitle("ERROR!!!")
            em.showMessage("No se ha iniciado ningun proceso")

    def setLines(self):
        'cambiar color ide'

    def Traducir_Alto_nivel(self):
        global traducir
        try:
            self.consola.clear()
            #self.tabla_cuadruplos.clear()
            tab = self.editor.widget(self.editor.currentIndex())
            items = tab.children()
            codigo = items[0].text()
            ast = Gramatica.parse(codigo)
            lst_errores = Gramatica.lst_errores
            errores = GraficarError(args=(lst_errores,"Errores"),daemon = True)
            errores.start()
            gda = GramaticaGDA.parse(codigo)
            nodo = GramaticaM.parse(codigo)
            g_ast = GraficarArbol(args=(nodo,"AST"),daemon = True)
            g_ast.start()
            g_gda = GraficarGDA(args=(gda,"GDA"),daemon=True)
            g_gda.start()
            
            self.codigo_3d.clear()
            self.codigo_3d_optimizado.clear()
            traducir = Traducir(args=(ast,self.tabla_cuadruplos, self.codigo_3d,self.consola,self.tabla_simbolos,self.codigo_3d_optimizado),daemon=True)
            traducir.start()
        except:
            print("ERROR EN EJECUCION NORMAL")
    
    def abrir_archivo(self):
        try:
            dialog = QtWidgets.QFileDialog().getOpenFileName(None,' Open document',r"C:\Users\\","All Files (*)")
            ruta = dialog[0]
            trozos = ruta.split("/")
            name = trozos[len(trozos)-1]
            self.pestañas[name] = ruta
            file = open(ruta,'r')
            codigo = file.read()
            tab = QtWidgets.QWidget()
            area = QsciScintilla(tab)
            area.setGeometry(QtCore.QRect(10, 10, 631, 371))
            area.setObjectName("plainTextEdit")
            area.setFont(self.__myFont)
            area.setMarginType(0, QsciScintilla.NumberMargin)
            area.setMarginWidth(0,"00000")
            area.setMarginsForegroundColor(QtGui.QColor("#0C4B72"))
            area.markerDefine(QsciScintilla.RightArrow, 0)
            area.setMarginSensitivity(0,True)
            area.setWrapMode(QsciScintilla.WrapWord)
            area.setWrapVisualFlags(QsciScintilla.WrapFlagByText)
            area.setWrapIndentMode(QsciScintilla.WrapIndentIndented)
            area.setEolMode(QsciScintilla.EolWindows)
            area.setEolVisibility(False)
            area.setWrapVisualFlags(QsciScintilla.WrapFlagByText)
            area.marginClicked.connect(self.on_margin_clicked)
            __lexer = QsciLexerCPP(area)
            area.setLexer(__lexer)
            self.editor.addTab(tab, "")
            area.setText(codigo)
            area.setObjectName("area")
            self.editor.addTab(tab, name)
            file.close()
        except:
            em = QtWidgets.QErrorMessage(self.mw)
            em.showMessage("Error al abrir {0}".format(name))

    def agregar_tab(self):
        text, okPressed = QInputDialog.getText(self.centralwidget, "Nuevo archivo","Nombre:", QLineEdit.Normal, "")
        if okPressed and text != '':

            tab = QtWidgets.QWidget()
            area = QsciScintilla(tab)
            area.setGeometry(QtCore.QRect(10, 10, 631, 371))
            area.setObjectName("plainTextEdit")
            area.setFont(self.__myFont)
            area.setMarginType(0, QsciScintilla.NumberMargin)
            area.setMarginWidth(0,"00000")
            area.setMarginsForegroundColor(QtGui.QColor("#0C4B72"))
            area.markerDefine(QsciScintilla.RightArrow, 0)
            area.setMarginSensitivity(0,True)
            area.setWrapMode(QsciScintilla.WrapWord)
            area.setWrapVisualFlags(QsciScintilla.WrapFlagByText)
            area.setWrapIndentMode(QsciScintilla.WrapIndentIndented)
            area.setEolMode(QsciScintilla.EolWindows)
            area.setEolVisibility(False)
            area.setWrapVisualFlags(QsciScintilla.WrapFlagByText)
            area.marginClicked.connect(self.on_margin_clicked)
            __lexer = QsciLexerCPP(area)
            area.setLexer(__lexer)
            self.editor.addTab(tab, "")
            area.setObjectName("area")
            self.editor.addTab(tab, text+".mc")         

    def closeTab(self, index):
        tab = self.editor.widget(index)
        name = self.editor.tabText(self.editor.currentIndex())
        tab.deleteLater()
        self.editor.removeTab(index)

    def guardar(self):
        indextab = self.editor.tabText(self.editor.currentIndex())
        if indextab.split(".")[0] in self.pestañas:
            ruta = self.pestañas[indextab.split(".")[0]]
            trozos = ruta.split("/")
            name = indextab
            try:
                file = open(ruta,"w")
                tab = self.editor.widget(self.editor.currentIndex())
                items = tab.children()
                codigo = items[0].text()
                file.write(codigo)
                file.close()
            except:
                em = QtWidgets.QErrorMessage(self.mw)
                em.showMessage("No fue posible guardar {0}".format(name))
                
        else:
            self.gc = True
            self.nombre = indextab
            self.guardar_como()
            self.pestañas[self.nombre]=self.rutaTemp
            self.nombre = ""
            self.gc = False

    def guardar_como(self):
        
        if not self.gc:
            self.nombre, okPressed = QInputDialog.getText(self.centralwidget, "Nuevo archivo","Nombre:", QLineEdit.Normal, "")
        carpeta = QtWidgets.QFileDialog().getExistingDirectory(self.centralwidget, "Seleccione carpeta")
        tname = self.nombre.split(".")
        name = tname[0]
        ruta = "{0}/{1}.mc".format(carpeta,name)
        self.nombre=name
        self.rutaTemp = ruta
        try:
            file = open(ruta,"w+")
            tab = self.editor.widget(self.editor.currentIndex())
            items = tab.children()
            codigo = items[0].text()
            file.write(codigo)
            file.close()
        except:
            em = QtWidgets.QErrorMessage(self.mw)
            em.showMessage("No fue posible guardar {0}".format(name))
    
    def show_ast(self):
        self.show("AST")
    def show_dga(self):
        self.show("GDA")
    def show_errores(self):
        self.show("Errores")
    def show_RO(self):
        self.show("reporteOptimizado")
    def show_TS(self):
        self.show("tabla_traducir")
    def show_RG(self):
        self.show("gramatical")

    def show(self, ruta):
        try:
            Dialog = QtWidgets.QDialog(self.mw)
            ui = Visor()
            ui.setupUi(Dialog,ruta+".png")
            Dialog.show()
        except:
            em = QtWidgets.QErrorMessage(self.mw)
            em.setWindowTitle("ERROR!!!")
            em.showMessage("No se ha generado ningun reporte")

    def ejecutar_optimizado(self):
        global traducir
        try:
            file = open("codigo_optimizado.txt", "r")
            codigo = file.read()
            ast2 = GramaticaA.parse(codigo)
            ast3 = ast2.instruccion
            ts = TSA()
            recolector = Recolectar(ast3,ts,[])
            recolector.procesar()
            self.consola.clear()
            traducir = Ejecutor(args=(ast3,ts,[],"",self.consola,self.tabla_simbolos),daemon=True)
            traducir.start()
        except:
            print("ERROR EN EJECUCION DE OPTIMIZADO")

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
        self.tema.setText(_translate("MainWindow", "Lineas"))
        self.lineas.setText(_translate("MainWindow", "Help"))
        self.editor.setTabText(self.editor.indexOf(self.tab), _translate("MainWindow", "Tab 1"))
        self.label.setText(_translate("MainWindow", "Codigo AUGUS"))
        self.label_2.setText(_translate("MainWindow", "Codigo AUGUS optimizado"))
        item = self.tabla_cuadruplos.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "op"))
        item = self.tabla_cuadruplos.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "arg1"))
        item = self.tabla_cuadruplos.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "arg2"))
        item = self.tabla_cuadruplos.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "result"))
        self.label_3.setText(_translate("MainWindow", "Cuadruplos"))
        item = self.tabla_simbolos.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "ID"))
        item = self.tabla_simbolos.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "VALOR"))
        self.label_4.setText(_translate("MainWindow", "Consola"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuReporte.setTitle(_translate("MainWindow", "Reporte"))
        self.menuRun.setTitle(_translate("MainWindow", "Run"))
        self.menuayuda.setTitle(_translate("MainWindow", "Help"))
        self.menuAUGUS.setTitle(_translate("MainWindow", "Augus"))
        self.actionEjecutar.setText(_translate("MainWindow", "Ejecutar"))
        self.actionDebug.setText(_translate("MainWindow", "Debug"))
        self.actionArbol_Ascendente.setText(_translate("MainWindow", "Arbol Ascendente"))
        self.actionDGA.setText(_translate("MainWindow", "GDA"))
        self.actionAbrir.setText(_translate("MainWindow", "Abrir"))
        self.actionGuardar.setText(_translate("MainWindow", "Guardar"))
        self.actionGuardar_como.setText(_translate("MainWindow", "Guardar como.."))
        self.actionBuscar.setText(_translate("MainWindow", "Buscar"))
        self.actionReemplazar.setText(_translate("MainWindow", "Reemplazar"))
        self.actionTabla_de_Simbolos.setText(_translate("MainWindow", "Tabla de Simbolos"))
        self.actionErrores_Lexicos_y_Sintacticos.setText(_translate("MainWindow", "Errores Lexicos y Sintacticos"))
        self.actionReporte_Gramatical.setText(_translate("MainWindow", "Reporte Optimizacion"))
        self.actionLexicos_y_Sintacticos.setText(_translate("MainWindow", "Lexicos y Sintacticos"))
        self.actionSemanticos.setText(_translate("MainWindow", "Semanticos"))
        self.actionTabla_de_simbolos.setText(_translate("MainWindow", "Tabla de simbolos"))
        self.actionArbol.setText(_translate("MainWindow", "Arbol"))
        self.actionGramatical.setText(_translate("MainWindow", "Gramatical"))
        self.consola.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\';\"><br /></p></body></html>"))
        