import pymysql
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from matplotlib import font_manager, rc
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

form_class = uic.loadUiType("snack_bar.ui")[0]

class smart_app(QWidget, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.stackedWidget.setCurrentIndex(0)

        self.signup_cancle_button.clicked.connect(self.gohome)
        self.signup_main_button.clicked.connect(self.signup_screen)
        self.signup_confirm_button.clicked.connect(self.signup)
        self.overlap_button.clicked.connect(self.double_check)

    def gohome(self):
        self.id_check.clear()
        self.name_check.clear()
        self.pw_check.clear()
        self.pw2_check.clear()
        self.add_check.clear()
        self.phon_check.clear()
        self.stackedWidget.setCurrentIndex(0)

    def signup_screen(self):
        self.login_okay = False
        self.stackedWidget.setCurrentIndex(1)

    def signup(self):
        if self.id_check.text() == '' or self.name_check.text() == '' or self.pw_check.text() == '' or self.pw2_check.text() == '' or self.add_check.text() == '' or self.phon_check.text() == '':
            QMessageBox.critical(self, "에러", "빈칸을 전부 입력해주세요")
        elif self.pw_check.text() != self.pw2_check.text():
            QMessageBox.critical(self, "에러", "비밀번호와 비밀번호확인이 일치하지 않습니다.")
        elif bool(self.login_okay) == False:
            QMessageBox.critical(self, "에러", "중복확인을 해주세요")
        elif bool(self.radioButton.isChecked()) == False and bool(self.radioButton_2.isChecked()) == False:
            QMessageBox.critical(self, "에러", "사업자 또는 개인 선택해주세요")
        else:
            information = 're'
            if self.radioButton.isChecked():
                information = self.radioButton.text()
            elif self.radioButton.isChecked():
                information = self.radioButton_2.text()
            conn = pymysql.connect(host='localhost', user='root', password='qwer1234', db='test165', charset='utf8')
            cur = conn.cursor()
            cur.execute(f'INSERT INTO user (아이디, 비밀번호, 이름, 주소, 전화번호, `사업자 여부`) VALUES ("{self.id_check.text()}", "{self.pw_check.text()}", "{self.name_check.text()}", "{self.add_check.text()}", "{self.phon_check.text()}", "{information}")')
            conn.commit()
            conn.close()
            QMessageBox.information(self, "확인", "회원가입에 성공하셨습니다")
            self.id_check.clear()
            self.name_check.clear()
            self.pw_check.clear()
            self.pw2_check.clear()
            self.add_check.clear()
            self.phon_check.clear()
            self.stackedWidget.setCurrentIndex(0)

    def double_check(self):
        conn = pymysql.connect(host='localhost', user='root', password='qwer1234', db='test165', charset='utf8')
        cur = conn.cursor()
        cur.execute(f'SELECT 아이디 FROM user WHERE 아이디 = "{self.id_check.text()}"')
        checking = cur.fetchall()
        conn.close()
        print(checking)
        if self.id_check.text() == '':
            QMessageBox.critical(self, "에러", "아이디를 입력해주세요")
        elif checking != ():
            QMessageBox.critical(self, "에러", "중복된 아이디 입니다")
        else:
            QMessageBox.information(self, "확인", "사용가능한 아이디입니다")
            self.login_okay = True
            self.id_check.textChanged.connect(self.signup_screen)

    def login_up(self):



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = smart_app()
    window.show()
    app.exec_()