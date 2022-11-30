import sys
import math
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# UI수정(2022.11.27)-issue_#1
# 기능 개선 및 추가(2022.11.29)-issue_#2
# gui_calculator_project v1.0 (2022.12.01)

# 숫자를 입력받을때 연산자 전의 숫자인지, 연산자 다음 초기화된 화면에서 새로 등장한 숫자인지 판별하기위한 전역변수
global i 
i = 1
# A ÷ B , A % B, A - B, 와 같이 피연산자의 순서에 따라 값이 달라지는 경우 A연산자와 B 연산자의 위치를 판별하기 위한 전역변수
global op
global A_op
global B_op
op = 0
A_op = 0
B_op = 0
# 전의 연산자를 저장하기 위한 변수
global code
code = ""
global Anum
global Bnum
Anum = None
Bnum = None

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
        self.equation.setFont(QFont('Arial', 40, QFont.Bold))
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
            number_button_dict[number].setFont(QFont('Arial Black',14, QFont.Bold))
            number_button_dict[number].setStyleSheet('background : white')
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

        # a. 연산 기능 버튼들의 크기 및 글씨체 조정
        self.button_style(button_remainder)
        self.button_style(button_CE)
        self.button_style(button_clear)
        button_backspace.setMinimumWidth(95)
        button_backspace.setMinimumHeight(57)
        button_backspace.setFont(QFont('Arial Nova',10, QFont.Bold))

        self.button_style(button_reciprocal)
        self.button_style(button_square)
        self.button_style(button_root)
        self.button_style(button_division)
        
        self.button_style(button_plus)
        self.button_style(button_minus)
        self.button_style(button_product)
        self.button_style(button_equal)

        button_dot.setMinimumWidth(95)
        button_dot.setMinimumHeight(57)
        button_dot.setFont(QFont('Arial Black',14, QFont.Bold))
        button_double_zero.setMinimumWidth(95)
        button_double_zero.setMinimumHeight(57)
        button_double_zero.setFont(QFont('Arial Black',14, QFont.Bold))
        
        # 버튼 색상 설정
        button_equal.setStyleSheet('background : skyblue')
        button_dot.setStyleSheet('background : white')
        button_double_zero.setStyleSheet('background : white')
        
        # c. 창 title 및 size 설정

        self.setWindowTitle('계산기')
        self.resize(360, 530)

        self.setLayout(main_layout)
        self.show()

    ##################################################################################################
    ########################################  functions  #############################################
    ##################################################################################################
        
    #  기능 구현 방식
    #  윈도우 계산기에선 연산자를 누를때마다 출력화면이 초기화 되고 " = " 를 누르지 않아도 연산자를 눌렀을때
    #                                          (피연산자가 2개필요한 함수들은 두번째 연산자 입력부터) 결과값이 표시됨.
    #  연산자를 연속해서 누를때 이전 연산에 대한 계산값을 출력해야함.

    # 1. 숫자 버튼을 클릭했을때 작동되는 함수
    #   - i가 1인지 2인지 짝수인지에 따라 현재클릭된 숫자가 현재 추가되는 숫자인지, 연산자 다음에 오는 새로운 피연산자인지 구분
    
    def number_button_clicked(self, num):
        global i
        if i == 1:
            equation = self.equation.text()
            equation += str(num)
            self.Anumber = float(equation)
            self.equation.setText(equation)
        
        elif i == 2: #연산자 다음 화면은 초기화 되어야 하기때문에
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
        global i,code,Anum,Bnum,op
        if operation == "√":                            #함수식 설명
            equation= str(self.equation.text()) # 현재 출력창의 텍스트(숫자) 받아들임
            equation_1= float(equation)         # 연산에 필요한 임시 변수
            self.result = math.sqrt(equation_1) # 루트 연산 실행해서 result에 저장
            self.result = round(self.result, 9) # 소수점 9자리까지 표기
            equation = str(self.result)         # equation변수에 result값 str형식으로 저장
            self.equation.setText(equation)     # equation값 setText 출력
            i=2                                 # 연산자 다음에 오는 숫자는 출력 초기화 된후 입력되도록
            op=op+1                             # 피연산자들 순서를 구분하기 위한 함수
            code = ""
            Anum =None 
            Bnum =None

        elif operation == "x²":
            equation=str(self.equation.text())
            equation_1=float(equation)
            self.result = math.pow((equation_1), 2)
            self.result = round(self.result, 9)
            equation = str(self.result)
            self.equation.setText(equation)
            i=2
            op=op+1
            code =""
            Anum =None 
            Bnum =None

        elif operation == "1/x":
            equation= str(self.equation.text())
            equation_1=float(equation)
            self.result = np.reciprocal(equation_1)
            self.result = round(self.result, 9)
            equation = str(self.result)
            self.equation.setText(equation)
            i=2
            op=op+1
            code = ""
            Anum =None 
            Bnum =None

