# -*- coding: utf-8 -*-
"""
Time:   2024/3/23 14:58
Auth:   Jeremy
File:   app.py
IDE:    PyCharm
GitHub: https://github.com/JeremyChim
"""
import sys
import os

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QWidget, QFileDialog
from PyQt6.QtCore import Qt
from colorama import init, Fore

from untitled import Ui_Form

init(autoreset=True)


class Window(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.init_button()
        self.init_attr_button()

        self.file_url: str = ''
        self.file_content: list[str] = ['']
        self.hero_name_list: list[str] = []
        self.hero_line_list: list[int] = []
        self.good_list: list[int] = [511, 602, 693,
                                     1327, 1418, 1509, 1599, 1689, 1779,
                                     5938, 6031, 6124]
        self.bad_list: list[int] = [238, 329, 420,
                                    784, 875, 966, 1057, 1147, 1237,
                                    5659, 5752, 5845]

    def init_ui(self):
        self.setupUi(self)
        self.setWindowTitle('Dota Tool')
        self.setWindowIcon(QIcon('app.ico'))
        self.lineEdit_4.setText('2024/04/16')
        self.lineEdit_5.setText('1.8.2')

    def init_button(self):
        self.pushButton.clicked.connect(self.get_file_url)
        self.pushButton_2.clicked.connect(self.get_file_content)
        self.pushButton_3.clicked.connect(self.save_file)
        self.pushButton_4.clicked.connect(self.update_xp_other)
        self.pushButton_5.clicked.connect(self.update_tower_data)
        self.pushButton_9.clicked.connect(self.ability_replace)
        self.pushButton_11.clicked.connect(self.get_file_url)
        self.pushButton_12.clicked.connect(self.get_file_content)
        self.pushButton_13.clicked.connect(self.save_file)
        self.pushButton_14.clicked.connect(self.get_hero_name)
        self.pushButton_15.clicked.connect(self.get_hero_data)
        self.pushButton_16.clicked.connect(self.update_hero_data)
        self.checkBox.clicked.connect(self.set_to_top)
        self.pushButton_45.clicked.connect(self.update_xp_good)
        self.pushButton_46.clicked.connect(self.update_xp_bad)
        self.pushButton_47.clicked.connect(self.open_vpk_file)
        self.pushButton_48.clicked.connect(self.run_vpk_script)
        self.pushButton_56.clicked.connect(self.add_attr_2)

    def get_file_url(self):
        file_url, file_type = QFileDialog.getOpenFileName()  # GET THE URL
        if file_url:
            print(f'Get file url : {Fore.LIGHTCYAN_EX + file_url}')
            self.lineEdit.setText(file_url)  # SENT THE URL
            self.lineEdit_8.setText(file_url)  # SENT THE URL
            self.file_url = file_url
            self.get_file_content()
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

    def update_xp_good(self):
        try:
            self.file_content: list[str]
            factor: float = self.doubleSpinBox.value()
            print(Fore.LIGHTBLUE_EX + f'factor : {factor}')

            line_num: int = 1  # MAKE LINE
            for one_line in self.file_content:
                one_line: str

                if line_num in self.good_list or line_num - 1 in self.good_list or line_num - 2 in self.good_list:
                    if 'BountyXP' in one_line or 'BountyGoldMin' in one_line or 'BountyGoldMax' in one_line:
                        print(Fore.LIGHTBLACK_EX + str(line_num) + one_line, end='\r')
                        one_list: list[str] = one_line.split('"')  # OLD DATA
                        one_list[3] = f'{float(one_list[3]) * factor:.0f}'  # CALC
                        one_line = '"'.join(one_list)  # NEW DATA
                        print(Fore.LIGHTYELLOW_EX + str(line_num) + one_line, end='\r')
                        self.file_content[line_num - 1] = one_line  # Write to Global

                elif line_num in self.bad_list or line_num - 1 in self.bad_list or line_num - 2 in self.bad_list:
                    pass

                else:
                    pass

                line_num += 1
            print(Fore.LIGHTGREEN_EX + 'Update success.')
        except:
            print(Fore.LIGHTRED_EX + 'Somthing is worry T_T')

    def update_xp_bad(self):
        try:
            self.file_content: list[str]
            factor: float = self.doubleSpinBox.value()
            print(Fore.LIGHTBLUE_EX + f'factor : {factor}')

            line_num: int = 1  # MAKE LINE
            for one_line in self.file_content:
                one_line: str

                if line_num in self.good_list or line_num - 1 in self.good_list or line_num - 2 in self.good_list:
                    pass

                elif line_num in self.bad_list or line_num - 1 in self.bad_list or line_num - 2 in self.bad_list:
                    if 'BountyXP' in one_line or 'BountyGoldMin' in one_line or 'BountyGoldMax' in one_line:
                        print(Fore.LIGHTBLACK_EX + str(line_num) + one_line, end='\r')
                        one_list: list[str] = one_line.split('"')  # OLD DATA
                        one_list[3] = f'{float(one_list[3]) * factor:.0f}'  # CALC
                        one_line = '"'.join(one_list)  # NEW DATA
                        print(Fore.LIGHTYELLOW_EX + str(line_num) + one_line, end='\r')
                        self.file_content[line_num - 1] = one_line  # Write to Global

                else:
                    pass

                line_num += 1
            print(Fore.LIGHTGREEN_EX + 'Update success.')
        except:
            print(Fore.LIGHTRED_EX + 'Somthing is worry T_T')

    def update_xp_other(self):
        try:
            self.file_content: list[str]
            factor: float = self.doubleSpinBox.value()
            print(Fore.LIGHTBLUE_EX + f'factor : {factor}')

            line_num: int = 1  # MAKE LINE
            for one_line in self.file_content:
                one_line: str

                if line_num in self.good_list or line_num - 1 in self.good_list or line_num - 2 in self.good_list:
                    pass

                elif line_num in self.bad_list or line_num - 1 in self.bad_list or line_num - 2 in self.bad_list:
                    pass

                else:
                    if 'BountyXP' in one_line or 'BountyGoldMin' in one_line or 'BountyGoldMax' in one_line:
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
        try:
            hero_name = self.comboBox.currentText()
            hero_name_index = self.hero_name_list.index(hero_name)
            hero_line: int = self.hero_line_list[hero_name_index]
            print(f'index : {Fore.LIGHTBLUE_EX + str(hero_name_index)}')
            print(f'name : {Fore.LIGHTMAGENTA_EX + hero_name}')
            print(f'line : {Fore.LIGHTYELLOW_EX + str(hero_line)}')

            function_list: list[tuple] = [('AttackDamageMin', lambda: self.doubleSpinBox_13.setValue(value)),
                                          ('AttackDamageMax', lambda: self.doubleSpinBox_14.setValue(value)),
                                          ('AttackRate', lambda: self.doubleSpinBox_15.setValue(value)),
                                          ('AttackAnimationPoint', lambda: self.doubleSpinBox_16.setValue(value)),
                                          ('AttackRange', lambda: self.doubleSpinBox_17.setValue(value)),
                                          ('ProjectileSpeed', lambda: self.doubleSpinBox_24.setValue(value)),
                                          ('AttributeBaseStrength', lambda: self.doubleSpinBox_18.setValue(value)),
                                          ('AttributeStrengthGain', lambda: self.doubleSpinBox_19.setValue(value)),
                                          ('AttributeBaseIntelligence', lambda: self.doubleSpinBox_20.setValue(value)),
                                          ('AttributeIntelligenceGain', lambda: self.doubleSpinBox_21.setValue(value)),
                                          ('AttributeBaseAgility', lambda: self.doubleSpinBox_22.setValue(value)),
                                          ('AttributeAgilityGain', lambda: self.doubleSpinBox_23.setValue(value)),
                                          ('MovementSpeed', lambda: self.doubleSpinBox_12.setValue(value)),
                                          ('ArmorPhysical', lambda: self.doubleSpinBox_25.setValue(value))]

            for keyword, function in function_list:
                keyword: str

                line_num: int = hero_line + 1
                for one_line in self.file_content[hero_line:]:
                    one_line: str

                    if keyword in one_line:
                        one_list: list[str] = one_line.split('"')
                        if len(one_list) == 5 and one_list[4] == '\n':
                            value: float = float(one_list[3])
                            function()
                            break

                    line_num += 1
        except:
            print(Fore.LIGHTRED_EX + 'Somthing is worry T_T')

    def update_hero_data(self):
        try:
            hero_name = self.comboBox.currentText()
            hero_name_index = self.hero_name_list.index(hero_name)
            hero_line: int = self.hero_line_list[hero_name_index]

            value_list: list[tuple] = [('AttackDamageMin', self.doubleSpinBox_13.value(), 0),
                                       ('AttackDamageMax', self.doubleSpinBox_14.value(), 0),
                                       ('AttackRate', self.doubleSpinBox_15.value(), 1),
                                       ('AttackAnimationPoint', self.doubleSpinBox_16.value(), 2),
                                       ('AttackRange', self.doubleSpinBox_17.value(), 0),
                                       ('ProjectileSpeed', self.doubleSpinBox_24.value(), 0),
                                       ('AttributeBaseStrength', self.doubleSpinBox_18.value(), 0),
                                       ('AttributeStrengthGain', self.doubleSpinBox_19.value(), 1),
                                       ('AttributeBaseIntelligence', self.doubleSpinBox_20.value(), 0),
                                       ('AttributeIntelligenceGain', self.doubleSpinBox_21.value(), 1),
                                       ('AttributeBaseAgility', self.doubleSpinBox_22.value(), 0),
                                       ('AttributeAgilityGain', self.doubleSpinBox_23.value(), 1),
                                       ('MovementSpeed', self.doubleSpinBox_12.value(), 0),
                                       ('ArmorPhysical', self.doubleSpinBox_25.value(), 0)]

            for keyword, value, point in value_list:
                keyword: str
                value: float
                point: int

                line_num: int = hero_line + 1
                for one_line in self.file_content[hero_line:]:
                    one_line: str

                    if keyword in one_line:
                        print(Fore.LIGHTYELLOW_EX + str(line_num), one_line, end='\r')
                        one_list: list[str] = one_line.split('"')

                        if len(one_list) == 5 and one_list[4] == '\n':
                            one_list[3] = f'{value:.{point}f}'
                            one_line = '"'.join(one_list)
                            print(Fore.LIGHTGREEN_EX + str(line_num), Fore.LIGHTGREEN_EX + one_line, end='\r')
                            self.file_content[line_num - 1] = one_line
                            break

                    line_num += 1
        except:
            print(Fore.LIGHTRED_EX + 'Somthing is worry T_T')

    def set_to_top(self):
        if self.checkBox.isChecked() is True:
            self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)  # window top
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowStaysOnTopHint)  # cancel
        self.show()

    def init_attr_button(self):
        self.pushButton_37.clicked.connect(lambda: self.add_attr('base'))
        self.pushButton_38.clicked.connect(lambda: self.add_attr('gain'))
        self.pushButton_39.clicked.connect(lambda: self.add_attr('move'))
        self.pushButton_40.clicked.connect(lambda: self.add_attr('rate'))
        self.pushButton_41.clicked.connect(lambda: self.add_attr('anim'))
        self.pushButton_42.clicked.connect(lambda: self.add_attr('range'))
        self.pushButton_43.clicked.connect(lambda: self.add_attr('speed'))
        self.pushButton_44.clicked.connect(lambda: self.add_attr('attack'))
        self.pushButton_57.clicked.connect(lambda: self.add_attr('armor'))

    def add_attr(self, x):
        match x:
            case 'base':
                self.doubleSpinBox_18.setValue(self.doubleSpinBox_18.value() + 1)
                self.doubleSpinBox_20.setValue(self.doubleSpinBox_20.value() + 1)
                self.doubleSpinBox_22.setValue(self.doubleSpinBox_22.value() + 1)
                print(self.pushButton_37.text())
            case 'gain':
                self.doubleSpinBox_19.setValue(self.doubleSpinBox_19.value() + 1)
                self.doubleSpinBox_21.setValue(self.doubleSpinBox_21.value() + 1)
                self.doubleSpinBox_23.setValue(self.doubleSpinBox_23.value() + 1)
                print(self.pushButton_38.text())
            case 'move':
                self.doubleSpinBox_12.setValue(self.doubleSpinBox_12.value() + 10)
                print(self.pushButton_39.text())
            case 'rate':
                self.doubleSpinBox_15.setValue(self.doubleSpinBox_15.value() - 0.1)
                print(self.pushButton_40.text())
            case 'anim':
                self.doubleSpinBox_16.setValue(self.doubleSpinBox_16.value() - 0.1)
                print(self.pushButton_41.text())
            case 'range':
                self.doubleSpinBox_17.setValue(self.doubleSpinBox_17.value() + 100)
                print(self.pushButton_42.text())
            case 'speed':
                self.doubleSpinBox_24.setValue(self.doubleSpinBox_24.value() + 100)
                print(self.pushButton_43.text())
            case 'attack':
                self.doubleSpinBox_13.setValue(self.doubleSpinBox_13.value() + 10)
                self.doubleSpinBox_14.setValue(self.doubleSpinBox_14.value() + 10)
                print(self.pushButton_44.text())
            case 'armor':
                self.doubleSpinBox_25.setValue(self.doubleSpinBox_25.value() + 1)
                print(self.pushButton_57.text())

    @staticmethod
    def open_vpk_file():
        folder_path = r'D:\PycharmProjects\Dota-Tool\vpk\pak01_dir\scripts\npc'
        print(f'open_vpk_file : {Fore.LIGHTBLUE_EX + folder_path}')
        os.startfile(folder_path)

    @staticmethod
    def run_vpk_script():
        print('run_vpk_script')
        order = 'echo create vpk file... && "vpk/vpk.exe" "vpk/pak01_dir" && timeout 3'
        os.system(f'start cmd /k "{order}"')

    def add_attr_2(self):
        self.pushButton_44.click()  # 攻击+10
        self.pushButton_40.click()  # 攻击速率-0.1
        self.pushButton_41.click()  # 攻击前摇-0.1
        self.pushButton_42.click()  # 攻击范围+100
        self.pushButton_43.click(), self.pushButton_43.click(), self.pushButton_43.click()  # 弹道速度+300
        self.pushButton_37.click()  # 全属性+1
        self.pushButton_38.click()  # 全成长+1
        self.pushButton_39.click(), self.pushButton_39.click()  # 移速+20
        self.pushButton_57.click()  # 护甲+1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())
