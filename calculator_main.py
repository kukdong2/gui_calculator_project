import sys
from PyQt5.QtWidgets import *

#UI수정(2022.11.27)-issue_#7
class Main(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        ### 각 위젯을 배치할 레이아웃을 미리 만들어 둠
        layout_operation = QGridLayout() # +,-,x,/ -> %,CE,C,backspace, 1/x , x^2, 루트, 나누기
        #layout_clear_equal = QGridLayout() # clear,backspace,= number에 다넣어
        layout_number = QGridLayout()
        layout_equation_solution = QFormLayout()

        ### 수식 입력과 답 출력을 위한 LineEdit 위젯 생성
        label_equation = QLabel("")
        #issue_#7수정 label_solution = QLabel("Number: ")
        self.equation = QLineEdit("")
        #issue_#7수정 self.solution = QLineEdit("")

        ### layout_equation_solution 레이아웃에 수식, 답 위젯을 추가
        layout_equation_solution.addRow(label_equation, self.equation)
        #layout_equation_solution.addRow(label_equation, self.solution)
        #issue_#7수정 layout_equation_solution.addRow(label_solution, self.solution)

        ### 사칙연산 버튼 생성
            ## layout_opereation에 생성되는 버튼들
        button_remainder = QPushButton("%")
        button_CE = QPushButton("CE")
        button_clear = QPushButton("C")
        button_backspace = QPushButton("Backspace")

        button_reciprocal = QPushButton("1/x")
        button_square = QPushButton("x²")
        button_root = QPushButton("√ ")
        button_division = QPushButton("÷")

            ## layout_number에 붙는애들
        button_plus = QPushButton("+")
        button_minus = QPushButton("-")
        button_product = QPushButton("x")
        button_equal = QPushButton("=")
        

        ### 사칙연산 버튼을 클릭했을 때, 각 사칙연산 부호가 수식창에 추가될 수 있도록 시그널 설정
        button_plus.clicked.connect(lambda state, operation = "+": self.button_operation_clicked(operation))
        button_minus.clicked.connect(lambda state, operation = "-": self.button_operation_clicked(operation))
        button_product.clicked.connect(lambda state, operation = "*": self.button_operation_clicked(operation))
        button_division.clicked.connect(lambda state, operation = "/": self.button_operation_clicked(operation))

        ### layout_opereation에 추가된 연산 버튼을 layout_operation 레이아웃에 추가
        layout_operation.addWidget(button_remainder,0,0)
        layout_operation.addWidget(button_CE,0,1)
        layout_operation.addWidget(button_clear,0,2)
        layout_operation.addWidget(button_backspace,0,3)

        layout_operation.addWidget(button_reciprocal,1,0)
        layout_operation.addWidget(button_square,1,1)
        layout_operation.addWidget(button_root,1,2)
        layout_operation.addWidget(button_division,1,3)

        #clear_equal
        ### =, clear, backspace 버튼 클릭 시 시그널 설정
        button_equal.clicked.connect(self.button_equal_clicked)
        button_CE.clicked.connect(self.button_clear_clicked)
        button_clear.clicked.connect(self.button_clear_clicked)
        button_backspace.clicked.connect(self.button_backspace_clicked)
        

        ### 숫자 버튼 생성하고, layout_number 레이아웃에 추가
        ### 각 숫자 버튼을 클릭했을 때, 숫자가 수식창에 입력 될 수 있도록 시그널 설정
        number_button_dict = {}
        for number in range(0, 10):
            number_button_dict[number] = QPushButton(str(number))
            number_button_dict[number].clicked.connect(lambda state, num = number:
                                                       self.number_button_clicked(num))

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
        ##옆에 사칙연산 및 =표시
        layout_number.addWidget(button_equal,3,4)
        layout_number.addWidget(button_plus,2,4)
        layout_number.addWidget(button_minus,1,4)
        layout_number.addWidget(button_product,0,4)

        ### 소숫점 버튼과 00 버튼을 입력하고 시그널 설정
        button_dot = QPushButton(".")
        button_dot.clicked.connect(lambda state, num = ".": self.number_button_clicked(num))
        layout_number.addWidget(button_dot, 3, 2)

        button_double_zero = QPushButton("00")
        button_double_zero.clicked.connect(lambda state, num = "00": self.number_button_clicked(num))
        layout_number.addWidget(button_double_zero, 3, 0)

        ### 각 레이아웃을 main_layout 레이아웃에 추가
        main_layout.addLayout(layout_equation_solution)
        main_layout.addLayout(layout_operation)
        main_layout.addLayout(layout_number)

        self.setLayout(main_layout)
        self.show()

    #################
    ### functions ###
    #################
    def number_button_clicked(self, num): #버튼을 클릭했을때
        equation = self.equation.text() #
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
