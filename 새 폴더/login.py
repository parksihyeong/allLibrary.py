import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
import csv

form_class = uic.loadUiType("signup.ui")[0]


class Login(QWidget, form_class):
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        self.stackedWidget.setCurrentIndex(0)   # 위젯의 인덱스 1번 페이지가 먼저 나오게 함

        # ----- 로그인 창 -----
        # 통합도서관 버튼 메인페이지 이동
        self.btn_all_library.setStyleSheet("background-image:url(allLibrary.png)")
        self.btn_all_library.clicked.connect(self.MoveallLibrary)

        # 로그인 하기 버튼
        # self.btn_login.clicked.connect(self.login_stack)
        # self.pw_input.returnPressed.connect(self.login_stack)

        # 회원가입 버튼
        self.btn_joinPage.clicked.connect(self.join_stack)

        # ----- 회원가입 창 -----
        # 뒤로가기 버튼
        self.btn_prevPage.clicked.connect(self.prevPage_stack)      # 수정전 메소드가 login_stack이었음

        # 회원가입 완료 버튼
        self.member_join.clicked.connect(self.pre_stack)
        self.phone.returnPressed.connect(self.pre_stack)

        # 비밀번호 설정
        self.pw_input.setEchoMode(QLineEdit.Password)
        self.pw.setEchoMode(QLineEdit.Password)
        self.pw.setMaxLength(16)
        self.real_pw.setEchoMode(QLineEdit.Password)
        self.duplication.clicked.connect(self.check_stack)
        self.sign_up = False
        self.login = []
        # 전화번호 숫자만 입력 설정
        self.onlyInt = QIntValidator()
        self.phone.setValidator(self.onlyInt)
        # self.gomain.clicked.connect(self.maingo_stack)

        # ----- 메인(임시) 창 -----
        # 로그아웃 버튼
        # self.btn_logout.clicked.connect(self.live_stack)

    # def maingo_stack(self):
    #     widget.setCurrentIndex(0)

    # 통합도서관 버튼 메인페이지 이동 메소드(추가했습니다_연수)
    def MoveallLibrary(self):
        self.id_input.clear()
        self.pw_input.clear()
        self.parent().setCurrentIndex(0)

    # 회원가입 페이지 이동 메소드
    def join_stack(self):
        self.id_input.clear()
        self.pw_input.clear()
        self.stackedWidget.setCurrentIndex(1)

    # 로그인 페이지 이동 메소드(추가했습니다_연수)
    def prevPage_stack(self):
        self.id.clear()
        self.pw.clear()
        self.name.clear()
        self.real_pw.clear()
        self.address.clear()
        self.phone.clear()
        self.stackedWidget.setCurrentIndex(0)

    def next_stack(self):
        self.sign_up = False
        self.stackedWidget.setCurrentIndex(1)

    def pre_stack(self):
        if self.id.text() == '' or self.pw.text() == '' or self.real_pw.text() == '' or self.phone.text() == '' or self.address.text() == '' or self.name.text() == '':
            QMessageBox.information(self, '가입 에러', '빈 칸을 전부 입력해주세요')
        elif self.pw.text() != self.real_pw.text():
            QMessageBox.information(self, '가입 에러', '비밀번호와 비밀번호 확인이 다릅니다')
        elif len(self.pw.text()) < 8:
            QMessageBox.information(self, '가입 에러', '비밀번호가 너무 짧습니다')
        elif len(self.id.text()) < 6:
            QMessageBox.information(self, '가입 에러', '아이디가 너무 짧습니다')
        elif self.sign_up == False:
            QMessageBox.information(self, '가입 에러', '아이디 중복 확인을 해주세요')
        elif self.sign_up == True:
            f = open("login.csv", 'a', newline='', encoding="UTF-8")
            self.data = [self.id.text(), self.pw.text()]
            self.profile = [self.name.text(), self.phone.text(), self.address.text()]
            wr = csv.writer(f)
            wr.writerow(self.data)
            wr.writerow(self.profile)
            f.close()
            self.id.clear()
            self.pw.clear()
            self.name.clear()
            self.real_pw.clear()
            self.address.clear()
            self.phone.clear()
            f = open('login.csv', 'r', newline='', encoding="UTF-8")
            line = csv.reader(f)
            for row in line:
                print(row)
            QMessageBox.information(self, '가입확인창', '가입되었습니다')
            self.stackedWidget.setCurrentIndex(1)

    def login_stack(self):
        login_id_pw = []
        f = open('login.csv', 'r', newline='', encoding="UTF-8")
        line = csv.reader(f)
        for row in line:
            print(row)
            login_id_pw.append(row)
        f.close()
        login_success = [self.id_input.text(), self.pw_input.text()]
        print(login_id_pw)
        if login_success in login_id_pw and self.id_input.text() != '':
            self.logine = login_success + login_id_pw[login_id_pw.index(login_success)+1]  # 로그인하면 리스트에 회원정보 저장
            f = open("profile.csv", 'w', newline='', encoding="UTF-8")
            wr = csv.writer(f)
            wr.writerow(self.logine)
            f.close()
            print(self.logine)
            self.id_input.clear()
            self.pw_input.clear()
            self.parent().setCurrentIndex(0)
        else:
            self.pw_input.clear()
            QMessageBox.information(self, '로그인 오류', '아이디나 비밀번호가 틀립니다')

    # def live_stack(self):
    #     self.login = []
    #     if bool(self.login) == False:
    #         print(self.login)
    #     self.stackedWidget.setCurrentIndex(1)

    def check_stack(self):
        f = open("login.csv", "r", newline='', encoding="UTF-8")
        line = csv.reader(f)
        id_check = []
        for row in line:
            id_check.append(row[0])
        if self.duplication.clicked:
            if self.id.text() in id_check:
                QMessageBox.information(self, '아이디 중복', '이미 있는 아이디 입니다')
                self.sign_up = False
            else:
                QMessageBox.information(self, '아이디', '사용가능한 아이디입니다')
                self.sign_up = True
                self.id.textChanged.connect(self.next_stack)


if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = Login()
    myWindow.show()
    app.exec_()