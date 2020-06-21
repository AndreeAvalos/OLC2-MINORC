
from PyQt5.QtCore import Qt, QRect, QRegExp
from PyQt5.QtWidgets import QWidget, QTextEdit, QPlainTextEdit
from PyQt5.QtGui import (QColor, QPainter, QFont, QSyntaxHighlighter,
                             QTextFormat, QTextCharFormat) 
# classes definition

class XMLHighlighter(QSyntaxHighlighter):
    '''
    Class for highlighting xml text inherited from QSyntaxHighlighter
    reference:
        http://www.yasinuludag.com/blog/?p=49    
    
    '''
    def __init__(self, parent=None):
        
        super(XMLHighlighter, self).__init__(parent)
        
        self.highlightingRules = []

        #COLOR PARA NUMEROS
        xmlAttributeFormat = QTextCharFormat()
        xmlAttributeFormat.setForeground(QColor("#262C83")) #anaranjado
        self.highlightingRules.append((QRegExp("[0-9]+"), xmlAttributeFormat))

        #COLOR PARA NUMEROS
        xmlAttributeFormat = QTextCharFormat()
        xmlAttributeFormat.setForeground(QColor("#44487B")) #anaranjado
        self.highlightingRules.append((QRegExp("[0-9]+\.[0-9]+"), xmlAttributeFormat))

        #COLOR PARA ID
        xmlAttributeFormat = QTextCharFormat()
        xmlAttributeFormat.setFontItalic(True)
        xmlAttributeFormat.setForeground(QColor("#A854EE")) #anaranjado
        self.highlightingRules.append((QRegExp("[A-Za-z0-9][A-Za-z0-9_]+"), xmlAttributeFormat))


        #COLOR PARA STRING
        xmlAttributeFormat = QTextCharFormat()
        xmlAttributeFormat.setFontItalic(True)
        xmlAttributeFormat.setForeground(QColor("#F98D03")) #anaranjado
        self.highlightingRules.append((QRegExp("\'.*\'"), xmlAttributeFormat))

        
        #COLOR PARA CARACTER
        xmlAttributeFormat = QTextCharFormat()
        xmlAttributeFormat.setFontKerning(True)
        xmlAttributeFormat.setForeground(QColor("#F8BDC5")) #rosado
        self.highlightingRules.append((QRegExp("\'[A-Za-z0-9]\'"), xmlAttributeFormat))

        #COLOR PARA int, float, char
        xmlAttributeFormat = QTextCharFormat()
        xmlAttributeFormat.setForeground(QColor("#1C3784")) #azul oscuro
        self.highlightingRules.append((QRegExp("int"), xmlAttributeFormat))
        self.highlightingRules.append((QRegExp("float"), xmlAttributeFormat))
        self.highlightingRules.append((QRegExp("char"), xmlAttributeFormat))
        self.highlightingRules.append((QRegExp("double"), xmlAttributeFormat))


        #COLOR PARA COMENTARIOS
        xmlAttributeFormat = QTextCharFormat()
        xmlAttributeFormat.setFontItalic(True)
        xmlAttributeFormat.setForeground(QColor("#29BB15")) #verde
        self.highlightingRules.append((QRegExp("#.*"), xmlAttributeFormat))

        #COLOR DE palabras reservadas
        xmlElementFormat = QTextCharFormat()
        xmlElementFormat.setFontItalic(True)
        xmlElementFormat.setForeground(QColor("#1593BB")) #verde
        self.highlightingRules.append(("main", xmlElementFormat))
        self.highlightingRules.append((QRegExp("print"), xmlElementFormat))
        self.highlightingRules.append((QRegExp("exit"), xmlElementFormat))
        self.highlightingRules.append((QRegExp("goto"), xmlElementFormat))        
        self.highlightingRules.append((QRegExp("if"), xmlElementFormat))
        self.highlightingRules.append((QRegExp("read"), xmlElementFormat))
        self.highlightingRules.append((QRegExp("unset"), xmlElementFormat))
        self.highlightingRules.append((QRegExp("abs"), xmlElementFormat))

        #COLOR PARA simbolos
        xmlAttributeFormat = QTextCharFormat()
        xmlAttributeFormat.setForeground(QColor("#D355CB")) #morado
        self.highlightingRules.append((QRegExp("="), xmlAttributeFormat))
        self.highlightingRules.append((QRegExp("\("), xmlAttributeFormat))
        self.highlightingRules.append((QRegExp("\)"), xmlAttributeFormat))
        self.highlightingRules.append((QRegExp(";"), xmlAttributeFormat))
        self.highlightingRules.append((QRegExp(":"), xmlAttributeFormat))
        self.highlightingRules.append((QRegExp("\["), xmlAttributeFormat))
        self.highlightingRules.append((QRegExp("\]"), xmlAttributeFormat))

        #COLOR PARA OPERACIONES NUMERICAS
        xmlAttributeFormat = QTextCharFormat()
        xmlAttributeFormat.setForeground(QColor("#0E877A")) #morado
        self.highlightingRules.append((QRegExp("\+"), xmlAttributeFormat))
        self.highlightingRules.append((QRegExp("-"), xmlAttributeFormat))
        self.highlightingRules.append((QRegExp("\*"), xmlAttributeFormat))
        self.highlightingRules.append((QRegExp("\/"), xmlAttributeFormat))
        self.highlightingRules.append((QRegExp("%"), xmlAttributeFormat))
        




                #COLOR PARA OPERACIONES BIT A BIT
        xmlAttributeFormat = QTextCharFormat()
        xmlAttributeFormat.setForeground(QColor("#8EC769")) #morado
        self.highlightingRules.append((QRegExp("=="), xmlAttributeFormat))
        self.highlightingRules.append((QRegExp("!="), xmlAttributeFormat))
        self.highlightingRules.append((QRegExp(">="), xmlAttributeFormat))
        self.highlightingRules.append((QRegExp("<="), xmlAttributeFormat))
        self.highlightingRules.append((QRegExp(">"), xmlAttributeFormat))
        self.highlightingRules.append((QRegExp("<"), xmlAttributeFormat))


        #COLOR PARA OPERACIONES BIT A BIT
        xmlAttributeFormat = QTextCharFormat()
        xmlAttributeFormat.setForeground(QColor("#787D08")) #morado
        self.highlightingRules.append((QRegExp("~"), xmlAttributeFormat))
        self.highlightingRules.append((QRegExp("&"), xmlAttributeFormat))
        self.highlightingRules.append((QRegExp("\|"), xmlAttributeFormat))
        self.highlightingRules.append((QRegExp("\^"), xmlAttributeFormat))
        self.highlightingRules.append((QRegExp(">>"), xmlAttributeFormat))
        self.highlightingRules.append((QRegExp("<<"), xmlAttributeFormat))

                        #COLOR PARA OPERACIONES Logicas
        xmlAttributeFormat = QTextCharFormat()
        xmlAttributeFormat.setForeground(QColor("#870E62")) #morado
        self.highlightingRules.append((QRegExp("!"), xmlAttributeFormat))
        self.highlightingRules.append((QRegExp("&&"), xmlAttributeFormat))
        self.highlightingRules.append((QRegExp("\|\|"), xmlAttributeFormat))
        self.highlightingRules.append((QRegExp("xor"), xmlAttributeFormat))

    
        self.valueFormat = QTextCharFormat()
        self.valueFormat.setForeground(QColor("#F98D03")) #orange 
        self.valueStartExpression = QRegExp("\"")
        self.valueEndExpression = QRegExp("\"")

        #COLOR PARA COMENTARIOS
        xmlAttributeFormat = QTextCharFormat()
        xmlAttributeFormat.setFontItalic(True)
        xmlAttributeFormat.setForeground(QColor("#29BB15")) #verde
        self.highlightingRules.append((QRegExp("#.*"), xmlAttributeFormat))
 
        textFormat = QTextCharFormat()
        textFormat.setForeground(QColor("#000000")) #black
        # (?<=...)  - lookbehind is not supported
        #self.highlightingRules.append((QRegExp(">(.+)(?=</)"), textFormat))
        
        keywordFormat = QTextCharFormat()
        keywordFormat.setForeground(QColor("#000070")) #blue
        keywordFormat.setFontWeight(QFont.Bold) 
        keywordPatterns = ["\\b?xml\\b"] 
        self.highlightingRules += [(QRegExp(pattern), keywordFormat)
                for pattern in keywordPatterns]


                
    #VIRTUAL FUNCTION WE OVERRIDE THAT DOES ALL THE COLLORING
    def highlightBlock(self, text):
        #for every pattern
        for pattern, format in self.highlightingRules: 
            #Create a regular expression from the retrieved pattern
            expression = QRegExp(pattern) 
            #Check what index that expression occurs at with the ENTIRE text
            index = expression.indexIn(text) 
            #While the index is greater than 0
            while index >= 0: 
                #Get the length of how long the expression is true, set the format from the start to the length with the text format
                length = expression.matchedLength()
                self.setFormat(index, length, format) 
                #Set index to where the expression ends in the text
                index = expression.indexIn(text, index + length) 

        #HANDLE QUOTATION MARKS NOW.. WE WANT TO START WITH " AND END WITH ".. A THIRD " SHOULD NOT CAUSE THE WORDS INBETWEEN SECOND AND THIRD TO BE COLORED
        self.setCurrentBlockState(0) 
        startIndex = 0
        if self.previousBlockState() != 1:
            startIndex = self.valueStartExpression.indexIn(text) 
        while startIndex >= 0:
            endIndex = self.valueEndExpression.indexIn(text, startIndex) 
            if endIndex == -1:
                self.setCurrentBlockState(1)
                commentLength = len(text) - startIndex
            else:
                commentLength = endIndex - startIndex + self.valueEndExpression.matchedLength() 
            self.setFormat(startIndex, commentLength, self.valueFormat) 
            startIndex = self.valueStartExpression.indexIn(text, startIndex + commentLength)

 
