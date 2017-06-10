# project-item2-python- Junseok Oh, Jingyu Ham, Juyoung Park
6/6(Tue)
(commit log - "Designed Prototype of Define Operator")
- define에 대한 기본적인 구현. 테이블에 define을 추가해서 define을 정의함
- define에서 정의한 ID는 독자적인 테이블을 가지며, 계산될 때 저장되어 있는 값으로 계산이 됨.

6/8(Thu)

(commit log - "Improve define command and revise plus,minus,multiple,divide")
- commit로그를 보면 define함수에서 테이블에 넣을 때, 테이블의 키에대한 value값으로 표현식이 들어가도 상관없게 하기위해 runexpr()함수를 이용해서 값을 계산하고 table에 추가함.
- plus, minus, divide, multiple에서 ID가 들어오면 ID가 table에 있는지 확인하고, define 되어있으면, table에서 define된 값을 가져와서 계산하기 위한 부분을 추가함.

(commit log - "revise run-func")
- plus, minus, divide, multiple을 제외한 것을 모두 구현.
- plus, minus, divide, multiple과 똑같이 ID에 대해서 확인하고 table에서 값을 가져오면 됨.

(commit log - "addtional revision of run-func() method")
- 이 과정은 간단하지만 해결하는데 까다로웠다.
- 만약에 eq?를 구현하는 과정에서 (eq? ( + a 1 ) b )를 예를 들어 보면 (a = 1, b = 2) 이 표현식은 #T가 나와야한다.
- 그러나 기본 코드에서는 이 과정에서 #F가 나왔는데, 고친 코드를 살펴보면 plus, minus, divide, multiple를 보면
return값으로 Node(TokenType.INT, int((run_expr(l_node)).value)*int((run_expr(r_node)).value))를 리턴한다. 근데 이 과정에서 
value의 인자값으로 넘어가는 부분이 INT인 상태로 넘어가는데, INT상태로 넘어가면 eq_?에서 받을때 NODE 오브젝트를 받아서 같은지를
판별할 수가 없었음. 그래서 str(int((run_expr(l_node)).value)*int((run_expr(r_node)).value)))로 바꾸면 eq_?가 정상적으로 작동한다. 이유는 아직 해결하지 못하였음.

6/9(Fri)
(commit log - "lambda commit")
- lambda 간단한 소스 테스트
- run_expr함수 과정에서 List가 두 개 들어갈시 오류가나서 수정해서 테스트한 결과 통과
- 테스트 11번까지 통과
- lamda 피라미터 부분, 바디 부분, 실제 피라미터 부분을 받아와서 바인딩 진행
- 피라미터는 while문을 통하여 무한히 계속 받을수 있도록 구현
- return값은 body부분을 run_expr에 인자로 넣으면 계산한 결과가 출력된다.

6/10(Sat)
(commit log - "lambda commit")
- lambda 최종완성
- 17, 19 제외한 테스트 모두 성공
- 다만 함수 이름에 '_'가 들어가면 오류가 떠서 _를 삭제시키고 수행
- actual parameter에 변수가 들어왔을 시 테이블에서 변수를 읽어오고 함수가 들어왔을 시 그 함수를 수행한 결과를 다시 피라미터로 셋팅한다.
- List가 두 개가 연속으로 선언 되어있을 때 기존 run_expr에서 오류를 발생시켜서 List가 두 개가 연속으로 선언되었을 때(lamda함수의 경우)의 경우를 만들어서 다시 셋팅하였고, List 다음에 정의한 함수 이름이 나올 경우 테이블에서 정의된 lambda함수를 불러와서 다시 수행시킨다.
