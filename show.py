import sys

from PyQt5.QtCore import pyqtSlot, QObject
from PyQt5.QtWidgets import QApplication, QTableView, QWidget, QHBoxLayout
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from mouse_key import Operate
from task import AutoFarm

class MyWidget(QWidget):

    def __init__(self, hwnd, location, monster, line):
        super().__init__()

        # 初始化用户界面
        self.initUI()

    def initUI(self):
        # 设置窗口标题和大小
        self.setWindowTitle('QTable View Example')
        self.resize(500, 300)

        # 创建水平布局
        h_layout = QHBoxLayout()

        # 创建一个TableView并将其放置在水平布局中
        table_view = QTableView(self)
        h_layout.addWidget(table_view)

        # 创建一个数据模型
        self.model  = QStandardItemModel(10, 4)

        # 设置数据模型的表头标签
        self.model.setHorizontalHeaderLabels(["位置", "怪物", "距离下次刷新时间", "当前状态"])


        # 将数据模型设置给TableView
        table_view.setModel(self.model)

        # 调整所有列的宽度以适应内容
        table_view.resizeColumnsToContents()

        # 调整所有行的高度以适应内容
        table_view.resizeRowsToContents()

        # 显示网格线
        table_view.showGrid()

        # 将水平布局设置为窗口的布局
        self.setLayout(h_layout)

    def proc_data(self, data):
        for row in range(len(data)):
                for column in range(4):
                    item = QStandardItem(data[row][column])
                    self.model.setItem(row, column, item)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = QtableViewExample()
    ex.show()
    sys.exit(app.exec_())