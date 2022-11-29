import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

#UI수정(2022.11.27)-issue_#7
class Main(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

    ########################################################################  
    ### 1.전체 UI 레이아웃 설정(각 위젯을 배치할 레이아웃을 미리 만들어 둠) ###
    ########################################################################  
        #모든 작동 버튼들은 QGrid Layout 사용

        # a. 계산 연산자 버튼들 레이아웃
        layout_operation = QGridLayout() # +,-,x,/ -> %,CE,C,backspace, 1/x , x^2, 루트, 나누기
        
        # b. number버튼을 배치할 QGridLayout
        layout_number = QGridLayout()
       
        # c. 입출력 화면은 FormLayout 사용
        layout_equation_solution = QFormLayout()

        # 입출력화면 - 하나의 위젯에서 하기 위한 LineEdit 위젯 생성
        label_equation = QLabel("")
        self.equation = QLineEdit("")
        #입력과 답 출력 창 크기 및 출력 문자를 윈도우 계산기처럼 오른쪽으로 배치
        self.equation.setFont(QFont('Arial',30))
        self.equation.setAlignment(Qt.AlignRight)

        # d. 모든 레이아웃들을 정리할 mainlayout은 QVBox레이아웃 사용
        main_layout = QVBoxLayout()
        
    #####################################################    
    ### 2. 새로운 기능 버튼 생성(계산에 필요한 연산자들) ###
    #####################################################

        # a. layout_opereation에 생성되는 버튼들(위에서 2줄까지 연산자)
        button_remainder = QPushButton("%")
        button_CE = QPushButton("CE")
        button_clear = QPushButton("C")
        button_backspace = QPushButton("Backspace")
        
        button_reciprocal = QPushButton("1/x")
        button_square = QPushButton("x²")
        button_root = QPushButton("√ ")
        button_division = QPushButton("÷")

        # b. layout_number쪽에 붙는 연산자 버튼들
        button_plus = QPushButton("+")
        button_minus = QPushButton("-")
        button_product = QPushButton("x")
        button_equal = QPushButton("=")

        button_dot = QPushButton(".")
        button_double_zero = QPushButton("00")

    ################################################### 
    ### 3. 버튼 시그널 설정 # issue_3(신규 연산 추가) ###
    ################################################### 

        # a. 사칙연산 버튼을 클릭했을 때, 각 사칙연산 부호가 수식창에 추가될 수 있도록 시그널 설정
        button_plus.clicked.connect(lambda state, operation = "+": self.button_operation_clicked(operation))
        button_minus.clicked.connect(lambda state, operation = "-": self.button_operation_clicked(operation))
        button_product.clicked.connect(lambda state, operation = "*": self.button_operation_clicked(operation))
        button_division.clicked.connect(lambda state, operation = "/": self.button_operation_clicked(operation))
        ##############################여기 다 고쳐야함
        #clear_equal
        # b. =, clear, backspace 버튼 클릭 시 시그널 설정
        button_equal.clicked.connect(self.button_equal_clicked)
        button_CE.clicked.connect(self.button_clear_clicked)
        button_clear.clicked.connect(self.button_clear_clicked)
        button_backspace.clicked.connect(self.button_backspace_clicked)

        button_dot.clicked.connect(lambda state, num = ".": self.number_button_clicked(num))
        button_double_zero.clicked.connect(lambda state, num = "00": self.number_button_clicked(num))

        # c. 숫자 버튼 생성 및 버튼 클릭 시 시그널 설정
        number_button_dict = {}
        for number in range(0, 10):
            number_button_dict[number] = QPushButton(str(number))
            number_button_dict[number].setMinimumWidth(95)
            number_button_dict[number].setMinimumHeight(57)
            number_button_dict[number].clicked.connect(lambda state, num = number:
                                                       self.number_button_clicked(num))

    ############################################ 
    ### 4. 생성된 QPushbotton을 layout에 추가 ###
    ############################################  
    
        # a. 수식, 답 위젯을 layout_equation_solution 레이아웃에 추가
        layout_equation_solution.addRow(label_equation, self.equation)
        
        # b. layout_opereation에 추가된 연산 버튼들을 layout_operation 레이아웃에 추가
        layout_operation.addWidget(button_remainder,0,0)
        layout_operation.addWidget(button_CE,0,1)
        layout_operation.addWidget(button_clear,0,2)
        layout_operation.addWidget(button_backspace,0,3)

        layout_operation.addWidget(button_reciprocal,1,0)
        layout_operation.addWidget(button_square,1,1)
        layout_operation.addWidget(button_root,1,2)
        layout_operation.addWidget(button_division,1,3)

        # c. 숫자 버튼들을 layout_number 레이아웃에 추가
        layout_number.addWidget(number_button_dict[0],3,1)                                           
        layout_number.addWidget(number_button_dict[1],2,0) 
        layout_number.addWidget(number_button_dict[2],2,1) 
        layout_number.addWidget(number_button_dict[3],2,2) 
        layout_number.addWidget(number_button_dict[4],1,0) 
        layout_number.addWidget(number_button_dict[5],1,1) 
        layout_number.addWidget(number_button_dict[6],1,2) 
        layout_number.addWidget(number_button_dict[7],0,0) 
        layout_number.addWidget(number_button_dict[8],0,1) 
        layout_number.addWidget(number_button_dict[9],0,2)

        # 제일 오른쪽 column에 표시되는 사칙연산 및 '=' 버튼을 layout_number 레이아웃에 추가
        layout_number.addWidget(button_equal,3,4)
        layout_number.addWidget(button_plus,2,4)
        layout_number.addWidget(button_minus,1,4)
        layout_number.addWidget(button_product,0,4)
        layout_number.addWidget(button_dot, 3, 2)
        layout_number.addWidget(button_double_zero, 3, 0)
    
    
        ### 각 레이아웃들을 main_layout 레이아웃에 추가
        main_layout.addLayout(layout_equation_solution)
        main_layout.addLayout(layout_operation)
        main_layout.addLayout(layout_number)

    ######################   
    ### 5. 기타 UI 설정 ###
    ######################  

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

        # b. 창 title 및 size
        
        self.setWindowTitle('계산기')
        self.resize(380,550)

        self.setLayout(main_layout)
        self.show()

    #################
    ### functions ###
    #################
    def number_button_clicked(self, num): #버튼을 클릭했을때
        equation = self.equation.text() 
        equation += str(num)
        self.equation.setText(equation) #settext 텍스트 쓰는것

    def button_operation_clicked(self, operation):
        equation = self.equation.text()
        equation += operation
        self.equation.setText(equation)

    def button_equal_clicked(self):
        equation = self.equation.text()
        solution = eval(equation)
        self.equation.setText(str(solution)) #21:45수정 #7

    def button_clear_clicked(self):
        self.equation.setText("")
        #self.solution.setText("") #21:45수정 #7

    def button_backspace_clicked(self):
        equation = self.equation.text()
        equation = equation[:-1]
        self.equation.setText(equation)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())