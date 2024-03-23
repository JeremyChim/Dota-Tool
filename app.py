# -*- coding: utf-8 -*-
"""
Time:   2024/3/23 14:58
Auth:   Jeremy
File:   app.py
IDE:    PyCharm
GitHub: https://github.com/JeremyChim
"""
from PyQt6.QtWidgets import QApplication, QWidget, QFileDialog
from untitled import Ui_Form


class Window(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.file_url: str = ''
        self.file_content: list[str] = ['']
        self.setWindowTitle('Dota Tool')
        self.setupUi(self)
        self.init_function()

    def init_function(self):
        self.pushButton.clicked.connect(self.get_file_url)
        self.pushButton_2.clicked.connect(self.get_file_content)
        self.pushButton_3.clicked.connect(self.save_file)

    def get_file_url(self):
        file_url, file_type = QFileDialog.getOpenFileName()
        print(f'get_file_url : {file_url}')
        self.lineEdit.setText(file_url)
        self.file_url = file_url

    def get_file_content(self):
        try:
            with open(self.file_url, 'r') as f:
                self.file_content = f.readlines()
                print(f'get_file_content_len : {len(self.file_content)}')
        except:
            print('somthing is worry T_T')

    def save_file(self):
        try:
            self.file_url = self.lineEdit.text()
            with open(self.file_url, 'w') as f:
                f.writelines(self.file_content)
                print(f'writelines_len : {len(self.file_content)}')
                print(f'save_fine_finsh. new file url : {self.file_url}')
        except:
            print('somthing is worry T_T')


if __name__ == '__main__':
    app = QApplication([])
    win = Window()
    win.show()
    app.exec()
