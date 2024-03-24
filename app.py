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
        self.pushButton_5.clicked.connect(self.update_tower_data)
        self.pushButton_9.clicked.connect(self.ability_replace)

    def get_file_url(self):
        file_url, file_type = QFileDialog.getOpenFileName()  # GET THE URL
        if file_url:
            print(f'Get file url : {Fore.LIGHTCYAN_EX + file_url}')
            self.lineEdit.setText(file_url)  # SENT THE URL
            self.file_url = file_url
        else:
            print(Fore.LIGHTRED_EX + 'URL is empty T_T')

    def get_file_content(self):
        try:
            with open(self.file_url, 'r') as f:
                self.file_content = f.readlines()  # GET CONTENT
                print(Fore.LIGHTGREEN_EX + 'Get file content success.',
                      Fore.LIGHTBLUE_EX + f'Content len : {len(self.file_content)}')
        except:
            print(Fore.LIGHTRED_EX + 'Somthing is worry T_T')

    def save_file(self):
        try:
            file_url, file_type = QFileDialog.getSaveFileName()
            with open(file_url, 'w') as f:
                f.writelines(self.file_content)
                print(Fore.LIGHTGREEN_EX + 'Write lines success.',
                      Fore.LIGHTBLUE_EX + f'Len : {len(self.file_content)}')
                print(Fore.LIGHTGREEN_EX + 'Save fine success.', Fore.LIGHTCYAN_EX + f'New file url : {file_url}')
        except:
            print(Fore.LIGHTRED_EX + 'Somthing is worry T_T')

    def update_xp_gold(self):
        try:
            self.file_content: list[str]
            factor: float = self.doubleSpinBox.value()
            print(Fore.LIGHTBLUE_EX + f'factor : {factor}')

            line_num: int = 1  # MAKE LINE
            for one_line in self.file_content:
                one_line: str
                if 'BountyXP' in one_line:
                    print(Fore.LIGHTBLACK_EX + str(line_num) + one_line, end='\r')
                    one_list: list[str] = one_line.split('"')  # OLD DATA
                    one_list[3] = f'{float(one_list[3]) * factor:.0f}'  # CALC
                    one_line = '"'.join(one_list)  # NEW DATA
                    print(Fore.LIGHTYELLOW_EX + str(line_num) + one_line, end='\r')
                    self.file_content[line_num - 1] = one_line  # Write to Global

                elif 'BountyGoldMin' in one_line:
                    print(Fore.LIGHTBLACK_EX + str(line_num) + one_line, end='\r')
                    one_list: list[str] = one_line.split('"')  # OLD DATA
                    one_list[3] = f'{float(one_list[3]) * factor:.0f}'  # CALC
                    one_line = '"'.join(one_list)  # NEW DATA
                    print(Fore.LIGHTYELLOW_EX + str(line_num) + one_line, end='\r')
                    self.file_content[line_num - 1] = one_line  # Write to Global

                elif 'BountyGoldMax' in one_line:
                    print(Fore.LIGHTBLACK_EX + str(line_num) + one_line, end='\r')
                    one_list: list[str] = one_line.split('"')  # OLD DATA
                    one_list[3] = f'{float(one_list[3]) * factor:.0f}'  # CALC
                    one_line = '"'.join(one_list)  # NEW DATA
                    print(Fore.LIGHTYELLOW_EX + str(line_num) + one_line, end='\r')
                    self.file_content[line_num - 1] = one_line  # Write to Global

                line_num += 1
            print(Fore.LIGHTGREEN_EX + 'Update success.')
        except:
            print(Fore.LIGHTRED_EX + 'Somthing is worry T_T')

    def update_tower(self, keyword: str, keyword2: str, mul: float, add: int):
        try:
            self.file_content: list[str]
            # mul: float = self.doubleSpinBox_2.value()
            # add: int = self.spinBox.value()
            print(Fore.LIGHTBLUE_EX + f'Update tower arg : ')
            print(Fore.LIGHTBLUE_EX + f'- keyword : {keyword}')
            print(Fore.LIGHTBLUE_EX + f'- keyword2 : {keyword2}')
            print(Fore.LIGHTBLUE_EX + f'- mul : {mul}')
            print(Fore.LIGHTBLUE_EX + f'- add : {add}')

            line_num: int = 1  # MAKE LINE
            for one_line in self.file_content:
                one_line: str
                if keyword in one_line:
                    print(Fore.LIGHTMAGENTA_EX + str(line_num) + one_line, end='\r')
                    key_line: str
                    line_num2 = line_num + 1
                    for key_line in self.file_content[line_num:]:
                        if keyword2 in key_line:
                            print(Fore.LIGHTBLACK_EX + str(line_num2) + key_line, end='\r')
                            key_list: list[str] = key_line.split('"')  # OLD DATA
                            key_list[3] = f'{float(key_list[3]) * mul + add:.0f}'  # CALC
                            key_line = '"'.join(key_list)  # NEW DATA
                            print(Fore.LIGHTYELLOW_EX + str(line_num2) + key_line, end='\r')
                            self.file_content[line_num2 - 1] = key_line  # Write to Global
                            break
                        line_num2 += 1
                line_num += 1
        except:
            print(Fore.LIGHTRED_EX + 'Somthing is worry T_T')

    def update_tower_data(self):
        # keyword: str = 'StatusHealth'
        # mul: float = self.doubleSpinBox_2.value()
        # add: int = self.spinBox.value()
        arg_list: list[tuple] = [('Tower 1', 'StatusHealth', self.doubleSpinBox_2.value(), self.spinBox.value()),
                                 ('Tower 1', 'ArmorPhysical', self.doubleSpinBox_3.value(), self.spinBox_2.value()),
                                 ('Tower 2', 'StatusHealth', self.doubleSpinBox_4.value(), self.spinBox_3.value()),
                                 ('Tower 2', 'ArmorPhysical', self.doubleSpinBox_5.value(), self.spinBox_4.value()),
                                 ('Tower 3', 'StatusHealth', self.doubleSpinBox_6.value(), self.spinBox_5.value()),
                                 ('Tower 3', 'ArmorPhysical', self.doubleSpinBox_7.value(), self.spinBox_6.value()),
                                 ('Tower 4', 'StatusHealth', self.doubleSpinBox_8.value(), self.spinBox_7.value()),
                                 ('Tower 4', 'ArmorPhysical', self.doubleSpinBox_9.value(), self.spinBox_8.value()),
                                 ('Guys Fort', 'StatusHealth', self.doubleSpinBox_10.value(), self.spinBox_9.value()),
                                 ('Guys Fort', 'ArmorPhysical', self.doubleSpinBox_11.value(), self.spinBox_10.value())]
        for arg in arg_list:
            arg: tuple
            if arg[2] == 1 and arg[3] == 0:
                pass
            else:
                self.update_tower(*arg)

    def ability_replace(self):
        self.textEdit_3.clear()
        mod: str = self.textEdit.toPlainText()
        # old_ab: str = self.textEdit_2.toPlainText()
        old_content: str = self.textEdit_2.toPlainText()
        old_lines: list[str] = old_content.split('\n')

        for old_ab in old_lines:
            old_ab: str
            # print(old_ab)
            if old_ab:
                old_ab_list: list[str] = old_ab.split('"')
                new_ab: str = mod.replace('ab_name', old_ab_list[1]).replace('ab_value', old_ab_list[3])
                self.textEdit_3.append(new_ab)
                print(old_ab)
                # print(mod)
                print(Fore.LIGHTBLUE_EX + new_ab)
            else:
                print(Fore.LIGHTRED_EX + 'Empty ability T_T')


if __name__ == '__main__':
    app = QApplication([])
    win = Window()
    win.show()
    app.exec()