# 과거 연산자에 대한 계산
    def past_operation(self, code):
        global Anum, Bnum
        if code=="%":
            
            result1 = Anum % Bnum
            result1 = round(result1, 9)
            Anum=result1
            self.equation.setText(str(result1))
        elif code=="÷":
            result1 = Anum / Bnum
            result1 = round(result1, 9)
            Anum=result1
            self.equation.setText(str(result1))
        elif code=="x":
            result1 = Anum* Bnum
            result1 = round(result1, 9)
            Anum=result1
            self.equation.setText(str(result1))
        elif code=="-":
            result1 = Anum - Bnum
            result1 = round(result1, 9)
            Anum=result1
            self.equation.setText(str(result1))
        elif code=="+":
            result1 = Anum + Bnum
            result1 = round(result1, 9)
            Anum=result1
            self.equation.setText(str(result1))


    #  3. 연산에 필요한 피연산자의 개수가 2개인 연산자들( % , ÷ , x , - , +) : button_operation_clicked
    def button_operation_clicked(self, operation):
        global i,op,A_op, B_op,code,Anum,Bnum
        # 나머지 (%) 버튼 입력시
        if operation == "%":
            op=op+1
            if i == 1 :
                A_op = op-1                             #첫번째 숫자니까 연산 바로 필요 없음
                equation= str(self.equation.text())     #현재 창에 있는 숫자 Anum으로 입력
                Anum = float(equation)
                code = "%"
                self.equation.setText("")

            elif i>=2 and Anum != None:                 #두번째 피연산까지 입력되었을때 (이땐 이전 연산 결과값 출력이 필요함)
                if op > A_op :                          #현재 피연산자가 2번째 피연산자 B인지 확인
                    B_op = op
                    equation= str(self.equation.text()) #두번째 피연산자를 Bnum에 추출
                    Bnum = float(equation)                                   
                    self.past_operation(code)            #operation function 실행 (과거의 연산자에 대한 실행)
                    A_op = B_op
                    code = "%"

            elif i>=2 and Anum == None :                #피연산자가 1개 필요한 연산(√ , 1/x , x²)이 이전에 실행됐었을때
                A_op = op - 1
                equation = str(self.equation.text())
                Anum=float(equation)
                code = "%"
            i=2

        # 나눗셈 (÷) 버튼 입력시
        elif operation == "÷":
            op=op+1
            if i == 1 :
                A_op = op-1                             #첫번째 숫자니까 연산 바로 필요 없음
                equation= str(self.equation.text())     #현재 창에 있는 숫자 Anum으로 입력
                Anum = float(equation)
                code = "÷"
                self.equation.setText("")

            elif i>=2 and Anum != None:                 #두번째 피연산까지 입력되었을때 (이땐 이전 연산 결과값 출력이 필요함)
                if op > A_op :                          #현재 피연산자가 2번째 피연산자 B인지 확인
                    B_op = op
                    equation= str(self.equation.text()) #두번째 피연산자를 Bnum에 추출
                    Bnum = float(equation)                                   
                    self.past_operation(code)            #operation function 실행 (과거의 연산자에 대한 실행)
                    A_op = B_op
                    code = "÷"

            elif i>=2 and Anum == None :                #피연산자가 1개 필요한 연산(√ , 1/x , x²)이 이전에 실행됐었을때
                A_op = op - 1
                equation = str(self.equation.text())
                Anum=float(equation)
                code = "÷"
            i=2

        # 곱셈 (x) 버튼 입력시
        elif operation == "x":
            op=op+1
            if i == 1 :
                A_op = op-1                             #첫번째 숫자니까 연산 바로 필요 없음
                equation= str(self.equation.text())     #현재 창에 있는 숫자 Anum으로 입력
                Anum = float(equation)
                code = "x"
                self.equation.setText("")

            elif i>=2 and Anum != None:                 #두번째 피연산까지 입력되었을때 (이땐 이전 연산 결과값 출력이 필요함)
                if op > A_op :                          #현재 피연산자가 2번째 피연산자 B인지 확인
                    B_op = op
                    equation= str(self.equation.text()) #두번째 피연산자를 Bnum에 추출
                    Bnum = float(equation)                                   
                    self.past_operation(code)            #operation function 실행 (과거의 연산자에 대한 실행)
                    A_op = B_op
                    code = "x"

            elif i>=2 and Anum == None :                #피연산자가 1개 필요한 연산(√ , 1/x , x²)이 이전에 실행됐었을때
                A_op = op - 1
                equation = str(self.equation.text())
                Anum=float(equation)
                code = "x"
            i=2

        # 빼기 (-) 버튼 입력시
        if operation == "-":
            op=op+1
            if i == 1 :
                A_op = op-1                             #첫번째 숫자니까 연산 바로 필요 없음
                equation= str(self.equation.text())     #현재 창에 있는 숫자 Anum으로 입력
                Anum = float(equation)
                code = "-"
                self.equation.setText("")

            elif i>=2 and Anum != None:                 #두번째 피연산까지 입력되었을때 (이땐 이전 연산 결과값 출력이 필요함)
                if op > A_op :                          #현재 피연산자가 2번째 피연산자 B인지 확인
                    B_op = op
                    equation= str(self.equation.text()) #두번째 피연산자를 Bnum에 추출
                    Bnum = float(equation)                                   
                    self.past_operation(code)            #operation function 실행 (과거의 연산자에 대한 실행)
                    A_op = B_op
                    code = "-"

            elif i>=2 and Anum == None :                #피연산자가 1개 필요한 연산(√ , 1/x , x²)이 이전에 실행됐었을때
                A_op = op - 1
                equation = str(self.equation.text())
                Anum=float(equation)
                code = "-"
            i=2
        # 더하기 (+) 버튼 입력시
        if operation == "+":
            op=op+1
            if i == 1 :
                A_op = op-1                             #첫번째 숫자니까 연산 바로 필요 없음
                equation= str(self.equation.text())     #현재 창에 있는 숫자 Anum으로 입력
                Anum = float(equation)
                code = "+"
                self.equation.setText("")

            elif i>=2 and Anum != None:                 #두번째 피연산까지 입력되었을때 (이땐 이전 연산 결과값 출력이 필요함)
                if op > A_op :                          #현재 피연산자가 2번째 피연산자 B인지 확인
                    B_op = op
                    equation= str(self.equation.text()) #두번째 피연산자를 Bnum에 추출
                    Bnum = float(equation)                                   
                    self.past_operation(code)            #operation function 실행 (과거의 연산자에 대한 실행)
                    A_op = B_op
                    code = "+"

            elif i>=2 and Anum == None :                #피연산자가 1개 필요한 연산(√ , 1/x , x²)이 이전에 실행됐었을때
                A_op = op - 1
                equation = str(self.equation.text())
                Anum=float(equation)
                code = "+"
            i=2   

    # 등호 " = " 버튼 입력시
    def button_equal_clicked(self):
        global A_op,B_op,Anum,Bnum,code,i

        B_op = op
        equation= str(self.equation.text())
        Bnum = float(equation)
        self.past_operation(code)
        A_op = B_op
        code = ""
        i=2
    # CE, C 버튼 입력시
    def button_clear_clicked(self):
        global Anum,Bnum,i
        Anum = None
        Bnum = None
        i = 1
        self.equation.setText("")
    # backspace 버튼 입력시
    def button_backspace_clicked(self):
        equation = self.equation.text()
        equation = equation[:-1]
        self.equation.setText(equation)

    #버튼 ui함수
    def button_style(self,button_name):
        button_name.setMinimumWidth(95)
        button_name.setMinimumHeight(57)
        button_name.setFont(QFont('Arial Nova',14, QFont.Bold))
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())
