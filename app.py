# -*- coding: utf-8 -*-
"""
Time:   2024/3/23 14:58
Auth:   Jeremy
File:   app.py
IDE:    PyCharm
GitHub: https://github.com/JeremyChim
"""
from PyQt6.QtWidgets import QApplication, QWidget, QFileDialog
from PyQt6.QtGui import QIcon
from untitled import Ui_Form
from colorama import init, Fore

init(autoreset=True)


class Window(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Dota Tool')
        self.setWindowIcon(QIcon('app.ico'))
        self.init_function()
        self.file_url: str = ''
        self.file_content: list[str] = ['']

    def init_function(self):
        self.pushButton.clicked.connect(self.get_file_url)
        self.pushButton_2.clicked.connect(self.get_file_content)
        self.pushButton_3.clicked.connect(self.save_file)
        self.pushButton_4.clicked.connect(self.update_xp_gold)

    def get_file_url(self):
        file_url, file_type = QFileDialog.getOpenFileName()  # GET THE URL
        print(f'Get file url : {Fore.BLUE + file_url}')
        self.lineEdit.setText(file_url)  # SENT THE URL
        self.file_url = file_url

    def get_file_content(self):
        try:
            with open(self.file_url, 'r') as f:
                self.file_content = f.readlines()  # GET CONTENT
                print(Fore.GREEN + 'Get file content success.', Fore.BLUE + f'Content len : {len(self.file_content)}')
        except:
            print(Fore.RED + 'Somthing is worry T_T')

    def save_file(self):
        try:
            file_url, file_type = QFileDialog.getSaveFileName()
            with open(file_url, 'w') as f:
                f.writelines(self.file_content)
                print(Fore.GREEN + 'Write lines success.', Fore.BLUE + f'Len : {len(self.file_content)}')
                print(Fore.GREEN + 'Save fine success.', Fore.BLUE + f'New file url : {file_url}')
        except:
            print(Fore.RED + 'Somthing is worry T_T')

    def update_xp_gold(self):
        try:
            self.file_content: list[str]
            factor: float = self.doubleSpinBox.value()
            print(Fore.BLUE + f'factor : {factor}')
            line_num: int = 1
            for one_line in self.file_content:
                one_line: str
                if 'BountyXP' in one_line:
                    print(Fore.LIGHTWHITE_EX + str(line_num) + one_line, end='\r')
                    one_list: list[str] = one_line.split('"')  # OLD DATA
                    one_list[3] = f'{float(one_list[3]) * factor:.0f}'  # CALC
                    one_line = '"'.join(one_list)  # NEW DATA
                    print(Fore.LIGHTBLACK_EX + str(line_num) + one_line, end='\r')
                    self.file_content[line_num - 1] = one_line

                elif 'BountyGoldMin' in one_line:
                    print(Fore.LIGHTWHITE_EX + str(line_num) + one_line, end='\r')
                    one_list: list[str] = one_line.split('"')  # OLD DATA
                    one_list[3] = f'{float(one_list[3]) * factor:.0f}'  # CALC
                    one_line = '"'.join(one_list)  # NEW DATA
                    print(Fore.LIGHTBLACK_EX + str(line_num) + one_line, end='\r')
                    self.file_content[line_num - 1] = one_line

                elif 'BountyGoldMax' in one_line:
                    print(Fore.LIGHTWHITE_EX + str(line_num) + one_line, end='\r')
                    one_list: list[str] = one_line.split('"')  # OLD DATA
                    one_list[3] = f'{float(one_list[3]) * factor:.0f}'  # CALC
                    one_line = '"'.join(one_list)  # NEW DATA
                    print(Fore.LIGHTBLACK_EX + str(line_num) + one_line, end='\r')
                    self.file_content[line_num - 1] = one_line

                line_num += 1
            print(Fore.GREEN + 'Update success.')
        except:
            print(Fore.RED + 'Somthing is worry T_T')


if __name__ == '__main__':
    app = QApplication([])
    win = Window()
    win.show()
    app.exec()
