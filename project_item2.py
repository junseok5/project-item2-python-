# -*- coding: utf-8 -*-
from string import letters, digits, whitespace


class CuteType:
    INT = 1
    ID = 4

    MINUS = 2
    PLUS = 3

    L_PAREN = 5
    R_PAREN = 6

    TRUE = 8
    FALSE = 9

    TIMES = 10
    DIV = 11

    LT = 12
    GT = 13
    EQ = 14
    APOSTROPHE = 15

    DEFINE = 20
    LAMBDA = 21
    COND = 22
    QUOTE = 23
    NOT = 24
    CAR = 25
    CDR = 26
    CONS = 27
    ATOM_Q = 28
    NULL_Q = 29
    EQ_Q = 30

    KEYWORD_LIST = ('define', 'lambda', 'cond', 'quote', 'not', 'car', 'cdr', 'cons',
                    'atom?', 'null?', 'eq?')

    BINARYOP_LIST = (DIV, TIMES, MINUS, PLUS, LT, GT, EQ)
    BOOLEAN_LIST = (TRUE, FALSE)


def check_keyword(token):
    """
    :type token:str
    :param token:
    :return:
    """
    if token.lower() in CuteType.KEYWORD_LIST:
        return True
    return False


def _get_keyword_type(token):
    return {
        'define': CuteType.DEFINE,
        'lambda': CuteType.LAMBDA,
        'cond': CuteType.COND,
        'quote': CuteType.QUOTE,
        'not': CuteType.NOT,
        'car': CuteType.CAR,
        'cdr': CuteType.CDR,
        'cons': CuteType.CONS,
        'atom?': CuteType.ATOM_Q,
        'null?': CuteType.NULL_Q,
        'eq?': CuteType.EQ_Q
    }[token]


CUTETYPE_NAMES = dict((eval(attr, globals(), CuteType.__dict__), attr) for attr in dir(
    CuteType()) if not callable(attr) and not attr.startswith('__'))


class Token(object):
    def __init__(self, type, lexeme):
        """
        :type type:CuteType
        :type lexeme: str
        :param type:
        :param lexeme:
        :return:
        """
        if check_keyword(lexeme):
            self.type = _get_keyword_type(lexeme)
            self.lexeme = lexeme
        else:
            self.type = type
            self.lexeme = lexeme
        # print type

    def __str__(self):
        # return self.lexeme
        return '[' + CUTETYPE_NAMES[self.type] + ': ' + self.lexeme + ']'

    def __repr__(self):
        return str(self)


class Scanner:

    def __init__(self, source_string=None):
        """
        :type self.__source_string: str
        :param source_string:
        """
        self.__source_string = source_string
        self.__pos = 0
        self.__length = len(source_string)
        self.__token_list = []

    def __make_token(self, transition_matrix, build_token_func=None):
        old_state = 0
        self.__skip_whitespace()
        temp_char = ''
        return_token = ''
        while not self.eos():
            temp_char = self.get()
            if old_state == 0 and temp_char in (')', '('):
                return_token = temp_char
                old_state = transition_matrix[(old_state, temp_char)]
                break

            return_token += temp_char
            old_state = transition_matrix[(old_state, temp_char)]
            next_char = self.peek()
            if next_char in whitespace or next_char in ('(', ')'):
                break

        return build_token_func(old_state, return_token)

    def scan(self, transition_matrix, build_token_func):
        while not self.eos():
            self.__token_list.append(self.__make_token(
                transition_matrix, build_token_func))
        return self.__token_list

    def pos(self):
        return self.__pos

    def eos(self):
        return self.__pos >= self.__length

    def skip(self, pattern):
        while not self.eos():
            temp_char = self.peek()
            if temp_char in pattern:
                temp_char = self.get()
            else:
                break

    def __skip_whitespace(self):
        self.skip(whitespace)

    def peek(self, length=1):
        return self.__source_string[self.__pos: self.__pos + length]

    def get(self, length=1):
        return_get_string = self.peek(length)
        self.__pos += len(return_get_string)
        return return_get_string


