import sys
import math
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

global i
i = 1

# UI수정(2022.11.27)-issue_#1
# 기능 개선 및 추가(2022.11.29)-issue_#2


class Main(QDialog):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

    ####################################################################################################
    ################# 1.전체 UI 레이아웃 설정(각 위젯을 배치할 레이아웃을 미리 만들어 둠) #################
    ####################################################################################################

        # 모든 작동 버튼들은 QGrid Layout 사용
        # a. 계산 연산자 버튼들 레이아웃
        layout_operation = QGridLayout()  # +,-,x,/ -> %,CE,C,backspace, 1/x , x^2, 루트, 나누기

        # b. number버튼을 배치할 QGridLayout
        layout_number = QGridLayout()

        # c. 입출력 화면은 FormLayout 사용
        layout_equation_solution = QFormLayout()

        # 입출력화면 - 하나의 위젯에서 하기 위한 LineEdit 위젯 생성
        label_equation = QLabel("")
        self.equation = QLineEdit("")
        # 입력과 답 출력 창 크기 및 출력 문자를 윈도우 계산기처럼 오른쪽으로 배치
        self.equation.setFont(QFont('Arial', 30))
        self.equation.setAlignment(Qt.AlignRight)

        # d. 모든 레이아웃들을 정리할 mainlayout은 QVBox레이아웃 사용
        main_layout = QVBoxLayout()

    #######################################################################################################
    ######################## 2. 새로운 기능 버튼 생성(계산에 필요한 연산자들) ###############################
    #######################################################################################################

        # a. layout_opereation에 생성되는 버튼들(위에서 2줄까지 연산자)
        button_remainder = QPushButton("%")
        button_CE = QPushButton("CE")
        button_clear = QPushButton("C")
        button_backspace = QPushButton("Backspace")

        button_reciprocal = QPushButton("1/x")
        button_square = QPushButton("x²")
        button_root = QPushButton("√ ")
        button_division = QPushButton("÷")

        # b. 숫자 버튼(layout_number)쪽에 붙는 연산자들
        button_plus = QPushButton("+")
        button_minus = QPushButton("-")
        button_product = QPushButton("x")
        button_equal = QPushButton("=")

        button_dot = QPushButton(".")
        button_double_zero = QPushButton("00")

    ####################################################################################################
    ######################## 3. 버튼 시그널 설정 issue_#3(신규 연산 추가) ###############################
    ####################################################################################################


        # a. 연산에 필요한 피연산자의 개수가 1개인 연산자들( √ , 1/x , x² )눌렀을때 시그널 : one_button_operation_clicked
        button_root.clicked.connect(
            lambda state, operation="√": self.one_button_operation_clicked(operation))
        button_reciprocal.clicked.connect(
            lambda state, operation="1/x": self.one_button_operation_clicked(operation))
        button_square.clicked.connect(
            lambda state, operation="x²": self.one_button_operation_clicked(operation))

        # b. 연산에 필요한 피연산자의 개수가 2개인 연산자들( % , ÷ , x , - , +)눌렀을때 시그널 : button_operation_clicked
        button_remainder.clicked.connect(
            lambda state, operation="%": self.button_operation_clicked(operation))
        button_plus.clicked.connect(
            lambda state, operation="+": self.button_operation_clicked(operation))
        button_minus.clicked.connect(
            lambda state, operation="-": self.button_operation_clicked(operation))
        button_product.clicked.connect(
            lambda state, operation="x": self.button_operation_clicked(operation))
        button_division.clicked.connect(
            lambda state, operation="÷": self.button_operation_clicked(operation))

        # c. backspace, C, CE 버튼을 눌렀을때 시그널 : button_clear_clicked, button_backspace_clicked
        button_CE.clicked.connect(self.button_clear_clicked)
        button_clear.clicked.connect(self.button_clear_clicked)
        button_backspace.clicked.connect(self.button_backspace_clicked)

        # d. 등호 (" = ") 버튼을 눌렀을때 시그널 : button_equal_clicked
        button_equal.clicked.connect(self.button_equal_clicked)

        # e. 기타 숫자 기호 (" 00 ", " . ") 버튼을 눌렀을때 시그널 : number_button_clicked
        button_dot.clicked.connect(
            lambda state, num=".": self.number_button_clicked(num))
        button_double_zero.clicked.connect(
            lambda state, num="00": self.number_button_clicked(num))

        # f. 숫자 button 생성 및 button 클릭 시 시그널 설정 : number_button_clicked
        number_button_dict = {}
        for number in range(0, 10):
            number_button_dict[number] = QPushButton(str(number))
            number_button_dict[number].setMinimumWidth(95)
            number_button_dict[number].setMinimumHeight(57)
            number_button_dict[number].clicked.connect(lambda state, num=number:
                                                       self.number_button_clicked(num))

    ###################################################################################################
    ############################ 4. 생성된 QPushbotton을 layout에 추가 #################################
    ###################################################################################################

        # a. 수식, 답 위젯을 layout_equation_solution 레이아웃에 추가
        layout_equation_solution.addRow(label_equation, self.equation)

        # b. layout_opereation에 추가된 연산 버튼들을 layout_operation 레이아웃에 추가
        layout_operation.addWidget(button_remainder, 0, 0)
        layout_operation.addWidget(button_CE, 0, 1)
        layout_operation.addWidget(button_clear, 0, 2)
        layout_operation.addWidget(button_backspace, 0, 3)

        layout_operation.addWidget(button_reciprocal, 1, 0)
        layout_operation.addWidget(button_square, 1, 1)
        layout_operation.addWidget(button_root, 1, 2)
        layout_operation.addWidget(button_division, 1, 3)

        # c. 숫자 버튼들을 layout_number 레이아웃에 추가
        layout_number.addWidget(number_button_dict[0], 3, 1)
        layout_number.addWidget(number_button_dict[1], 2, 0)
        layout_number.addWidget(number_button_dict[2], 2, 1)
        layout_number.addWidget(number_button_dict[3], 2, 2)
        layout_number.addWidget(number_button_dict[4], 1, 0)
        layout_number.addWidget(number_button_dict[5], 1, 1)
        layout_number.addWidget(number_button_dict[6], 1, 2)
        layout_number.addWidget(number_button_dict[7], 0, 0)
        layout_number.addWidget(number_button_dict[8], 0, 1)
        layout_number.addWidget(number_button_dict[9], 0, 2)

        # d. 제일 오른쪽 column에 표시되는 사칙연산 및 '=' 버튼을 layout_number 레이아웃에 추가
        layout_number.addWidget(button_equal, 3, 4)
        layout_number.addWidget(button_plus, 2, 4)
        layout_number.addWidget(button_minus, 1, 4)
        layout_number.addWidget(button_product, 0, 4)
        layout_number.addWidget(button_dot, 3, 2)
        layout_number.addWidget(button_double_zero, 3, 0)

        # e. 각 레이아웃들을 main_layout 레이아웃에 추가
        main_layout.addLayout(layout_equation_solution)
        main_layout.addLayout(layout_operation)
        main_layout.addLayout(layout_number)

    ##################################################################################
    ################################# 5. 기타 UI 설정 #################################
    ##################################################################################

        # a. 연산 기능 버튼들의 크기 조정
        button_remainder.setMinimumWidth(95)
        button_remainder.setMinimumHeight(57)
        button_CE.setMinimumWidth(95)
        button_CE.setMinimumHeight(57)
        button_clear.setMinimumWidth(95)
        button_clear.setMinimumHeight(57)
        button_backspace.setMinimumWidth(95)
        button_backspace.setMinimumHeight(57)

        button_reciprocal.setMinimumWidth(95)
        button_reciprocal.setMinimumHeight(57)
        button_square.setMinimumWidth(95)
        button_square.setMinimumHeight(57)
        button_root.setMinimumWidth(95)
        button_root.setMinimumHeight(57)
        button_division.setMinimumWidth(95)
        button_division.setMinimumHeight(57)

        button_plus.setMinimumWidth(95)
        button_minus.setMinimumWidth(95)
        button_product.setMinimumWidth(95)
        button_equal.setMinimumWidth(95)
        button_plus.setMinimumHeight(57)
        button_minus.setMinimumHeight(57)
        button_product.setMinimumHeight(57)
        button_equal.setMinimumHeight(57)

        button_dot.setMinimumWidth(95)
        button_dot.setMinimumHeight(57)
        button_double_zero.setMinimumWidth(95)
        button_double_zero.setMinimumHeight(57)

        # b. 창 title 및 size 설정

        self.setWindowTitle('계산기')
        self.resize(380, 550)

        self.setLayout(main_layout)
        self.show()

    ##################################################################################################
    ########################################  functions  #############################################
    ##################################################################################################

    #  기능 구현 방식
    #  윈도우 계산기에선 연산자를 누를때마다 출력화면이 초기화 되고 " = " 를 누르지 않아도 결과값이 표시됨.
    #  연산자를 누를때 이전의 계산값이 저장되있어야함.

    # 1. 숫자 버튼을 클릭했을때 작동되는 함수
    # i가 홀수, 짝수인지에 따라 현재클릭된 숫자가 자리수에 추가되는 숫자인지, 연산자 다음에 오는 새로운 피연산자인지 구분
    def number_button_clicked(self, num):
        global i
        if i % 2 == 1:
            equation = self.equation.text()
            equation += str(num)
            self.Anumber = float(equation)
            self.equation.setText(equation)
        
        elif i==2:
            self.equation.setText("")
            equation = self.equation.text() 
            equation += str(num)
            self.equation.setText(equation)
            i=i+2

        elif i % 2 == 0:
            equation = self.equation.text()
            equation += str(num)
            self.Bnumber = float(equation)
            self.equation.setText(equation)

        

    # 2. 연산에 필요한 피연산자의 개수가 1개인 연산자들( √ , 1/x , x² ) : one_button_operation_clicked
    def one_button_operation_clicked(self, operation):
        global i
        if operation == "√":
            equation= str(self.equation.text())
            equation1= float(equation)
            self.result = math.sqrt(equation1)
            self.result = round(self.result, 9) #소수점 9자리까지 표기
            equation = str(self.result)
            self.equation.setText(equation)
            i=2

        elif operation == "x²":
            self.result = math.pow(self.Anumber, 2)
            self.result = round(self.result, 9)
            self.Anumber = self.result
            equation = self.equation.text()
            equation = str(self.result)
            self.equation.setText(equation)
            i=2
        elif operation == "1/x":
            self.result = np.reciprocal(float(self.Anumber))
            self.result = round(self.result, 9)
            self.Anumber = self.result
            equation = self.equation.text()
            equation = str(self.result)
            self.equation.setText(equation)
            i=2

    #  3. 연산에 필요한 피연산자의 개수가 2개인 연산자들( % , ÷ , x , - , +) : button_operation_clicked
    def button_operation_clicked(self, operation):
        equation = self.equation.text()
        equation += operation
        self.equation.setText(equation)

    def button_equal_clicked(self):
        equation = self.equation.text()
        solution = eval(equation)
        self.equation.setText(str(solution))

    def button_clear_clicked(self):
        self.Anumber = 0
        self.Bnumber = 0
        global i
        i = 1
        self.equation.setText("")

    def button_backspace_clicked(self):
        equation = self.equation.text()
        equation = equation[:-1]
        self.equation.setText(equation)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())
