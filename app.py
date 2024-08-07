# -*- coding: utf-8 -*-
"""
Time:   2024/3/23 14:58
Auth:   Jeremy
File:   app.py
IDE:    PyCharm
GitHub: https://github.com/JeremyChim
"""
import configparser
import os
import shutil
import sys
from time import sleep


import pyperclip
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDragEnterEvent, QDropEvent
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QWidget, QFileDialog
from colorama import init, Fore

from untitled import Ui_Form
from script.calc_num2 import calculate_next_two_elements_from_string as calc2
from script import scepter

init(autoreset=True)
config = configparser.ConfigParser()


class Window(QWidget, Ui_Form):

    def init_ui(self):
        self.setupUi(self)
        self.setWindowTitle('Dota Tool')
        self.setWindowIcon(QIcon('app.ico'))
        self.lineEdit_4.setText('2024/08/04')
        self.lineEdit_5.setText('1.19.1')

    def __init__(self):
        super().__init__()

        self.unit_data: list[str] = ['']  # 单位数据
        self.hero_data: list[str] = ['']  # 英雄数据
        self.hero_name_list: list[str] = []  # 英雄列表
        self.hero_line_list: list[int] = []  # 英雄所在行列表

        # 防御塔所在行列表
        self.good_list: list[int] = [511, 602, 693,
                                     1327, 1418, 1509, 1599, 1689, 1779,
                                     5938, 6031, 6124]
        self.bad_list: list[int] = [238, 329, 420,
                                    784, 875, 966, 1057, 1147, 1237,
                                    5659, 5752, 5845]

        self.init_ui()  # 初始化ui
        self.init_button()  # 初始化按钮
        self.init_attr_button()  # 初始化属性按钮
        self.setAcceptDrops(True)  # 允许拖放，拖放路径读取功能

        # 默认首次点击
        self.read_config_pushButton.click()  # 读取配置
        self.unit_load_pushButton.click()  # 读取单位数据
        self.hero_load_pushButton.click()  # 读取英雄数据
        self.load_hero_name_pushButton.click()  # 读取英雄列表数据
        self.load_hero_value_pushButton.click()  # 读取英雄数值

    def init_button(self):

        # 置顶按钮
        # 游戏路径
        # 保存配置
        # 读取配置
        self.set_top_checkBox.clicked.connect(self.set_to_top)
        self.game_path_pushButton.clicked.connect(lambda: self.get_file_url2(self.game_path_lineEdit, ""))
        self.set_config_pushButton.clicked.connect(self.set_config)
        self.read_config_pushButton.clicked.connect(self.read_config)

        # 读取路径，单位
        # 保存路径，单位
        # 读取，单位
        # 保存，单位
        self.browse_unit_load_path_pushButton.clicked.connect(lambda: self.get_file_url(self.unit_load_path_lineEdit))
        self.browse_unit_save_path_pushButton.clicked.connect(
            lambda: self.get_file_url2(self.unit_save_path_lineEdit, "/npc_units.txt"))
        self.unit_load_pushButton.clicked.connect(lambda: self.get_unit_data(self.unit_load_path_lineEdit))
        self.unit_save_pushButton.clicked.connect(
            lambda: self.save_file(self.unit_save_path_lineEdit.text(), self.unit_data))

        # 天辉小兵
        # 夜魇小兵
        # 其他单位
        # 防御塔
        self.good_guy_pushButton.clicked.connect(self.update_good_guy)
        self.bad_guy_pushButton.clicked.connect(self.update_bad_guy)
        self.other_guy_pushButton.clicked.connect(self.update_other_guy)
        self.update_tower_pushButton.clicked.connect(self.update_tower_data)

        # 读取路径，英雄
        # 保存路径，英雄
        # 读取，英雄
        # 保存，英雄
        self.browse_hero_load_path_pushButton.clicked.connect(lambda: self.get_file_url(self.hero_load_path_lineEdit))
        self.browse_hero_save_path_pushButton.clicked.connect(
            lambda: self.get_file_url2(self.hero_save_path_lineEdit, "/npc_heroes.txt"))
        self.hero_load_pushButton.clicked.connect(lambda: self.get_hero_data(self.hero_load_path_lineEdit))
        self.hero_save_pushButton.clicked.connect(
            lambda: self.save_file(self.hero_save_path_lineEdit.text(), self.hero_data))
        self.hero_save_pushButton_2.clicked.connect(
            lambda: self.save_file(self.hero_save_path_lineEdit.text(), self.hero_data))

        # 读取英雄名
        # 读取英雄数值
        # 写入新的数值
        # 搜索英雄名
        # 当英雄名发生变化，自动获取英雄数值
        self.load_hero_name_pushButton.clicked.connect(self.get_hero_name)
        self.load_hero_value_pushButton.clicked.connect(self.get_hero_value)
        self.update_hero_value_pushButton.clicked.connect(self.update_hero_data)
        self.search_hero_lineEdit.textChanged.connect(self.search_hero)
        self.hero_name_comboBox.currentIndexChanged.connect(self.load_hero_value_pushButton.click)

        # 魔晶技能替换
        # 普通技能计算
        # 终极技能计算
        self.pushButton_9.clicked.connect(self.ability_replace)
        self.pushButton_58.clicked.connect(self.ability_calc)
        self.pushButton_64.clicked.connect(lambda: self.ability_calc(is_big_ab=True))

        # 打开VPK配置文件夹
        # 生成VPK文件
        # 打开gi文件
        # 打开gi2文件
        # 打开MOD文件夹
        self.open_vpk_file_pushButton.clicked.connect(self.open_vpk_file)
        self.create_vpk_pushButton.clicked.connect(self.create_vpk)
        self.open_gi_pushButton.clicked.connect(self.open_gi_file)
        self.open_gi2_pushButton.clicked.connect(self.open_gi2_file)
        self.open_mod_file_pushButton.clicked.connect(self.open_mod_file)

        # 将VPK文件移动至MOD文件夹
        # 开始Dota2
        # 一键生成VPK，移动至MOD，并启动Dota2
        self.move_vpk_mod_pushButton.clicked.connect(self.move_vpk_mod)
        self.start_dota2_pushButton.clicked.connect(self.start_dota2)
        self.vpk_mod_dota2_pushButton.clicked.connect(self.vpk_mod_dota2)

        # 夜间视野+
        # 属性+++
        # 天赋属性点清空
        # 复制英雄技能文件至VPK配置文件夹
        # 复制英雄名
        self.pushButton.clicked.connect(self.add_night)
        self.pushButton_56.clicked.connect(self.add_attr_2)
        self.pushButton_67.clicked.connect(self.add_lv25)
        self.copy_hero_ab_pushButton.clicked.connect(self.copy_hero_ab)
        self.copy_hero_name_pushButton.clicked.connect(self.copy_hero_name)

        # 打开旧的npc_units.txt
        # 打开新的npc_units.txt
        # 打开旧的npc_heroes.txt
        # 打开新的npc_heroes.txt
        self.open_load_unitstxt_pushButton.clicked.connect(lambda: self.open_txt(self.unit_load_path_lineEdit.text()))
        self.open_save_unitstxt_pushButton.clicked.connect(lambda: self.open_txt(self.unit_save_path_lineEdit.text()))
        self.open_load_herotxt_pushButton.clicked.connect(lambda: self.open_txt(self.hero_load_path_lineEdit.text()))
        self.open_save_herotxt_pushButton.clicked.connect(lambda: self.open_txt(self.hero_save_path_lineEdit.text()))

    def read_config(self):
        try:
            # 读取项目路径中的NPC文件
            unit_load_path = (os.getcwd() + '/npc/npc_units.txt').replace('\\', '/')
            hero_load_path = (os.getcwd() + '/npc/npc_heroes.txt').replace('\\', '/')
            unit_save_path = (os.getcwd() + '/vpk/pak01_dir/scripts/npc/npc_units.txt').replace('\\', '/')
            hero_save_path = (os.getcwd() + '/vpk/pak01_dir/scripts/npc/npc_heroes.txt').replace('\\', '/')
            self.unit_load_path_lineEdit.setText(unit_load_path)
            self.hero_load_path_lineEdit.setText(hero_load_path)
            self.unit_save_path_lineEdit.setText(unit_save_path)
            self.hero_save_path_lineEdit.setText(hero_save_path)

            # 读取config.ini
            config.read('config.ini')
            game_path = config.get('path', 'game_path')

            # 尝试读取配置
            self.game_path_lineEdit.setText(game_path)
            print(Fore.LIGHTGREEN_EX + '读取config.ini配置成功。')

        except Exception as e:
            print(Fore.LIGHTGREEN_EX + f'读取config.ini配置失败，原因：{e}')

    def copy_hero_name(self):
        """复制英雄名"""
        try:
            name = self.hero_name_comboBox.currentText()
            print(f'复制英雄名：{Fore.LIGHTMAGENTA_EX + name}')
            pyperclip.copy(name)
        except Exception as e:
            print(f'复制英雄名发生错误，原因：{e}')

    @staticmethod
    def open_txt(path):
        """打开txt"""
        try:
            print(f'打开文件，路径： {Fore.LIGHTBLUE_EX + path}')
            os.startfile(path)
        except Exception as e:
            print(Fore.LIGHTRED_EX + f'打开文件{path}错误，错误原因：{e}。')

    def vpk_mod_dota2(self):
        """生成vpk并移动至mod"""
        self.create_vpk_pushButton.click()  # 生成vpk
        sleep(1)  # 等待1秒
        self.move_vpk_mod_pushButton.click()  # 移动到mod
        self.start_dota2_pushButton.click()  # 启动DOTA2

    def copy_hero_ab(self):
        """复制npc_heroes.txt到目标路径"""
        hero_txt = self.hero_name_comboBox.currentText() + '.txt'
        # print(f'复制文件名：{hero_txt}')

        src = self.hero_load_path_lineEdit.text().replace('npc_heroes.txt', f'heroes/{hero_txt}')  # 替换路径
        dst = self.hero_save_path_lineEdit.text().replace('npc_heroes.txt', f'heroes/{hero_txt}')  # 替换路径

        try:
            shutil.copy(src, dst)  # src 是源路径，dst 是目标路径
            os.startfile(dst)
            print(Fore.LIGHTGREEN_EX + f"文件 {src} 已成功复制到 {dst}，正在打开")
        except OSError as e:
            print(Fore.LIGHTRED_EX + f"文件复制失败: {e.strerror}")

    def search_hero(self):
        """搜索英雄名"""
        try:
            # 清除当前组合框的选项
            self.hero_name_comboBox.clear()
            # 遍历英雄名
            for name in self.hero_name_list:
                if self.search_hero_lineEdit.text() in name:
                    self.hero_name_comboBox.addItem(name)
        except:
            pass

    @staticmethod
    def get_file_url2(line_edit, file_name: str):
        """获取文件路径（选择文件夹）"""
        file_url = QFileDialog.getExistingDirectory(directory=os.getcwd())
        if file_url:
            file_url = file_url + file_name
            line_edit.setText(file_url)
            print(f'获取文件夹路径：{Fore.LIGHTCYAN_EX + file_url}')

    @staticmethod
    def get_file_url(line_edit):
        """获取文件路径（选择文件）"""
        file_url, file_type = QFileDialog.getOpenFileName()  # 打开文件管理器
        if file_url:
            line_edit.setText(file_url)
            print(f'获取文件路径：{Fore.LIGHTCYAN_EX + file_url}')

    def get_unit_data(self, line_edit):
        """获取单位数据"""
        file_url = line_edit.text()
        try:
            with open(file_url, 'r') as f:
                self.unit_data = f.readlines()  # 获取内容，列表类型
                print(Fore.LIGHTGREEN_EX + '读取单位数据成功，',
                      Fore.LIGHTBLUE_EX + f'共有{len(self.unit_data)}行，',
                      Fore.LIGHTCYAN_EX + f'读取路径：{file_url}。')
        except Exception as e:
            print(Fore.LIGHTRED_EX + f'读取单位数据失败！原因是：{e.__str__()}')

    def get_hero_data(self, line_edit):
        """获取英雄数据"""
        file_url = line_edit.text()
        try:
            with open(file_url, 'r') as f:
                self.hero_data = f.readlines()  # 获取内容，列表类型
                print(Fore.LIGHTGREEN_EX + '读取英雄数据成功，',
                      Fore.LIGHTBLUE_EX + f'共有{len(self.hero_data)}行，',
                      Fore.LIGHTCYAN_EX + f'读取路径：{file_url}。')
        except Exception as e:
            print(Fore.LIGHTRED_EX + f'读取英雄数据失败！原因是：{e.__str__()}')

    @staticmethod
    def save_file(save_path, file_content):
        """保存文件"""
        try:
            with open(save_path, 'w') as f:
                f.writelines(file_content)
                print(Fore.LIGHTGREEN_EX + '保存数据成功，',
                      Fore.LIGHTBLUE_EX + f'共有{len(file_content)}行，',
                      Fore.LIGHTCYAN_EX + f'保存路径：{save_path}')
        except Exception as e:
            print(Fore.LIGHTRED_EX + f'保存数据错误，原因是：{e}')

    def update_good_guy(self):
        """更新天辉小兵的数据"""
        try:
            factor: float = self.good_guy_doubleSpinBox.value()
            print(Fore.LIGHTBLUE_EX + f'天辉小兵系数：{factor}')

            line_num: int = 1  # MAKE LINE
            for one_line in self.unit_data:
                one_line: str

                if line_num in self.good_list or line_num - 1 in self.good_list or line_num - 2 in self.good_list:
                    if 'BountyXP' in one_line or 'BountyGoldMin' in one_line or 'BountyGoldMax' in one_line:
                        print(Fore.LIGHTBLACK_EX + str(line_num) + one_line, end='\r')
                        one_list: list[str] = one_line.split('"')  # 旧的数据
                        one_list[3] = f'{float(one_list[3]) * factor:.0f}'  # 计算
                        one_line = '"'.join(one_list)  # 新的数据
                        print(Fore.LIGHTYELLOW_EX + str(line_num) + one_line, end='\r')
                        self.unit_data[line_num - 1] = one_line  # 全局写入

                elif line_num in self.bad_list or line_num - 1 in self.bad_list or line_num - 2 in self.bad_list:
                    pass

                else:
                    pass

                line_num += 1
            print(Fore.LIGHTGREEN_EX + '天辉小兵数据更新成功。')
        except Exception as e:
            print(Fore.LIGHTRED_EX + f'数据更新失败！原因是：{e}')

    def update_bad_guy(self):
        """更新夜宴小兵的数据"""
        try:
            factor: float = self.bad_guy_doubleSpinBox.value()
            print(Fore.LIGHTBLUE_EX + f'夜魇小兵系数：{factor}')

            line_num: int = 1  # MAKE LINE
            for one_line in self.unit_data:
                one_line: str

                if line_num in self.good_list or line_num - 1 in self.good_list or line_num - 2 in self.good_list:
                    pass

                elif line_num in self.bad_list or line_num - 1 in self.bad_list or line_num - 2 in self.bad_list:
                    if 'BountyXP' in one_line or 'BountyGoldMin' in one_line or 'BountyGoldMax' in one_line:
                        print(Fore.LIGHTBLACK_EX + str(line_num) + one_line, end='\r')
                        one_list: list[str] = one_line.split('"')  # 旧的数据
                        one_list[3] = f'{float(one_list[3]) * factor:.0f}'  # 计算
                        one_line = '"'.join(one_list)  # 新的数据
                        print(Fore.LIGHTYELLOW_EX + str(line_num) + one_line, end='\r')
                        self.unit_data[line_num - 1] = one_line  # 全局写入

                else:
                    pass

                line_num += 1
            print(Fore.LIGHTGREEN_EX + '夜魇小兵数据更新成功。')
        except Exception as e:
            print(Fore.LIGHTRED_EX + f'数据更新失败！原因是：{e}')

    def update_other_guy(self):
        """更新野怪的数据"""
        try:
            factor: float = self.other_guy_doubleSpinBox.value()
            print(Fore.LIGHTBLUE_EX + f'factor : {factor}')

            line_num: int = 1  # MAKE LINE
            for one_line in self.unit_data:
                one_line: str

                if line_num in self.good_list or line_num - 1 in self.good_list or line_num - 2 in self.good_list:
                    pass

                elif line_num in self.bad_list or line_num - 1 in self.bad_list or line_num - 2 in self.bad_list:
                    pass

                else:
                    if 'BountyXP' in one_line or 'BountyGoldMin' in one_line or 'BountyGoldMax' in one_line:
                        print(Fore.LIGHTBLACK_EX + str(line_num) + one_line, end='\r')
                        one_list: list[str] = one_line.split('"')  # 旧的数据
                        one_list[3] = f'{float(one_list[3]) * factor:.0f}'  # 计算
                        one_line = '"'.join(one_list)  # 新的数据
                        print(Fore.LIGHTYELLOW_EX + str(line_num) + one_line, end='\r')
                        self.unit_data[line_num - 1] = one_line  # 全局写入

                line_num += 1
            print(Fore.LIGHTGREEN_EX + '其他单位数据更新成功。')
        except:
            print(Fore.LIGHTRED_EX + '数据更新失败！')

    def update_tower(self, keyword: str, keyword2: str, mul: float, add: int):
        """更新防御塔和基地的数据"""
        try:
            print(Fore.LIGHTBLUE_EX + f'更新防御塔数据，',
                  Fore.LIGHTBLUE_EX + f'一级关键词：{keyword} ，',
                  Fore.LIGHTBLUE_EX + f'二级关键词：{keyword2} ，',
                  Fore.LIGHTBLUE_EX + f'乘系数: {mul} ，',
                  Fore.LIGHTBLUE_EX + f'加系数: {add} 。')

            line_num: int = 1  # MAKE LINE
            for one_line in self.unit_data:
                one_line: str
                if keyword in one_line:
                    print(Fore.LIGHTMAGENTA_EX + str(line_num) + one_line, end='\r')
                    key_line: str
                    line_num2 = line_num + 1
                    for key_line in self.unit_data[line_num:]:
                        if keyword2 in key_line:
                            print(Fore.LIGHTBLACK_EX + str(line_num2) + key_line, end='\r')
                            key_list: list[str] = key_line.split('"')  # OLD DATA
                            key_list[3] = f'{float(key_list[3]) * mul + add:.0f}'  # CALC
                            key_line = '"'.join(key_list)  # NEW DATA
                            print(Fore.LIGHTYELLOW_EX + str(line_num2) + key_line, end='\r')
                            self.unit_data[line_num2 - 1] = key_line  # Write to Global
                            break
                        line_num2 += 1
                line_num += 1
        except:
            print(Fore.LIGHTRED_EX + '数据更新失败！')

    def update_tower_data(self):
        """绑定数据框（防御塔）"""
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
            if arg[2] == 1 and arg[3] == 0:  # 如果乘1加0，就不进行计算了
                pass
            else:
                self.update_tower(*arg)

    def ability_replace(self):
        """魔晶技能替换"""
        self.textEdit_3.clear()
        mod: str = self.textEdit.toPlainText()
        old_content: str = self.textEdit_2.toPlainText()
        old_lines: list[str] = old_content.split('\n')

        for old_ab in old_lines:
            old_ab: str

            if old_ab:
                old_ab_list: list[str] = old_ab.split('"')

                v1 = old_ab_list[3]
                v2 = v1.split(' ')
                if len(v2) > 1:
                    v3, v4 = calc2(v1)
                    scepter_value, max_value = scepter.func(float(v2[-1]), float(v4))

                    new_ab: str = (mod.
                                   replace('ab_name', old_ab_list[1]).
                                   replace('ab_value', v3).
                                   replace('=0', f'+{v4}').
                                   replace('=1', f'={scepter_value}').
                                   replace('max_value', f'{max_value}')
                                   )


                else:
                    new_ab: str = (mod.
                                   replace('ab_name', old_ab_list[1]).
                                   replace('ab_value', old_ab_list[3]))

                # 写入文本框
                self.textEdit_3.append(new_ab)

                print(old_ab)
                # print(mod)
                print(Fore.LIGHTBLUE_EX + new_ab)
            else:
                print(Fore.LIGHTRED_EX + '技能替换失败！')

    def get_hero_name(self):
        """获取英雄列表"""
        try:
            hero_name_list: list[str] = []
            hero_line_list: list[int] = []
            line_num: int = 1  # MAKE LINE
            for one_line in self.hero_data:
                one_line: str
                if '\t"npc_dota_hero_' in one_line and one_line.split('"')[2] == '\n':
                    print(Fore.LIGHTYELLOW_EX + str(line_num), one_line, end='\r')
                    hero_name: str = one_line.split('"')[1]
                    hero_name_list.append(hero_name)  # 获取英雄名字，加入列表
                    hero_line_list.append(line_num)  # 获取所在行号，加入列表
                    self.hero_name_comboBox.addItem(hero_name)
                line_num += 1
            print(Fore.LIGHTGREEN_EX + '读取英雄名成功，',
                  Fore.LIGHTBLUE_EX + f'共有英雄{len(hero_name_list) - 1}名（base是英雄通用模型）。')
            self.hero_name_list = hero_name_list
            self.hero_line_list = hero_line_list
        except:
            print(Fore.LIGHTRED_EX + '读取英雄名失败！')

    def get_hero_value(self):
        """获取英雄属性值"""
        try:
            hero_name = self.hero_name_comboBox.currentText()
            hero_name_index = self.hero_name_list.index(hero_name)
            hero_line: int = self.hero_line_list[hero_name_index]
            print(f'英雄名：{Fore.LIGHTMAGENTA_EX + hero_name}',
                  f'索引：{Fore.LIGHTBLUE_EX + str(hero_name_index)}',
                  f'行号：{Fore.LIGHTYELLOW_EX + str(hero_line)}。')

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

                for one_line in self.hero_data[hero_line:]:
                    one_line: str
                    if keyword in one_line:
                        one_list: list[str] = one_line.split('"')
                        if len(one_list) == 5 and one_list[4] == '\n':
                            value: float = float(one_list[3])
                            function()
                            break

                    line_num += 1
        except:
            print(Fore.LIGHTRED_EX + f'读取英雄数值失败！')

    def add_lv25(self):
        """添加25级天赋槽"""
        try:
            hero_name = self.hero_name_comboBox.currentText()
            hero_name_index = self.hero_name_list.index(hero_name)
            hero_line: int = self.hero_line_list[hero_name_index]

            line_num: int = hero_line + 1
            for one_line in self.hero_data[hero_line:]:
                if "Ability17" in one_line:
                    self.hero_data[line_num - 1] = one_line + '\t\t"Ability25"\t\t""\n'
                    print(Fore.LIGHTYELLOW_EX + str(line_num), self.hero_data[line_num - 1])
                    break

                line_num += 1

        except:
            print(Fore.LIGHTRED_EX + '写入新的等级25天赋技能失败！')

    def add_night(self):
        """夜间视野+"""
        try:
            hero_name = self.hero_name_comboBox.currentText()
            hero_name_index = self.hero_name_list.index(hero_name)
            hero_line: int = self.hero_line_list[hero_name_index]

            line_num: int = hero_line + 1
            for one_line in self.hero_data[hero_line:]:
                if "MovementSpeed" in one_line:
                    self.hero_data[line_num - 1] = one_line + '\t\t"VisionNighttimeRange"\t\t"1800"\n'
                    print(Fore.LIGHTYELLOW_EX + str(line_num), self.hero_data[line_num - 1])
                    break

                line_num += 1

        except:
            print(Fore.LIGHTRED_EX + '写入夜间视野+失败！')

    def update_hero_data(self):
        """绑定数据框（英雄）"""
        try:
            hero_name = self.hero_name_comboBox.currentText()
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
                for one_line in self.hero_data[hero_line:]:
                    one_line: str

                    if keyword in one_line:
                        print(Fore.LIGHTYELLOW_EX + str(line_num), one_line, end='\r')
                        one_list: list[str] = one_line.split('"')

                        if len(one_list) == 5 and one_list[4] == '\n':
                            one_list[3] = f'{value:.{point}f}'
                            one_line = '"'.join(one_list)
                            print(Fore.LIGHTGREEN_EX + str(line_num), Fore.LIGHTGREEN_EX + one_line, end='\r')
                            self.hero_data[line_num - 1] = one_line
                            break

                    line_num += 1
        except:
            print(Fore.LIGHTRED_EX + '写入新的数值失败！')

    def set_to_top(self):
        if self.set_top_checkBox.isChecked() is True:
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
        folder_name = os.getcwd() + '/vpk/pak01_dir/scripts/npc'
        folder_name2 = os.getcwd() + '/vpk/pak01_dir/scripts/npc/heroes'

        # 检查文件夹是否存在
        if os.path.exists(folder_name):
            print(f"vpk配置文件夹 {folder_name} 已存在，正在打开")
            os.startfile(folder_name)
            if not os.path.exists(folder_name2):
                os.makedirs(folder_name2)
        else:
            # 如果文件夹不存在，则创建它
            try:
                os.makedirs(folder_name)
                os.makedirs(folder_name2)
                print(f"vpk配置文件夹 {folder_name} 已创建，正在打开")
                os.startfile(folder_name)
            except OSError as e:
                print(Fore.LIGHTRED_EX + f"创建文件夹 {folder_name} 时出错: {e}")

    @staticmethod
    def create_vpk():
        """生产vpk"""
        print('正在创建vpk文件中。。。')
        order = 'echo create vpk file... && "vpk/vpk.exe" "vpk/pak01_dir" && timeout 1 && exit'
        os.system(f'start cmd /k "{order}"')

    def add_attr_2(self):
        """全属性+++"""
        self.pushButton_44.click()  # 攻击+10
        self.pushButton_40.click()  # 攻击速率-0.1
        self.pushButton_41.click()  # 攻击前摇-0.1
        self.pushButton_42.click()  # 攻击范围+100
        if self.doubleSpinBox_24.value() != 0:  # 如果有弹道速度的话
            self.pushButton_43.click(), self.pushButton_43.click(), self.pushButton_43.click()  # 弹道速度+300
        self.pushButton_37.click()  # 全属性+1
        self.pushButton_38.click()  # 全成长+1
        self.pushButton_39.click(), self.pushButton_39.click()  # 移速+20
        self.pushButton_57.click()  # 护甲+1
        self.update_hero_value_pushButton.click()  # 写入
        self.pushButton.click()  # 夜间视野 1800

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        """拖拽功能"""
        # 当有文件拖入窗口时触发
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent) -> None:
        """拖拽识别路径"""
        # 当文件被放下时触发
        for url in event.mimeData().urls():
            file_url = url.toLocalFile()
            print(f'Get file url : {Fore.LIGHTCYAN_EX + file_url}')
            if 'npc_units.txt' in file_url:
                self.unit_load_path_lineEdit.setText(file_url)  # SENT THE URL - unit
            elif 'npc_heroes.txt' in file_url:
                self.hero_load_path_lineEdit.setText(file_url)  # SENT THE URL - hero
            elif 'dota 2 beta' in file_url:
                self.game_path_lineEdit.setText(file_url)  # SENT THE URL - steam

    def ability_calc(self, is_big_ab: bool = False):
        """技能计算"""
        try:
            self.textEdit_5.clear()
            for original_string in self.textEdit_4.toPlainText().split('\n'):
                original_string: str
                original_list: list[str] = original_string.split('"')
                num_string: str = original_list[3]

                new_string, _ = calc2(num_string, is_big_ab)
                original_list[3] = new_string
                new = '"'.join(original_list)

                # 输出结果
                self.textEdit_5.append(new)
                print(new)

        except:
            print(Fore.LIGHTRED_EX + '技能计算失败！')

    def open_gi_file(self):
        """打开gi文件"""
        try:
            path = self.game_path_lineEdit.text() + r'/dota/gameinfo.gi'
            print(f'正在打开gameinfo.gi文件，路径：{Fore.LIGHTBLUE_EX + path}')
            os.startfile(path)
        except Exception as e:
            print(Fore.LIGHTRED_EX + f'打开gameinfo.gi文件失败！原因是：{e.__str__()}')

    def open_gi2_file(self):
        """打开gi2文件"""
        try:
            path = self.game_path_lineEdit.text() + '/dota/gameinfo_branchspecific.gi'
            print(f'正在打开gameinfo_branchspecific.gi文件，路径：{Fore.LIGHTBLUE_EX + path}')
            os.startfile(path)
        except Exception as e:
            print(Fore.LIGHTRED_EX + f'打开gameinfo_branchspecific.gi文件失败！原因是：{e.__str__()}')

    def open_mod_file(self):
        """创建/打开mod文件"""
        folder_name = self.game_path_lineEdit.text() + '/mod'

        # 检查文件夹是否存在
        if os.path.exists(folder_name):
            print(f"文件夹 {folder_name} 已存在，正在打开")
            os.startfile(folder_name)
        else:
            # 如果文件夹不存在，则创建它
            try:
                os.makedirs(folder_name)
                print(f"文件夹 {folder_name} 已创建，正在打开")
                os.startfile(folder_name)
            except OSError as e:
                print(Fore.LIGHTRED_EX + f"创建文件夹 {folder_name} 时出错: {e}")

    def move_vpk_mod(self):
        """移动vpk至mod文件夹"""
        src = os.getcwd() + '/vpk/pak01_dir.vpk'
        dst = self.game_path_lineEdit.text() + '/mod/pak01_dir.vpk'

        try:
            shutil.move(src, dst)  # src 是源路径，dst 是目标路径
            print(Fore.LIGHTGREEN_EX + f"文件 {src} 已成功移动到 {dst}")
        except OSError as e:
            print(Fore.LIGHTRED_EX + f"文件移动失败: {e.strerror}")

    def start_dota2(self):
        path = self.game_path_lineEdit.text() + r'/bin/win64/dota2.exe'
        try:
            os.startfile(path)
            print(Fore.LIGHTGREEN_EX + '启动Dota2。。。。。。')
        except:
            print(Fore.LIGHTRED_EX + '启动Dota2失败！')

    def set_config(self):
        """写入配置"""
        try:
            config['path'] = {'game_path': self.game_path_lineEdit.text()}

            with open('config.ini', 'w') as configfile:
                config.write(configfile)
                print(Fore.LIGHTGREEN_EX + '写入配置成功。')
            os.startfile('config.ini')
        except:
            print(Fore.LIGHTRED_EX + '写入配置失败！')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())