class QCodeEditor(QPlainTextEdit):
    '''
    QCodeEditor inherited from QPlainTextEdit providing:
        
        numberBar - set by DISPLAY_LINE_NUMBERS flag equals True
        curent line highligthing - set by HIGHLIGHT_CURRENT_LINE flag equals True
        setting up QSyntaxHighlighter
    references:
        https://john.nachtimwald.com/2009/08/19/better-qplaintextedit-with-line-numbers/    
        http://doc.qt.io/qt-5/qtwidgets-widgets-codeeditor-example.html
    
    '''
    class NumberBar(QWidget):
        '''class that deifnes textEditor numberBar'''

        def __init__(self, editor):
            QWidget.__init__(self, editor)
            
            self.editor = editor
            self.editor.blockCountChanged.connect(self.updateWidth)
            self.editor.updateRequest.connect(self.updateContents)
            self.font = QFont()
            self.numberBarColor = QColor("#e8e8e8")
                     
        def paintEvent(self, event):
            
            painter = QPainter(self)
            painter.fillRect(event.rect(), self.numberBarColor)
             
            block = self.editor.firstVisibleBlock()
 
            # Iterate over all visible text blocks in the document.
            while block.isValid():
                blockNumber = block.blockNumber()
                block_top = self.editor.blockBoundingGeometry(block).translated(self.editor.contentOffset()).top()
 
                # Check if the position of the block is out side of the visible area.
                if not block.isVisible() or block_top >= event.rect().bottom():
                    break
 
                # We want the line number for the selected line to be bold.
                if blockNumber == self.editor.textCursor().blockNumber():
                    self.font.setBold(True)
                    painter.setPen(QColor("#000000"))
                else:
                    self.font.setBold(False)
                    painter.setPen(QColor("#717171"))
                painter.setFont(self.font)
                
                # Draw the line number right justified at the position of the line.
                paint_rect = QRect(0, block_top, self.width(), self.editor.fontMetrics().height())
                painter.drawText(paint_rect, Qt.AlignRight, str(blockNumber+1))
 
                block = block.next()
 
            painter.end()
            
            QWidget.paintEvent(self, event)
 
        def getWidth(self):
            count = self.editor.blockCount()
            width = self.fontMetrics().width(str(count)) + 5
            return width      
        
        def updateWidth(self):
            width = self.getWidth() + 5
            if self.width() != width:
                self.setFixedWidth(width)
                self.editor.setViewportMargins(width, 0, 0, 0)
 
        def updateContents(self, rect, scroll):
            if scroll:
                self.scroll(0, scroll)
            else:
                self.update(0, rect.y(), self.width(), rect.height())
            
            if rect.contains(self.editor.viewport().rect()):   
                fontSize = self.editor.currentCharFormat().font().pointSize()
                self.font.setPointSize(fontSize)
                self.font.setStyle(QFont.StyleNormal)
                self.updateWidth()
                
        
    def __init__(self,DISPLAY_LINE_NUMBERS=True, HIGHLIGHT_CURRENT_LINE=True,
                 SyntaxHighlighter=None, *args):        
        '''
        Parameters
        ----------
        DISPLAY_LINE_NUMBERS : bool 
            switch on/off the presence of the lines number bar
        HIGHLIGHT_CURRENT_LINE : bool
            switch on/off the current line highliting
        SyntaxHighlighter : QSyntaxHighlighter
            should be inherited from QSyntaxHighlighter
        
        '''                  
        super(QCodeEditor, self).__init__()
        self.setFont(QFont("Ubuntu Mono", 11))
        self.setLineWrapMode(QPlainTextEdit.NoWrap)
                               
        self.DISPLAY_LINE_NUMBERS = DISPLAY_LINE_NUMBERS

        if DISPLAY_LINE_NUMBERS:
            self.number_bar = self.NumberBar(self)
            
        if HIGHLIGHT_CURRENT_LINE:
            self.currentLineNumber = None
            self.currentLineColor = self.palette().alternateBase()
            # self.currentLineColor = QColor("#e8e8e8")
            self.cursorPositionChanged.connect(self.highligtCurrentLine)
        
        if SyntaxHighlighter is not None: # add highlighter to textdocument
           self.highlighter = SyntaxHighlighter(self.document())         
                 
    def resizeEvent(self, *e):
        '''overload resizeEvent handler'''
                
        if self.DISPLAY_LINE_NUMBERS:   # resize number_bar widget
            cr = self.contentsRect()
            rec = QRect(cr.left(), cr.top(), self.number_bar.getWidth(), cr.height())
            self.number_bar.setGeometry(rec)
        
        QPlainTextEdit.resizeEvent(self, *e)

    def highligtCurrentLine(self):
        newCurrentLineNumber = self.textCursor().blockNumber()
        if newCurrentLineNumber != self.currentLineNumber:                
            self.currentLineNumber = newCurrentLineNumber
            hi_selection = QTextEdit.ExtraSelection() 
            hi_selection.format.setBackground(self.currentLineColor)
            hi_selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            hi_selection.cursor = self.textCursor()
            hi_selection.cursor.clearSelection() 
            self.setExtraSelections([hi_selection])    