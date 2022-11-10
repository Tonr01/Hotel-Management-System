from operator import truediv, truth
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QMessageBox,
                             QPushButton, QGridLayout, QLineEdit, QComboBox, QFrame, QTableWidgetItem)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets, QtCore
import pymysql

db_settings = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "a7630225",
    "db": "hotel_management",
    "charset": "utf8"
}
connection = pymysql.connect(**db_settings)    # 建立Connection物件
cursor = connection.cursor()    # 建立Cursor物件


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QGridLayout()
        self.setLayout(layout)

        # --------------------Window--------------------
        self.setWindowTitle('離島飯店管理系統')  # Window Title
        self.setGeometry(0, 0, 1000, 1000)  # Window Size (水平位置,垂直位置,寬,高)
        # Window background color
        self.setStyleSheet("background-color: white")

        # --------------------background--------------------
        self.label_background = QLabel('', self)  # label in window
        self.label_background.setGeometry(50, 100, 900, 900)
        self.label_background.setStyleSheet(
            "background-color: rgb(240,240,230)")  # label背景顏色
        self.label_background.setFrameShape(QFrame.Box)   # 設定邊框樣式
        self.label_background.setFrameShadow(QFrame.Raised)

        # --------------------Big Title--------------------
        self.Title = QLabel('離島飯店管理系統', self)
        self.Title.setGeometry(0, 10, 1000, 50)
        self.Title.setFont(QFont('Arial', 25))  # label字型、字體大小
        self.Title.setAlignment(Qt.AlignCenter)  # 字體置中

        # --------------------查詢工具--------------------
        self.label_function1_1 = QLabel('查詢工具', self)
        self.label_function1_1.setGeometry(50, 100, 200, 100)
        self.label_function1_1.setFont(QFont('Arial', 20))  # label字型、字體大小
        self.label_function1_1.setAlignment(Qt.AlignCenter)  # 字體置中
        self.label_function1_1.setFrameShape(QFrame.Box)   # 設定邊框樣式
        self.label_function1_1.setFrameShadow(QFrame.Raised)
        self.label_function1_1.setStyleSheet(
            "background-color: rgb(150,150,130)")    # label背景顏色

        self.label_function1_2 = QLabel('', self)
        self.label_function1_2.setGeometry(250, 100, 700, 100)
        self.label_function1_2.setFrameShape(QFrame.Box)   # 設定邊框樣式
        self.label_function1_2.setFrameShadow(QFrame.Raised)
        self.label_function1_2.setStyleSheet(
            "background-color: rgbrgb(240,240,230)")    # label背景顏色

        # --------------------查詢關鍵字--------------------
        self.label_function2 = QLabel('查詢關鍵字', self)
        self.label_function2.setGeometry(50, 200, 200, 150)
        self.label_function2.setFont(QFont('Arial', 20))  # label字型、字體大小
        self.label_function2.setAlignment(Qt.AlignCenter)  # 字體置中
        self.label_function2.setFrameShape(QFrame.Box)   # 設定邊框樣式
        self.label_function2.setFrameShadow(QFrame.Raised)
        self.label_function2.setStyleSheet(
            "background-color: rgb(150,150,130)")    # label背景顏色

        # --------------------關鍵字顯示區--------------------
        self.label_showarea = QLabel('', self)
        self.label_showarea.setGeometry(50, 410, 900, 200)
        self.label_showarea.setFont(QFont('Arial', 20))  # label字型、字體大小
        self.label_showarea.setWordWrap(True)  # 換行
        self.label_showarea.setAlignment(Qt.AlignTop)  # 字體向上對齊
        self.label_showarea.setFrameShape(QFrame.Box)   # 設定邊框樣式
        self.label_showarea.setFrameShadow(QFrame.Raised)
        self.label_showarea.setStyleSheet(
            "background-color: white")    # label背景顏色

        # --------------------打字區--------------------
        self.label_coding = QLineEdit(self)
        self.label_coding.setGeometry(250, 200, 700, 150)
        self.label_coding.setFont(QFont('Arial', 20))  # label字型、字體大小
        self.label_coding.setAlignment(Qt.AlignTop)  # 字體向上對齊
        self.label_coding.setStyleSheet(
            "background-color: rgbrgb(240,240,230)")    # label背景顏色

        # --------------------下拉式選單--------------------
        self.combobox_function = QComboBox(self)
        self.combobox_function.setGeometry(350, 120, 500, 60)
        self.combobox_function.setFont(
            QFont('Arial', 25))  # label字型、字體大小
        self.combobox_function.addItems(['MYSQL', 'SELECT-FROM-WHERE', 'DELETE', 'INSERT', 'UPDATE',
                                        'IN', 'NOT IN', 'EXISTS', 'NOT EXISTS', 'COUNT', 'SUM', 'MAX', 'MIN', 'AVG', 'HAVING'])

        # --------------------查詢button--------------------
        self.button_search = QPushButton('查詢', self)
        self.button_search.setGeometry(50, 350, 900, 60)
        self.button_search.setFont(QFont('Arial', 20))  # button字型、字體大小
        self.button_search.setStyleSheet(
            "background-color: rgbrgb(240,240,230)")    # button背景顏色
        self.button_search.clicked.connect(self.onButtonClick)

        # --------------------查詢結果--------------------
        self.label_result = QLabel('查詢結果', self)
        self.label_result.setGeometry(50, 610, 900, 60)
        self.label_result.setFont(QFont('Arial', 20))  # label字型、字體大小
        self.label_result.setAlignment(Qt.AlignCenter)  # 字體置中
        self.label_result.setFrameShape(QFrame.Box)   # 設定邊框樣式
        self.label_result.setFrameShadow(QFrame.Raised)
        self.label_result.setStyleSheet(
            "background-color: rgb(150,150,130)")    # label背景顏色

        # --------------------Create Output Table--------------------
        self.table = QtWidgets.QTableWidget(self)
        self.table.setGeometry(QtCore.QRect(50, 670, 900, 280))

    # --------------------Button click 施工中--------------------
    def onButtonClick(self):
        function = self.combobox_function.currentText()

        if function == 'SELECT-FROM-WHERE':
            # 找出所有男性員工
            command = "SELECT * FROM Employee WHERE Sex = 'male'"
            self.label_showarea.setText(command)

        elif function == 'DELETE':
            # 將Tom炒魷魚
            command = "DELETE FROM Employee WHERE Name = 'Tom'"
            self.label_showarea.setText(command)

        elif function == 'INSERT':
            # 將新進員工Brandy的資料加入database
            command = "INSERT INTO Employee VALUES (11, 'Brandy', 'male', '1950/6/1')"
            self.label_showarea.setText(command)

        elif function == 'UPDATE':
            # 客人Order_ID為9的訂單，客人要將房間改成306
            command = "UPDATE Orders SET Room_number = 306 WHERE Order_ID = 9"
            self.label_showarea.setText(command)

        elif function == 'IN':
            # 找出所有在2022/10/30、31入住的客人資料
            command = "SELECT * FROM Orders WHERE Date IN ('2022/10/30','2022/10/31')"
            self.label_showarea.setText(command)

        elif function == 'NOT IN':
            # 找出所有不是在2022/10/30、31入住的客人資料
            command = "SELECT * FROM Orders WHERE Date NOT IN ('2022/10/30','2022/10/31')"
            self.label_showarea.setText(command)

        elif function == 'EXISTS':
            # 找出ID=7的員工負責過的所有訂房訂單
            command = "SELECT Orders.* FROM Orders WHERE EXISTS(SELECT * FROM Employee WHERE Employee.ID = Orders.Emp_ID AND Orders.Emp_ID = 7)"
            self.label_showarea.setText(command)

        elif function == 'NOT EXISTS':
            # 找出沒負責過的訂房訂單的員工
            command = "SELECT * FROM Employee WHERE NOT EXISTS(SELECT * FROM Orders WHERE Employee.ID = Orders.Emp_ID)"
            self.label_showarea.setText(command)

        elif function == 'COUNT':
            # 計算價格超過4000的房間總數
            command = "SELECT COUNT(Number) FROM Room WHERE Price > 4000"
            self.label_showarea.setText(command)

        elif function == 'SUM':
            # 求出在2022/10/30的當日房間收入
            command = "SELECT SUM(Price) FROM Orders WHERE Date = '2022/10/30'"
            self.label_showarea.setText(command)

        elif function == 'MAX':
            # 找出最高的訂單消費
            command = "SELECT MAX(Price) FROM Orders"
            self.label_showarea.setText(command)

        elif function == 'MIN':
            # 找出最低的訂單消費
            command = "SELECT MIN(Price) FROM Orders"
            self.label_showarea.setText(command)

        elif function == 'AVG':
            # 找出平均的訂單消費
            command = "SELECT AVG(Price) FROM Orders"
            self.label_showarea.setText(command)

        elif function == 'HAVING':
            # 找出來過2次以上的客人，顯示出他的名子及來的日期
            command = "SELECT CName, COUNT(CName) FROM Orders GROUP BY CName HAVING COUNT(CName) >= 2"
            self.label_showarea.setText(command)

        else:   # MYSQL自行輸入Query
            command = self.label_coding.text()
            self.label_showarea.setText(command)

        try:
            # 執行指令
            cursor.execute(command)

            if (function == 'INSERT'):
                cursor.execute("SELECT * FROM Employee")
            elif (function == 'DELETE'):
                cursor.execute("SELECT * FROM Employee")
            elif (function == 'UPDATE'):
                cursor.execute("SELECT * FROM Orders")

            # --------------------Set Output Table--------------------
            result = cursor.fetchall()

            # 將attribute name放入HorizontalHeader陣列中，再輸出到Output table
            HorizontalHeader = []
            for i in range(len(result[0])):
                HorizontalHeader.insert(i, cursor.description[i][0])

            self.table.setColumnCount(len(result[0]))
            self.table.setRowCount(len(result))
            self.table.setHorizontalHeaderLabels(HorizontalHeader)

            # 將fetch data放入table裡
            for i in range(len(result)):
                for j in range(len(result[i])):
                    item = QTableWidgetItem(str(result[i][j]))
                    item.setTextAlignment(
                        Qt.AlignHCenter | Qt.AlignVCenter)
                    self.table.setItem(i, j, item)

            # connection.commit()  #儲存database變更

        except Exception as EX:
            print('Error')
            QMessageBox.information(None, 'Error', 'Wrong Query')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyWidget()
    w.show()
    sys.exit(app.exec_())
