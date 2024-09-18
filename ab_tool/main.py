import os
import sys

from PyQt6.QtCore import QStringListModel, Qt
from PyQt6.QtWidgets import QApplication, QWidget, QFileDialog

from ab_script import ab_func
from lv_script import lv_func
from tab_script import tab_func
from try_script import try_func
from untitled import Ui_Form


class Win(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('ab tool')

        # 控件初始化
        self.pushButton.clicked.connect(lambda: self.load_func())
        self.pushButton_2.clicked.connect(lambda: self.calc_func(0))
        self.pushButton_3.clicked.connect(lambda: self.tab_func('+'))
        self.pushButton_4.clicked.connect(lambda: self.tab_func('-'))
        self.pushButton_5.clicked.connect(lambda: self.calc_func(0))
        self.pushButton_6.clicked.connect(lambda: self.save_func())
        self.pushButton_7.clicked.connect(lambda: self.undo_func())
        self.pushButton_8.clicked.connect(lambda: self.save_open_func())
        self.pushButton_9.clicked.connect(lambda: self.calc_func(0, 0))
        self.pushButton_10.clicked.connect(lambda: self.calc_func(0, 0))
        self.pushButton_11.clicked.connect(lambda: self.lv_func(4))
        self.pushButton_12.clicked.connect(lambda: self.lv_func(6))
        self.pushButton_13.clicked.connect(lambda: self.cut_func())
        self.pushButton_14.clicked.connect(lambda: self.paste_func())
        self.pushButton_15.clicked.connect(lambda: self.clean_func())
        self.pushButton_16.clicked.connect(lambda: self.calc_func(0, 2))
        self.pushButton_17.clicked.connect(lambda: self.calc_func(0, 3))
        self.pushButton_18.clicked.connect(lambda: self.calc_func(0, 4))
        self.pushButton_19.clicked.connect(lambda: self.calc_func(0, 5))
        self.pushButton_20.clicked.connect(lambda: self.calc_func(0, 6))
        self.pushButton_21.clicked.connect(lambda: self.calc_func(0, 6))
        self.radioButton.clicked.connect(lambda: self.top_func())
        self.label.setText('version: 1.3.0')
        self.setAcceptDrops(True)  # 开拖拽
        # self.radioButton.click()  # 置顶

        # 绑定快捷键
        self.pushButton.setShortcut('ctrl+l')
        self.pushButton_6.setShortcut('ctrl+s')
        self.pushButton_8.setShortcut('ctrl+o')
        self.radioButton.setShortcut('ctrl+t')
        self.pushButton_5.setShortcut('ctrl+1')
        self.pushButton_2.setShortcut('ctrl+2')
        self.pushButton_11.setShortcut('ctrl+4')
        self.pushButton_12.setShortcut('ctrl+6')
        self.pushButton_16.setShortcut('ctrl+9')
        self.pushButton_17.setShortcut('ctrl+0')
        self.pushButton_13.setShortcut('ctrl+x')
        self.pushButton_15.setShortcut('ctrl+c')
        self.pushButton_14.setShortcut('ctrl+v')
        self.pushButton_7.setShortcut('ctrl+z')

        self.fn = None  # 保存文件名的默认值
        self.ab = None  # 保存字段，方便回退
        self.url = None  # 保存路径
        self.board = []  # 剪切板

    @try_func
    def dragEnterEvent(self, event):
        """允许拖拽文件"""
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    @try_func
    def dropEvent(self, event):
        """处理拖放事件"""
        url = [u.toLocalFile() for u in event.mimeData().urls()][0]
        if url:
            with open(url, 'r') as f:
                ls = f.readlines()
            m = QStringListModel()  # 建立模型
            m.setStringList(ls)  # 写入内容至模型
            self.listView.setModel(m)  # lv绑定模型
            self.fn = url.split('/')[-1]  # 记忆文件名
            self.label.setText('load file. finsh.')

    @try_func
    def top_func(self):
        if self.radioButton.isChecked() is True:
            self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)  # window top
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowStaysOnTopHint)  # cancel
        self.show()

    @try_func
    def load_func(self):
        url, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "文本文件 (*.txt);;所有文件 (*)")
        if url:
            with open(url, 'r') as f:
                ls = f.readlines()
            m = QStringListModel()  # 建立模型
            m.setStringList(ls)  # 写入内容至模型
            self.listView.setModel(m)  # lv绑定模型
            self.fn = url.split('/')[-1]  # 记忆文件名
            self.pushButton_15.click()  # 清空剪切板
            self.label.setText(f'load file. finsh. url: {url}')

    @try_func
    def tab_func(self, x: str):
        """
        :param x: +是进格，-是退格
        """
        m = self.listView.model()  # 读模型，QStringListModel
        ls = self.listView.selectionModel().selectedIndexes()  # [<PyQt6.QtCore.QModelIndex>]
        for i in ls:
            ab = m.data(i)  # 读
            self.ab = str(ab)
            ab2 = tab_func(ab, x)  # +是进格，-是退格
            m.setData(i, ab2)  # 写

    @try_func
    def calc_func(self, x, y=None):
        """
        :param x: 1是大招，2是普通技
        :param y: 1是带{}，0是“”，2是只有魔晶{}，3是只有魔杖{}，4是只有魔晶""，5是只有魔杖""，不输入就自行判断
        """
        m = self.listView.model()  # 读模型，QStringListModel
        ls = self.listView.selectionModel().selectedIndexes()  # [<PyQt6.QtCore.QModelIndex>]
        for i in ls:
            ab = m.data(i)  # 读
            ab2 = ab_func(ab, x, y)  # 计算后x位
            m.setData(i, ab2)  # 写
            self.ab = f'{ab}'  # 备份原字段

    @try_func
    def undo_func(self):
        m = self.listView.model()  # 读模型，QStringListModel
        ls = self.listView.selectionModel().selectedIndexes()  # [<PyQt6.QtCore.QModelIndex>]
        for i in ls:
            if self.ab:
                m.setData(i, self.ab)  # 写

    @try_func
    def save_func(self):
        url, _ = QFileDialog.getSaveFileName(self, "保存文件", self.fn, "文本文件 (*.txt);;所有文件 (*)")
        if url:
            with open(url, 'w') as f:
                m = self.listView.model()  # 读模型，QStringListModel
                row = m.rowCount()  # 共多少行
                ls = []
                for r in range(row):
                    i = m.index(r, 0)  # r行0列
                    tx = m.data(i)  # 内容
                    ls.append(tx)  # 写入列表
                f.writelines(ls)  # 写
            self.url = f'{url}'
            self.label.setText(f'save file. finsh. url: {self.url}')

    @try_func
    def open_func(self):
        if self.url:
            os.startfile(self.url)

    @try_func
    def save_open_func(self):
        self.save_func()
        self.open_func()

    @try_func
    def lv_func(self, x):
        """
        :param x: "MaxLevel"   "x"
        """
        m = self.listView.model()  # 读模型，QStringListModel
        ls = self.listView.selectionModel().selectedIndexes()  # [<PyQt6.QtCore.QModelIndex>]
        for i in ls:
            t = m.data(i)  # 读
            t2 = lv_func(t, x)
            m.setData(i, t2)  # 写

    @try_func
    def cut_func(self):
        m = self.listView.model()  # 读模型，QStringListModel
        ls = self.listView.selectionModel().selectedIndexes()  # [<PyQt6.QtCore.QModelIndex>]
        for i in ls:
            t = m.data(i)  # 读
            self.board.append(t)  # 剪切
            m.setData(i, '')  # 删
        self.label.setText(f'cut finsh. len: {len(self.board)}')

    @try_func
    def paste_func(self):
        m = self.listView.model()  # 读模型，QStringListModel
        ls = self.listView.selectionModel().selectedIndexes()  # [<PyQt6.QtCore.QModelIndex>]
        for i in ls:
            t = m.data(i)  # 读
            t2 = '\n'.join(self.board)  # 读剪切板
            t3 = tab_func(t2, '+')  # 剪切板内容全部进格
            t4 = t + t3
            m.setData(i, t4 + '\n')  # 写
        self.pushButton_15.click()  # 清空剪切板
        self.label.setText('paste finsh.')

    @try_func
    def clean_func(self):
        self.board = []
        self.label.setText('board clean.')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Win()
    win.show()
    app.exec()
