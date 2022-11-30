# gui_calculator 개요

파이썬을 이용하여 윈도우 표준 계산기와 비슷한 계산기를 실행해보는 프로그램입니다.

이 프로그램은 해당 블로그의 코드를 기반으로 추가 기능과 UI를 구현하였습니다.
``` 
https://studyingrabbit.tistory.com/23
``` 

위에서 참고한 계산기코드에서 추가로 구현할 목표는 다음과 같습니다.

 - UI 수정 및 개선
* PyQt 기반의 UI를 사용하되, 버튼은 QGridLayout으로만 구성
* 참고한 코드의 Equation, Solution값에 대해 2개의 창에서 출력되는것을 윈도우 계산기처럼 하나의 창에 표현 
* 참고한 코드에 없는 항목( √ , 1/x , x², %)에 대해 버튼 추가
* 각 연산 버튼 및 숫자 버튼의 배치 조정

 - 기능에 관한 수정 및 개선
* 참고한 코드에 eval함수를 쓰지않고 기본 함수 및 라이브러리(수식,math,numpy 등)를 사용하여 계산 기능 구현
* 참고한 코드에 없는 항목( √ , 1/x , x², %)에 대한 계산 기능 추가
* CE, C 버튼을 눌렀을 경우 지금까지의 연산내용과 출력값을 전부 초기화

## 코드에 관하여

구현해야할 기능에 대하여 다음과 같은 로직으로 코드를 구현하였습니다.

먼저, 윈도우 계산기에서는 연산자로 ( √ , 1/x , x² )가 입력되었을 경우에는 바로전 입력된 피연산자에 대하여 즉시 해당결과를 출력하고, ( % , ÷ , x , - , +)가 입력되었을 경우에는 다음 피연산자가 입력되고난 후 다음 연산자 혹은 등호를 누를 때 그 계산 결과 값이 출력됩니다. 그리고 CE, C 버튼을 눌렀을 경우 지금까지의 연산내용과 출력값을 전부 초기화 시킵니다.

따라서 기능 로직을 크게 두가지로 나누고 각각 세부적으로 함수를 구성했습니다.

* 숫자 버튼을 눌렀을 경우
* 연산자 버튼을 눌렀을 경우

1. 숫자버튼을 눌렀을 경우
    예를들어 A ÷ B 를 계산하는경우, 피연산자의 A, B의 순서에 따라 해당 연산의 결과값이 달라지므로
    숫자가 입력되었을 경우에는 이 숫자가 연산자 전의 피연산자(A)의 숫자인지, 연산자 뒤의 새로운 피연산자(B)인지 구분이 필요합니다.
    따라서 op라는 전역변수를 사용하여 연산자가 시행될때마다 op+=1을 하고 op의 크기를 비교하여 입력되는 숫자의 위치를 구분하였습니다.

2. 연산자 버튼을 눌렀을 경우

    연산자 버튼을 두가지 경우로 나누어 함수를 구현하였습니다.
    
    * 연산에 필요한 피연산자의 개수가 1개인 연산자들( √ , 1/x , x² )
    * 연산에 필요한 피연산자의 개수가 2개인 연산자들( % , ÷ , x , - , +)

    그리고 "3" , "+" , "3" 을 차례대로 눌렀을때, 그다음으로 등호 " = "가 아닌 "+" 같은 연산자를 눌렀을경우에도 이전의 계산값이 출력되어야하므로,
    연산자가 두번이상 사용될때부터( √ , 1/x , x² 를 제외한 경우)는 연산자를 누를때마다 이전의 연산값을 출력하도록 기능을 구현 하였습니다.

    예를들어 "3" -> " + " -> " 3 " 을 순서대로 눌렀을때, 다음으로 " -  " 버튼을 누르면 출력화면엔 " 6 " 이 나오고, 그다음 " 6 " 을 누른뒤 등호 " = "을 누르면 " 0 " 이 출력됩니다.

### Prerequisites

프로그램을 실행하기 위해서 pyqt5파이썬 패키지 모듈설치가 필요합니다.

cmd, Anaconda나 Vscode등을 이용해서 해당 패키지 모듈을 설치합니다. 

* pip를 통한 pyqt5설치
``` 
pip install pyqt5
```

## Running the tests

파이썬 실행이 가능한 환경에서 calculator_main.py 파이썬 파일을 실행합니다.


## Built With

참고한 계산기 예시 코드의 출처는 다음과 같습니다
* https://studyingrabbit.tistory.com/23

## Contributing

Please read [CONTRIBUTING.md] for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

gui_calculator_project v1.2 (updated 2022.12.01)

## Authors

kukdong2(https://github.com/kukdong2)

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
