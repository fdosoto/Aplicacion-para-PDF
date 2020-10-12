from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow,  QAction, QTextEdit, QFontDialog, QColorDialog, QFileDialog, QListWidget
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter, QPrintPreviewDialog
from PyQt5.Qt import QFileInfo
from PyPDF2 import PdfFileMerger



class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = "PDFApp"
        self.top = 200
        self.left = 500
        self.width = 680
        self.height = 480

        self.setWindowIcon(QtGui.QIcon("PDF.ico"))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.createEditor()
        self.CreateMenu()
        self.show()

    def CreateMenu(self):
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('Archivo')
        editMenu = mainMenu.addMenu('Editar')
        viewMenu = mainMenu.addMenu('Ver')
        exportpdfAction = QAction(QIcon("PDF.ico"), "Exportar como PDF", self)
        exportpdfAction.triggered.connect(self.printPDF)
        fileMenu.addAction(exportpdfAction)
        exiteAction = QAction(QIcon("salir.png"), 'Salir', self)
        exiteAction.setShortcut("Ctrl+E")
        exiteAction.triggered.connect(self.exitWindow)
        fileMenu.addAction(exiteAction)
        rotateAction = QAction(QIcon("rotar.png"), 'Rotar', self)
        rotateAction.setShortcut("Ctrl+R")
        editMenu.addAction(rotateAction)
        saveAction = QAction(QIcon("Save.png"), 'Save', self)
        saveAction.setShortcut("Ctrl+S")
        editMenu.addAction(saveAction)
        mergeAction = QAction(QIcon("unir.png"), 'Unir Documentos', self)
        mergeAction.setShortcut("Ctrl+U")
        editMenu.addAction(mergeAction)
        fontAction = QAction(QIcon("font.png"), "Font", self)
        fontAction.setShortcut("Ctrl+F")
        fontAction.triggered.connect(self.fontDialog)
        viewMenu.addAction(fontAction)
        colorAction = QAction(QIcon("color.png"), "Color", self)
        colorAction.triggered.connect(self.colorDialog)
        viewMenu.addAction(colorAction)
        self.toolbar = self.addToolBar('Toolbar')
        self.toolbar.addAction(rotateAction)
        self.toolbar.addAction(saveAction)
        self.toolbar.addAction(mergeAction)
        self.toolbar.addAction(exiteAction)
        self.toolbar.addAction(fontAction)
        self.toolbar.addAction(colorAction)
        #self.toolbar.addAction(printAction)
        #self.toolbar.addAction(printPreviewAction)
        self.toolbar.addAction(exportpdfAction)

    def exitWindow(self):
        self.close()

    def createEditor(self):
        self.textEdit = QTextEdit(self)
        self.setCentralWidget(self.textEdit)

    def fontDialog(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.textEdit.setFont(font)

    def colorDialog(self):
        color = QColorDialog.getColor()
        self.textEdit.setTextColor(color)
    def printDialog(self):

        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer, self)
        if dialog.exec_() == QPrintDialog.Accepted:
            self.textEdit.print_(printer)
    def printpreviewDialog(self):

        printer = QPrinter(QPrinter.HighResolution)
        previewDialog = QPrintPreviewDialog(printer, self)
        previewDialog.paintRequested.connect(self.printPreview)
        previewDialog.exec_()


    def printPDF(self):
        fn, _ = QFileDialog.getSaveFileName(self, 'Exportar PDF', None, \
                                'Archivos PDF (.pdf);;Todos los Archivos()')
        if fn != '':
            if QFileInfo(fn).suffix() == "" : fn += '.pdf'
            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(fn)
            self.textEdit.document().print_(printer)

    def resource_path(relative_path):
    	try:
    		base_path = sys._MEIPASS

    	except Exception:
    		base_path = os.path.abspath('.')
    	return os.path.join(base_path, relative_path)

    class ListWidget(QListWidget):
    	def __init__(self, parent= None):
    		super().__init__(parent=None)
    		self.setAcceptDrops(True)
    		self.setStyleSheet('font-size: 25px;')
    		self.setDragDropMode(QAbstractItemView.InternalMove)
    		self.setSelectionMode(QAbstractItemView.ExtendedSelection)

    	def dragEnterEvent(self, event):

    		if event.mimeData().hasUrls():
    			event.accept()
    		else:
    			return super().dragEnterEvent(event)

    	def dragMoveEvent(self, event):
    		if event.mimeData().hasUrls():
    			event.setDropAction(Qt.CopyAction)
    			event.accept()

    	def dropEvent(self, event):
    		if event.mimeData().hasUrls():
    			event.setDropAction(Qt.CopyAction)
    			event.accept()

    			pdfFiles = []

    			for url in event.mimeData().urls():
    				if url.isLocalFile():
    					if url.toString().endswith('.pdf'):

    						pdfFiles.append(str(url.toLocalFile))

    			self.addItems(pdfFiles)

    		else:
    			return super().dropEvent(event)

App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
