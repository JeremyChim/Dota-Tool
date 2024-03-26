# -*- coding: utf-8 -*-
"""
Time:   2024/3/23 14:58
Auth:   Jeremy
File:   app.py
IDE:    PyCharm
GitHub: https://github.com/JeremyChim
"""
from PyQt6 import QtWidgets
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
        self.hero_name_list: list[str] = []
        self.hero_line_list: list[int] = []

    def init_function(self):
        self.pushButton.clicked.connect(self.get_file_url)
        self.pushButton_2.clicked.connect(self.get_file_content)
        self.pushButton_3.clicked.connect(self.save_file)
        self.pushButton_4.clicked.connect(self.update_xp_gold)
        self.pushButton_5.clicked.connect(self.update_tower_data)
        self.pushButton_9.clicked.connect(self.ability_replace)
        self.pushButton_11.clicked.connect(self.get_file_url)
        self.pushButton_12.clicked.connect(self.get_file_content)
        self.pushButton_13.clicked.connect(self.save_file)
        self.pushButton_14.clicked.connect(self.get_hero_name)
        self.pushButton_15.clicked.connect(self.get_hero_data)
        self.pushButton_16.clicked.connect(self.update_hero_data)

    def get_file_url(self):
        file_url, file_type = QFileDialog.getOpenFileName()  # GET THE URL
        if file_url:
            print(f'Get file url : {Fore.LIGHTCYAN_EX + file_url}')
            self.lineEdit.setText(file_url)  # SENT THE URL
            self.lineEdit_8.setText(file_url)  # SENT THE URL
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

    def get_hero_name(self):

        try:
            hero_name_list: list[str] = []
            hero_line_list: list[int] = []
            line_num: int = 1  # MAKE LINE
            for one_line in self.file_content:
                one_line: str
                if '\t"npc_dota_hero_' in one_line and one_line.split('"')[2] == '\n':
                    print(Fore.LIGHTYELLOW_EX + str(line_num), one_line, end='\r')
                    hero_name: str = one_line.split('"')[1]
                    hero_name_list.append(hero_name)  # Get Name
                    hero_line_list.append(line_num)  # Get Line Number
                    self.comboBox.addItem(hero_name)
                line_num += 1
            print(Fore.LIGHTGREEN_EX + 'Read hero data success.', Fore.LIGHTBLUE_EX + f'hero : {len(hero_name_list)}')
            self.hero_name_list = hero_name_list
            self.hero_line_list = hero_line_list
        except:
            print(Fore.LIGHTRED_EX + 'Somthing is worry T_T')

    def get_hero_data(self):
        hero_name = self.comboBox.currentText()
        hero_name_index = self.hero_name_list.index(hero_name)
        hero_line: int = self.hero_line_list[hero_name_index]
        print(f'index : {Fore.LIGHTBLUE_EX + str(hero_name_index)}')
        print(f'name : {Fore.LIGHTMAGENTA_EX + hero_name}')
        print(f'line : {Fore.LIGHTYELLOW_EX + str(hero_line)}')

        widget_list: list[tuple] = [('MovementSpeed', self.doubleSpinBox_12)]

        line_num: int = hero_line + 1
        for one_line in self.file_content[hero_line:]:
            one_line: str
            if 'MovementSpeed' in one_line:
                # print(Fore.LIGHTYELLOW_EX + str(line_num), one_line, end='\r')
                one_list: list[str] = one_line.split('"')
                value: float = float(one_list[3])
                self.doubleSpinBox_12.setValue(value)
                break
            line_num += 1

    def update_hero_data(self):
        hero_name = self.comboBox.currentText()
        hero_name_index = self.hero_name_list.index(hero_name)
        hero_line: int = self.hero_line_list[hero_name_index]
        line_num: int = hero_line + 1
        for one_line in self.file_content[hero_line:]:
            one_line: str
            if 'MovementSpeed' in one_line:
                print(Fore.LIGHTYELLOW_EX + str(line_num), one_line, end='\r')
                one_list: list[str] = one_line.split('"')
                one_list[3] = f'{self.doubleSpinBox_12.value():.0f}'
                one_line = '"'.join(one_list)
                print(Fore.LIGHTGREEN_EX + str(line_num), Fore.LIGHTGREEN_EX + one_line, end='\r')
                self.file_content[line_num - 1] = one_line
                break
            line_num += 1


if __name__ == '__main__':
    app = QApplication([])
    win = Window()
    win.show()
    app.exec()