class CuteScanner(object):

    transM = {}

    def __init__(self, source):
        """
        :type source:str
        :param source:
        :return:
        """
        self.source = source
        self._init_TM()

    def _init_TM(self):
        for alpha in letters:
            self.transM[(0, alpha)] = 4
            self.transM[(4, alpha)] = 4

        for digit in digits:
            self.transM[(0, digit)] = 1
            self.transM[(1, digit)] = 1
            self.transM[(2, digit)] = 1
            self.transM[(4, digit)] = 4

        self.transM[(4, '?')] = 16
        self.transM[(0, '-')] = 2
        self.transM[(0, '+')] = 3
        self.transM[(0, '(')] = 5
        self.transM[(0, ')')] = 6

        self.transM[(0, '#')] = 7
        self.transM[(7, 'T')] = 8
        self.transM[(7, 'F')] = 9

        self.transM[(0, '/')] = 11
        self.transM[(0, '*')] = 10

        self.transM[(0, '<')] = 12
        self.transM[(0, '>')] = 13
        self.transM[(0, '=')] = 14
        self.transM[(0, "'")] = 15

    def tokenize(self):

        def build_token(type, lexeme): return Token(type, lexeme)
        cute_scanner = Scanner(self.source)
        return cute_scanner.scan(self.transM, build_token)


class TokenType():
    INT = 1
    ID = 4
    MINUS = 2
    PLUS = 3
    LIST = 5
    TRUE = 8
    FALSE = 9
    TIMES = 10
    DIV = 11
    LT = 12
    GT = 13
    EQ = 14
    APOSTROPHE = 15
    DEFINE = 20
    LAMBDA = 21
    COND = 22
    QUOTE = 23
    NOT = 24
    CAR = 25
    CDR = 26
    CONS = 27
    ATOM_Q = 28
    NULL_Q = 29
    EQ_Q = 30

NODETYPE_NAMES = dict((eval(attr, globals(), TokenType.__dict__), attr) for attr in dir(
    TokenType()) if not callable(attr) and not attr.startswith('__'))

class Node (object):

    def __init__(self, type, value=None):
        self.next = None
        self.value = value
        self.type = type

    def set_last_next(self, next_node):
        if self.next is not None:
            self.next.set_last_next(next_node)

        else:
            self.next = next_node

    def __str__(self):
        result = ''

        if self.type is TokenType.ID:
            result = '[' + NODETYPE_NAMES[self.type] + ':' + self.value + ']'
        elif self.type is TokenType.INT:
            result = '['+NODETYPE_NAMES[self.type]+':' + self.value + ']'
        elif self.type is TokenType.LIST:
            if self.value is not None:
                if self.value.type is TokenType.QUOTE:
                    result = str(self.value)
                else:
                    result = '(' + str(self.value) + ')'
            else:
                result = '(' + str(self.value) + ')'
        elif self.type is TokenType.QUOTE:
            result = "\'"
        else:
            result = '['+NODETYPE_NAMES[self.type]+']'

        # fill out
        if self.next is not None:
            return result + ' ' + str(self.next)
        else:
            return result


class BasicPaser(object):

    def __init__(self, token_list):
        """
        :type token_list:list
        :param token_list:
        :return:
        """
        self.token_iter = iter(token_list)

    def _get_next_token(self):
        """
        :rtype: Token
        :return:
        """
        next_token = next(self.token_iter, None)
        if next_token is None:
            return None
        return next_token

    def parse_expr(self):
        """
        :rtype : Node
        :return:
        """
        token = self._get_next_token()

        '"":type :Token""'
        if token is None:
            return None
        result = self._create_node(token)
        return result

    def _create_node(self, token):
        if token is None:
            return None
        elif token.type is CuteType.INT:
            return Node(TokenType.INT,  token.lexeme)
        elif token.type is CuteType.ID:
            return Node(TokenType.ID,   token.lexeme)
        elif token.type is CuteType.L_PAREN:
            return Node(TokenType.LIST, self._parse_expr_list())
        elif token.type is CuteType.R_PAREN:
            return None
        elif token.type in CuteType.BOOLEAN_LIST:
            return Node(token.type)
        elif token.type in CuteType.BINARYOP_LIST:
            return Node(token.type, token.lexeme)
        elif token.type is CuteType.QUOTE:
            return Node(TokenType.QUOTE, token.lexeme)
        elif token.type is CuteType.APOSTROPHE:
            node = Node(TokenType.LIST, Node(TokenType.QUOTE, token.lexeme))
            node.value.next = self.parse_expr()
            return node
        elif check_keyword(token.lexeme):
            return Node(token.type, token.lexeme)

    def _parse_expr_list(self):
        head = self.parse_expr()
        '"":type :Node""'
        if head is not None:
            head.next = self._parse_expr_list()
        return head


