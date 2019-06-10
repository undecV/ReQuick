import sys
import re
# import logging

from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QMainWindow, QCheckBox, QListWidget, QStatusBar, QPlainTextEdit, QLineEdit, QPushButton
from PySide2 import QtCore
from PySide2.QtCore import QFile
import yaml

# logging.basicConfig(level=logging.DEBUG)

RE_YAML_FILE = 're.yml'

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        ui_file = QFile("main.ui")
        ui_file.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.window = loader.load(ui_file)
        ui_file.close()
        self.window.show()

        self.clipboard = QApplication.clipboard()

        self.checkBox_1 = self.window.findChild(QCheckBox, 'checkBox_1')
        self.checkBox_2 = self.window.findChild(QCheckBox, 'checkBox_2')
        self.checkBox_3 = self.window.findChild(QCheckBox, 'checkBox_3')
        self.lineEdit_1 = self.window.findChild(QLineEdit, 'lineEdit_1')
        self.lineEdit_2 = self.window.findChild(QLineEdit, 'lineEdit_2')
        self.listWidget_1 = self.window.findChild(QListWidget, 'listWidget_1')
        self.plainTextEdit_1 = self.window.findChild(QPlainTextEdit, 'plainTextEdit_1')
        self.plainTextEdit_2 = self.window.findChild(QPlainTextEdit, 'plainTextEdit_2')
        self.pushButton_1 = self.window.findChild(QPushButton, 'pushButton_1')
        self.pushButton_2 = self.window.findChild(QPushButton, 'pushButton_2')
        self.pushButton_3 = self.window.findChild(QPushButton, 'pushButton_3')
        self.pushButton_4 = self.window.findChild(QPushButton, 'pushButton_4')
        self.statusbar = self.window.findChild(QStatusBar, 'statusbar')
        # print(self.__dict__)

        self.checkBox_1.stateChanged.connect(self.on_checkBox_1_stateChanged)
        self.checkBox_2.stateChanged.connect(self.on_checkBox_2_stateChanged)
        self.checkBox_3.stateChanged.connect(self.on_checkBox_3_stateChanged)
        self.lineEdit_1.textChanged.connect(self.on_lineEdit_1_textChanged)
        self.lineEdit_2.textChanged.connect(self.on_lineEdit_2_textChanged)
        self.clipboard.dataChanged.connect(self.on_clipboard_dataChanged)
        self.listWidget_1.itemSelectionChanged.connect(self.on_listWidget_1_itemSelectionChanged)
        self.plainTextEdit_1.textChanged.connect(self.on_plainTextEdit_1_textChanged)
        # self.plainTextEdit_1.clicked.connect(self.on_plainTextEdit_1_clicked)
        self.plainTextEdit_2.textChanged.connect(self.on_plainTextEdit_2_textChanged)
        self.pushButton_1.clicked.connect(self.on_pushButton_1_clicked)
        self.pushButton_2.clicked.connect(self.on_pushButton_2_clicked)
        self.pushButton_3.clicked.connect(self.on_pushButton_3_clicked)
        self.pushButton_4.clicked.connect(self.on_pushButton_4_clicked)

        # self.checkBox_1.setEnabled(False)
        # self.checkBox_2.setEnabled(False)
        # self.checkBox_3.setEnabled(False)
        self.statusbar.showMessage('https://github.com/undecV/ReQuick')

        self.res = {}
        self.ref = ''
        self.ret = ''
        self.on_pushButton_2_clicked()


    def on_clipboard_dataChanged(self):
        text = self.clipboard.text()
        # print("on_clipboard_dataChanged", repr(text))
        if not self.checkBox_1.isChecked():
            return
        if text == self.plainTextEdit_1.toPlainText():
            return
        # if text == self.plainTextEdit_2.toPlainText():
        #     return 
        self.plainTextEdit_1.setPlainText(text)
        # print("on_clipboard_dataChanged, setPlainText", repr(text))


    def on_listWidget_1_itemSelectionChanged(self):
        key = self.listWidget_1.currentItem().text()
        if key not in self.res:
            raise KeyError()
        self.ref, self.ret = self.res[key]
        self.lineEdit_2.setText(self.ref)
        self.lineEdit_1.setText(self.ret)
        self.on_plainTextEdit_1_textChanged()


    def on_lineEdit_1_textChanged(self):
        self.ret = self.lineEdit_1.text()
        self.on_plainTextEdit_1_textChanged()


    def on_lineEdit_2_textChanged(self):
        self.ref = self.lineEdit_2.text()
        self.on_plainTextEdit_1_textChanged()


    def on_checkBox_1_stateChanged(self):
        if self.checkBox_1.isChecked():
            if self.checkBox_2.isChecked():
                self.checkBox_2.setChecked(False)
            self.on_clipboard_dataChanged()

    
    def on_checkBox_2_stateChanged(self):
        if self.checkBox_2.isChecked():
            if self.checkBox_1.isChecked():
                self.checkBox_1.setChecked(False)
            pass
        pass


    def on_checkBox_3_stateChanged(self):
        """Toggle window stay on the top."""
        # https://stackoverflow.com/a/4850757
        # Window will hide and show.
        # https://stackoverflow.com/a/47122426
        # https://doc.qt.io/qt-5/qwidget.html#windowFlags-prop
        if self.checkBox_3.isChecked():
            self.window.setWindowFlags(self.window.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
            self.window.show()
        else: 
            self.window.setWindowFlags(self.window.windowFlags() & ~QtCore.Qt.WindowStaysOnTopHint)
            self.window.show()


    def on_pushButton_1_clicked(self):
        """Copy Button"""
        text = self.plainTextEdit_2.toPlainText()
        # print("on_pushButton_1_clicked: " + repr(text))
        self.clipboard.setText(text)
        self.statusbar.showMessage('copied! ' + repr(text))
        # print('Copied', repr(text))


    def on_pushButton_2_clicked(self):
        """Reload YAML Button"""
        with open(RE_YAML_FILE, 'r', encoding='utf-8') as fp:
            self.res = yaml.load(fp, Loader=yaml.FullLoader)
        # print(self.res)
        self.listWidget_1.clear()
        self.listWidget_1.addItems(list(self.res.keys()))
        self.listWidget_1.setCurrentRow(0)


    def on_pushButton_3_clicked(self):
        """Clear Button"""
        self.plainTextEdit_1.clear()


    def on_pushButton_4_clicked(self):
        """Paste Button"""
        text = self.clipboard.text()
        self.on_pushButton_3_clicked()
        self.plainTextEdit_1.setPlainText(text)


    def on_plainTextEdit_1_textChanged(self):
        text = self.plainTextEdit_1.toPlainText()
        # print(self.ref, self.ret)
        try: 
            opt = re.sub(self.ref, self.ret, text)
        except Exception as e:
            opt = text
            self.statusbar.showMessage(str(e))
        self.plainTextEdit_2.setPlainText(opt)
        # print(repr(text))


    def on_plainTextEdit_2_textChanged(self):
        text = self.plainTextEdit_2.toPlainText()
        # print('on_plainTextEdit_2_textChanged', repr(text))
        if not self.checkBox_2.isChecked():
            return
        if self.plainTextEdit_1.toPlainText() == text:
            return
        self.on_pushButton_1_clicked()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())