def run_list(root_node):
    """
    :type root_node: Node
    """
    op_code_node = root_node.value

    return run_func(op_code_node)(root_node)


def run_func(op_code_node):
    """
    :type op_code_node:Node/
    """
    def quote(node):
        return node

    def strip_quote(node):
        """
        :type node: Node
        """
        if node.type is TokenType.LIST:
            if node.value is TokenType.QUOTE or TokenType.APOSTROPHE:
                return node.value.next
        if node.type is TokenType.QUOTE:
            return node.next
        return node

    def cons(node):
        """
        :type node: Node
        """
        l_node = node.value.next
        r_node = l_node.next
        if l_node.type is TokenType.ID:
            l_node = lookupTable(l_node.value)
        if r_node.type is TokenType.ID:
            r_node = lookupTable(r_node.value)
        r_node = run_expr(r_node)
        l_node = run_expr(l_node)
        new_r_node = r_node
        new_l_node = l_node
        new_r_node = strip_quote(new_r_node)
        new_l_node = strip_quote(new_l_node)
        new_l_node.next = new_r_node.value

        return create_new_quote_list(new_l_node, True)

    def car(node):
        l_node = node.value.next
        if l_node.type is TokenType.ID:
            l_node = lookupTable(l_node.value)
        else:
            l_node = run_expr(node.value.next)
        result = strip_quote(l_node).value
        if result.type is not TokenType.LIST:
            return result
        return create_new_quote_list(result)

    def cdr(node):
        """
        :type node: Node
        """
        l_node = node.value.next
        if l_node.type is TokenType.ID:
            l_node = lookupTable(l_node.value)
        else:
            l_node = run_expr(l_node)
        new_r_node = strip_quote(l_node)
        return create_new_quote_list(new_r_node.value.next, True)

    def null_q(node):
        l_node = node.value.next
        if l_node.type is TokenType.ID:
            l_node = lookupTable(l_node.value)
        else:
            l_node = run_expr(node.value.next)
        new_l_node = strip_quote(l_node).value
        if new_l_node is None:
            return Node(TokenType.TRUE)
        else:
            return Node(TokenType.FALSE)

    def atom_q(node):
        l_node = node.value.next
        if l_node.type is TokenType.ID:
            l_node = lookupTable(l_node.value)
        else:
            l_node = run_expr(node.value.next)
        new_l_node = strip_quote(l_node)

        if new_l_node.type is TokenType.LIST:
            if new_l_node.value is None:
                return Node(TokenType.TRUE)
            return Node(TokenType.FALSE)
        else:
            return Node(TokenType.TRUE)

    def eq_q(node):
        l_node = node.value.next
        r_node = l_node.next
        if l_node.type is TokenType.ID:
            l_node = lookupTable(l_node.value)
        if r_node.type is TokenType.ID:
            r_node = lookupTable(r_node.value)
        new_l_node = strip_quote(run_expr(l_node))
        new_r_node = strip_quote(run_expr(r_node))
        if (new_l_node.type or new_r_node.type) is not TokenType.INT:
            return Node(TokenType.FALSE)
        if new_l_node.value == new_r_node.value:
            return Node(TokenType.TRUE)
        return Node(TokenType.FALSE)

    # Fill Out
    # table을 보고 함수를 작성하시오--------------------------------------------------------------------------------------------
    def define(node):
        l_node = node.value.next
        r_node = l_node.next

        new_r_node = (run_expr(r_node))
        insertTable(l_node.value, new_r_node)
        print lookupTable(l_node.value)

    def lambda_exe(node):
        # lambda 구조에 따른 값 전달
        param = node.value.next.value
        if (node.value.next.next.value.type is TokenType.DEFINE):   # local 변수 정의가 존재한다면
            local_vars = node.value.next.next
            body = node.value.next.next.next
        else:
            body = node.value.next.next

        if (node.next is not None):
            act_param = node.next
        else:
            return node

        # 피라미터 바인딩
        while (param is not None):
            if (act_param.type is TokenType.ID):  # actual parameter가 저장되어 있는 변수 또는 함수일 경우
                lookup_act_param = lookupTable(act_param.value)
                insertTable(param.value, lookup_act_param)
            elif (act_param.type is TokenType.LIST):    # actual parameter이 함수일 경우
                act_param = run_expr(act_param)
                insertTable(param.value, act_param)
            else:   # actual parameter가 숫자일 경우
                insertTable(param.value, act_param)
            if (param.next is not None):
                param = param.next
                act_param = act_param.next
            else:
                break;

        return run_expr(body)


    def cond(node):
        l_node = node.value.next
        if l_node.type is TokenType.ID:
            l_node = lookupTable(l_node.value)

        if l_node is not None:
            return run_cond(l_node)
        else:
            print('cond null error!')

    def run_cond(node):
        """
        :type node: Node
        """
        #Fill Out
        if run_expr(node.value).type is TokenType.TRUE:
            return node.value.next
        else:
            return run_cond(node.next)

    def plus(node):
        l_node = node.value.next
        r_node = l_node.next

        if l_node.type is TokenType.ID:
            l_node = lookupTable(l_node.value)
        if r_node.type is TokenType.ID:
            r_node = lookupTable(r_node.value)
        return Node(TokenType.INT, str(int((run_expr(l_node)).value)+int((run_expr(r_node)).value)))


    def minus(node):
        l_node = node.value.next
        r_node = l_node.next
        if l_node.type is TokenType.ID:
            l_node = lookupTable(l_node.value)
        if r_node.type is TokenType.ID:
            r_node = lookupTable(r_node.value)
        return Node(TokenType.INT, str(int((run_expr(l_node)).value)-int((run_expr(r_node)).value)))

    def multiple(node):
        l_node = node.value.next
        r_node = l_node.next
        if l_node.type is TokenType.ID:
            l_node = lookupTable(l_node.value)
        if r_node.type is TokenType.ID:
            r_node = lookupTable(r_node.value)
        return Node(TokenType.INT, str(int((run_expr(l_node)).value)*int((run_expr(r_node)).value)))

    def divide(node):
        l_node = node.value.next
        r_node = l_node.next
        if l_node.type is TokenType.ID:
            l_node = lookupTable(l_node.value)
        if r_node.type is TokenType.ID:
            r_node = lookupTable(r_node.value)
        return Node(TokenType.INT, str(int((run_expr(l_node)).value)/int((run_expr(r_node)).value)))

    def lt(node):
        l_node = node.value.next
        r_node = l_node.next
        if l_node.type is TokenType.ID:
            l_node = lookupTable(l_node.value)
        if r_node.type is TokenType.ID:
            r_node = lookupTable(r_node.value)

        if int((run_expr(l_node)).value) < int((run_expr(r_node)).value):
            return Node(TokenType.TRUE)
        else:
            return Node(TokenType.FALSE)

    def gt(node):
        l_node = node.value.next
        r_node = l_node.next
        if l_node.type is TokenType.ID:
            l_node = lookupTable(l_node.value)
        if r_node.type is TokenType.ID:
            r_node = lookupTable(r_node.value)

        if int((run_expr(l_node)).value) > int((run_expr(r_node)).value):
            return Node(TokenType.TRUE)
        else:
            return Node(TokenType.FALSE)

    def eq(node):
        l_node = node.value.next
        r_node = l_node.next
        if l_node.type is TokenType.ID:
            l_node = lookupTable(l_node.value)
        if r_node.type is TokenType.ID:
            r_node = lookupTable(r_node.value)
        if int((run_expr(l_node)).value) == int((run_expr(r_node)).value):
            return Node(TokenType.TRUE)
        else:
            return Node(TokenType.FALSE)

    def not_op(node):
        l_node = node.value.next
        if l_node.type is TokenType.ID:
            l_node = lookupTable(l_node.value)
        if (run_expr(l_node)).type is TokenType.FALSE:
            return Node(TokenType.TRUE)
        else:
            return Node(TokenType.FALSE)




    def create_new_quote_list(value_node, list_flag=False):
        """
        :type value_node: Node
        """
        quote_list = Node(TokenType.QUOTE, 'quote')
        wrapper_new_list = Node(TokenType.LIST, quote_list)
        if value_node is None:
            pass
        elif value_node.type is TokenType.LIST:
            if list_flag:
                inner_l_node = Node(TokenType.LIST, value_node)
                quote_list.next = inner_l_node
            else:
                quote_list.next = value_node
            return wrapper_new_list
        new_value_list = Node(TokenType.LIST, value_node)
        quote_list.next = new_value_list
        return wrapper_new_list

    table = {}
    table['cons'] = cons
    table["'"] = quote
    table['quote'] = quote
    table['cdr'] = cdr
    table['car'] = car
    table['eq?'] = eq_q
    table['null?'] = null_q
    table['atom?'] = atom_q
    table['not'] = not_op
    table['+'] = plus
    table['-'] = minus
    table['*'] = multiple
    table['/'] = divide
    table['<'] = lt
    table['>'] = gt
    table['='] = eq
    table['cond'] = cond
    table['define'] = define
    table['lambda'] = lambda_exe
    return table[op_code_node.value]


def run_expr(root_node):
    """
    :type root_node : Node
    """
    if root_node is None:
        return None

    if root_node.type is TokenType.ID:
        return root_node
    elif root_node.type is TokenType.INT:
        return root_node
    elif root_node.type is TokenType.TRUE:
        return root_node
    elif root_node.type is TokenType.FALSE:
        return root_node
    elif root_node.type is TokenType.LIST:
        if (root_node.value.type is TokenType.LIST):    # lamda 함수 이용 시 괄호 두 개에 대한 입력 받을 시
            return run_list(root_node.value)
        if (root_node.value.value in MyDiction):     # root_node.value.value라는 이름을 가진 함수가 선언되어 있을 시
            key = root_node.value.value
            lambda_node = lookupTable(key)
            act_parameter = root_node.value.next
            lambda_node.next = act_parameter        # actual parameter 함수 뒤에 달아주기
            root_node = lambda_node
        return run_list(root_node)
    else:
        print 'Run Expr Error'
    return None

MyDiction = dict()

def print_node(node):
    """
    "Evaluation 후 결과를 출력하기 위한 함수"
    "입력은 List Node 또는 atom"
    :type node: Node
    """
    def print_list(node):
        """
        "List노드의 value에 대해서 출력"
        "( 2 3 )이 입력이면 2와 3에 대해서 모두 출력함"
        :type node: Node
        """
        def print_list_val(node):
            if node.next is not None:
                return print_node(node)+' '+print_list_val(node.next)
            return print_node(node)

        if node.type is TokenType.LIST:
            if node.value is None:
                return '( )'
            if node.value.type is TokenType.QUOTE:
                return print_node(node.value)
            return '('+print_list_val(node.value)+')'

    if node is None:
        return ''
    if node.type is TokenType.ID:
        if MyDiction.__len__() == 0:
            return node.value
        else:
            for a in MyDiction:
                if node.value == a:
                    return print_node(lookupTable(node.value))
                else:
                    continue
                return node.value
    if node.type is TokenType.INT:
        return node.value
    if node.type is TokenType.TRUE:
        return '#T'
    if node.type is TokenType.FALSE:
        return '#F'
    if node.type is TokenType.PLUS:
        return '+'
    if node.type is TokenType.MINUS:
        return '-'
    if node.type is TokenType.TIMES:
        return '*'
    if node.type is TokenType.DIV:
        return '/'
    if node.type is TokenType.GT:
        return '>'
    if node.type is TokenType.LT:
        return '<'
    if node.type is TokenType.EQ:
        return '='
    if node.type is TokenType.LIST:
        return print_list(node)
    if node.type is TokenType.ATOM_Q:
        return 'atom?'
    if node.type is TokenType.CAR:
        return 'car'
    if node.type is TokenType.CDR:
        return 'cdr'
    if node.type is TokenType.COND:
        return 'cond'
    if node.type is TokenType.CONS:
        return 'cons'
    if node.type is TokenType.LAMBDA:
        return 'lambda'
    if node.type is TokenType.NULL_Q:
        return 'null?'
    if node.type is TokenType.EQ_Q:
        return 'eq?'
    if node.type is TokenType.NOT:
        return 'not'
    if node.type is TokenType.QUOTE:
        return "'"+print_node(node.next)

def insertTable(id, value):
    MyDiction[id] = value

def lookupTable(id):
    return MyDiction[id]



def Test_method(input):
    test_cute = CuteScanner(input)
    test_tokens = test_cute.tokenize()
    test_basic_paser = BasicPaser(test_tokens)
    node = test_basic_paser.parse_expr()
    cute_inter = run_expr(node)
    print "… "+str(print_node(cute_inter))


def Test_All():
    valinput = raw_input("> ")
    """
    아무입력이없으면 종료됩니다.
    """

    if valinput is "":
        print "end"
    else:
        Test_method(valinput)
        Test_All()

Test_All()