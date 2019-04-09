# Wei Chen
# 110926494
# 4/5/19
import ply.lex as lex
import sys
import ply.yacc as yacc

# debugging = True
debugging = False


def debug(s, t=""):
    global debugging
    if debugging:
        print(s, t)


class Node:
    def __init__(self):
        self.value = -1

    def evaluate(self):
        return self.value

    def execute(self):
        return self.value


class BooleanNode(Node):
    def __init__(self, s):
        super().__init__()
        # debug("Boolean ")
        if s == 'True' or s == True:
            self.value = True
        else:
            self.value = False

    def negate(self):
        debug("BooleanNode negate:", self.value)
        self.value = not self.value
        debug("BooleanNode negate:", self.value)
        return self

    def evaluate(self):
        return self.value

    def execute(self):
        # print(str(self.value).lower())
        # return str(self.value).lower()
        return self.value


class StringNode(Node):
    def __init__(self, s):
        super().__init__()
        self.value = str(s)

    def get_element(self, index):
        if index < 0:
            raise Exception("string index cannot be negative")
        return StringNode(self.value[index])

    def evaluate(self):
        return self.value

    def execute(self):
        return self.value

    def replace(self, param, param1):
        self.value = self.value.replace(param, param1)
        pass


class NumberNode(Node):
    def __init__(self, v):
        super().__init__()
        if '.' in v or 'e' in v:
            self.value = float(v)
        else:
            self.value = int(v)

    def evaluate(self):
        return self.value

    def execute(self):
        return self.value


class IntNode(NumberNode):
    def __init__(self, v):
        super().__init__(v)
        self.value = int(v)

    def evaluate(self):
        return self.value

    def execute(self):
        return self.value


class FloatNode(NumberNode):
    def __init__(self, v):
        super().__init__(v)
        self.value = float(v)

    def evaluate(self):
        return self.value

    def execute(self):
        return self.value


# class NotNode(Node):
#     def __init__(self, v):
#         super().__init__()
#         if isinstance(v,BooleanNode):
#             raise Exception("can't not a non boolean")
#         self.value = not v
#
#     def evaluate(self):
#         return self.value

class UminusNode(Node):
    def __init__(self, v):
        super().__init__()
        # print(v,)
        self.value = -v.evaluate()

    def evaluate(self):
        return self.value


class ComparisonNode(BooleanNode):
    def __init__(self, comparator, v1, v2):
        super().__init__(False)
        self.comparator = comparator
        self.v1 = v1
        self.v2 = v2
        debug("ComparisonNode: compare= ", comparator)
        debug("ComparisonNode: v1= ", v1)
        debug("ComparisonNode: v2= ", v2)

    def evaluate(self):
        v1 = self.v1.evaluate()
        v2 = self.v2.evaluate()
        debug("ComparisonNode: v1= ", v1)
        debug("ComparisonNode: v2= ", v2)
        if (isinstance(v1, bool) and not isinstance(v2, bool)) or (not isinstance(v1, bool) and isinstance(v2, bool)):
            raise ValueError
        try:
            if self.comparator == '<':
                self.value = v1 < v2
            elif self.comparator == '>':
                self.value = (v1 > v2)

            elif self.comparator == '<=':
                self.value = (v1 <= v2)
            elif self.comparator == '>=':
                self.value = (v1 >= v2)
            elif self.comparator == '==':
                self.value = (v1 == v2)
            elif self.comparator == '<>':
                self.value = (v1 < v2 or v1 > v2)
            elif self.comparator == 'andalso':
                if not isinstance(v1, (bool, ComparisonNode)) or not isinstance(v2, (bool, ComparisonNode)):
                    raise ValueError
                self.value = (v1 and v2)
            elif self.comparator == 'orelse':
                if not isinstance(v1, (bool, ComparisonNode)) or not isinstance(v2, (bool, ComparisonNode)):
                    raise ValueError
                self.value = (v1 or v2)

            return self.value
        except Exception:
            raise Exception("SEMANTIC ERROR222")

    def execute(self):
        self.evaluate()
        # print("compare execute")
        return self.value


class BopNode(Node):
    def __init__(self, op, v1, v2):
        super().__init__()
        self.v1 = v1
        self.v2 = v2
        self.op = op
        self.value = 0

    def evaluate(self):
        v1 = self.v1.evaluate()
        v2 = self.v2.evaluate()
        if isinstance(v1, bool) or isinstance(v2, bool):
            raise ValueError
        try:
            if self.op == '+':
                self.value = v1 + v2
            elif self.op == '-':
                # if not isinstance(v1,int) or not isinstance(v2,int):
                #     raise ValueError
                self.value = v1 - v2
            elif self.op == '*':
                self.value = v1 * v2

            elif self.op == '/':

                self.value = v1 / v2
            elif self.op == '**':
                self.value = v1 ** v2
            elif self.op == 'mod':
                if isinstance(v1, int) and isinstance(v2, int):
                    self.value = v1 % v2
                else:
                    raise ValueError
            elif self.op == 'div':
                if isinstance(v1, int) and isinstance(v2, int):
                    self.value = v1 // v2
                else:
                    raise ValueError

            debug(self.value)
            return self.value
        except Exception as e:
            debug(e)
            raise Exception("SEMANTIC ERROR")

    def execute(self):
        debug(self.value)
        self.evaluate()
        return self.value


class ListNode(Node):
    def __init__(self, v=None):
        super().__init__()
        if v is None:
            self.value = []
        else:
            self.value = [v]

    def append(self, v):
        self.value.append(v)
        return self

    def cons(self, v):
        self.value.insert(0, v)
        return self

    def get_element(self, index):
        if index < 0:
            raise Exception("SEMANTIC ERROR")
        return self.value[index]

    def evaluate(self):
        return [x.evaluate() for x in self.value]

    def execute(self):
        return [x.execute() for x in self.value]


class TupleNode(Node):
    def __init__(self, l):
        # TupleNode takes in a list and convert to tuple
        # Maybe takes a ListNode?
        super().__init__()
        self.value = tuple(l)

    def get_element(self, index):
        if index <= 0:
            raise Exception("SEMANTIC ERROR")
        return self.value[index - 1]

    def evaluate(self):
        return tuple([x.evaluate() for x in self.value])

    def execute(self):
        return tuple([x.execute() for x in self.value])


reserved = {
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'while': 'WHILE',

}
tokens = [
    'NUMBER', 'INTEGER', 'REAL', 'STRING', 'BOOLEAN',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'POWER', 'MOD', 'DIV',
    'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET',
    'COMMA', 'HASHTAG', 'SEMICOLON', 'IN', 'CONS',
    'LES', 'GRT', 'LEQ', 'GEQ', 'EQUALEQUAL', 'LESORGRT',
    'NOT', 'ANDALSO', 'ORELSE',
    'ID',
]+list(reserved.values())

# Tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COMMA = r','
t_SEMICOLON = r';'
t_HASHTAG = r'[#]'
t_POWER = r'\*\*'
t_MOD = r'mod'
t_DIV = r'div'
t_IN = r'in'
t_CONS = r'::'
t_EQUAL = r'='
t_EQUALEQUAL = r'=='
t_LES = r'<'
t_GRT = r'>'
t_LEQ = r'<='
t_GEQ = r'>='
t_LESORGRT = r'<>'
t_NOT = r'not'
t_ANDALSO = r'andalso'
t_ORELSE = r'orelse'


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t

def t_NUMBER(t):
    r'\d*(\d\.|\.\d)\d*([eE]-?\d+)?|\d+'
    try:
        t.value = NumberNode(t.value)
        debug(t.value.value)
    except ValueError:
        raise SyntaxError("SYNTAX ERROR")
        # t.value = 0
    return t


def t_STRING(t):
    r'(\'(\\\n|\\\\|\\\"|\\\'|\\\t|[^\\\'])*\')|(\"(\\\n|\\\\|\\\"|\\\'|\\\t|[^\\\"])*\")'

    try:
        # print(t.value[1:-1])
        string = str(t.value.replace("\\\\", "\\")
                     .replace('\\\n', '\n')
                     .replace('\\\'', '\'')
                     .replace('\\\"', '\"')
                     .replace('\\\t', '\t')
                     )
        t.value = StringNode(string[1:-1])
    except ValueError:
        raise SyntaxError("SYNTAX ERROR")
        # t.value = ''
    return t


def t_BOOLEAN(t):
    r'(True)|(False)'
    t.value = BooleanNode(t.value)
    return t


# Ignored characters
t_ignore = " \t"


def t_error(t):
    raise SyntaxError("SYNTAX ERROR")


# Build the lexer
lex.lex()

# Parsing rules
precedence = (
    ('left', 'ORELSE'),
    ('left', 'ANDALSO'),
    ('left', 'NOT'),
    ('left', 'LES', 'GRT', 'LEQ', 'GEQ', 'EQUALEQUAL', 'LESORGRT'),
    ('right', 'CONS'),
    ('left', 'IN'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MOD', 'DIV'),
    ('right', 'UMINUS'),
    ('right', 'POWER'),
    ('nonassoc', 'LBRACKET', 'RBRACKET'),
    ('left', 'HASHTAG'),
    ('nonassoc', 'LPAREN', 'RPAREN'),
)

class PrintNode(Node):
    def __init__(self, v):
        super().__init__()
        if isinstance(v, str):
            v = "'" + v + "'"
        self.value = v

    def execute(self):
        # self.value = self.value.evaluate
        print(self.value)
        return self.value

# dictionary of names
names = {}

def p_statement_assignment(t):
    '''statement : NAME EQUALS expression SEMICOLON
                 | expression LBRACKET expression RBRACKET'''

    if len(t) == 4:



    # print(t[1])
def p_statement_print(t):
  t  'statement : PRINT LPAREN expression RPAREN'
    debug("p_expression_statement:", t[3])
    debug("p_expression_statement:", t[3].value)
    debug("p_expression_statement:", t[3].evaluate())
    t[0] = PrintNode(t[3].evaluate())


def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    # print("p_expression_group")
    t[0] = t[2]


def p_expression_binop(t):
    '''expression : expression PLUS expression
                      | expression MINUS expression
                      | expression TIMES expression
                      | expression DIVIDE expression
                      | expression POWER expression
                      | expression MOD expression
                      | expression DIV expression'''
    debug("p_expression_binop")
    # print(t[1].value)
    # print(t[3].value)
    t[0] = BopNode(t[2], t[1], t[3])
    debug(t[0])


def p_expression_elements(t):
    '''elements : elements COMMA expression
                | expression'''
    if len(t) > 2:
        t[1].append(t[3])
        t[0] = t[1]
        # print("p_expression_elements if", t[0].execute())
    else:
        # print("p_expression_elements else", )

        t[0] = ListNode(t[1])
        # print(t[0].execute())


def p_expression_tuple(t):
    '''tuple : LPAREN elements RPAREN
             | LPAREN RPAREN'''

    if len(t) > 3:
        t[0] = TupleNode(t[2].value)  # t[2] = elements seperated by comma, ex. "1,2,3"
    else:
        t[0] = TupleNode([])


def p_expression_tuple_index(t):
    '''indexing : HASHTAG expression LPAREN expression RPAREN
                | HASHTAG expression expression '''
    # print("p_expression_tuple_index")
    # print(t[2])
    index = t[2].evaluate()
    if isinstance(index, bool) or not isinstance(index, int):
        raise ValueError
    if len(t) > 4:
        t[0] = t[4].get_element(index)
    else:
        t[0] = t[3].get_element(index)


def p_expression_list(t):
    '''list : LBRACKET elements RBRACKET
            | LBRACKET RBRACKET'''
    debug("p_expression_list")
    if len(t) > 3:
        # print("p_expression_list if")
        t[0] = t[2]
    else:
        # print("p_expression_list else")
        t[0] = ListNode()


def p_expression_list_index(t):
    'indexing : expression LBRACKET expression RBRACKET'

    # print(t[3])
    index = t[3].evaluate()
    debug("p_expression_list_index", index)
    if isinstance(index, bool) or not isinstance(index, int) or not isinstance(t[1], (ListNode, StringNode)):
        raise ValueError
    t[0] = t[1].get_element(index)


def p_expression_in(t):
    'expression : expression IN expression'
    # t1 can be anything, when t3 is list
    # t1 must be str when t3 is str
    t3 = t[3].evaluate()
    t1 = t[1].evaluate()
    if isinstance(t3, list):
        condition = t1 in t3
        t[0] = BooleanNode(condition)
    elif isinstance(t3, str):
        if isinstance(t1, str):
            condition = t1 in t3
            t[0] = BooleanNode(condition)
        else:
            raise ValueError
    else:
        raise ValueError


def p_expression_cons(t):
    '''expression : expression CONS expression'''
    # t3 must be list
    # print(t[1])
    t[0] = t[3].cons(t[1])


def p_expression_comparison(t):
    """expression : expression LES expression
                      | expression GRT expression
                      | expression LEQ expression
                      | expression GEQ expression
                      | expression EQUALEQUAL expression
                      | expression LESORGRT expression
                      | expression ANDALSO expression
                      | expression ORELSE expression"""
    # print(t[2])
    # print(t[1].value, t[1])
    # print(t[3].value, t[3])
    t[0] = ComparisonNode(t[2], t[1], t[3])
    # print(t[0].value, t[0])


def p_expression_not(t):
    'expression : NOT expression'
    # FIXME: replace value with evaluate
    if not isinstance(t[2].evaluate(), bool):
        raise ValueError
    debug("p_expression_not: ", t[2].value)
    t[0] = BooleanNode(not t[2].evaluate())
    debug("p_expression_not: ", t[0].value)


def p_expression_uminus(t):
    'expression : MINUS expression %prec UMINUS'
    t[0] = UminusNode(t[2])


def p_expression_factor(t):
    '''expression : factor
                  | indexing'''

    t[0] = t[1]


def p_factor(t):
    '''factor : NUMBER
              | BOOLEAN
              | STRING
              | tuple
              | list'''
    debug("p_factor ", t[1])
    t[0] = t[1]


# def p_expression_list_index(t):
#     'expression : list  LBRACKET expression RBRACKET'
#     t[0] = (t[1])[t[3]]


def p_error(t):
    raise SyntaxError("SYNTAX ERROR")
    # print("Syntax error at '%s'" % t.value)


yacc.yacc()


def test_one(input=";"):
    code = [input]
    # code = [
    # "11==12 orelse 1>2;"
    # '1/0;'
    # '-1;'
    # "[1]::2::[4];"
    # "5mod2;"
    # "1 + 2.0 * 3.0;"
    #
    # '1-2;'
    # "3 div 2;"
    # "3 mod 2;"
    # "4 mod 2;"
    # "true;"
    # "'Hello\\\n\\\\World';"

    # ]

    ast = None
    try:
        # lex.input(code)
        # while True:
        #     token = lex.token()
        #     if not token: break
        # print(token)
        print(">>>", code[0])
        ast = yacc.parse(code[0])

        # print(ast)
        # print(eval(code))
        # assert ast.execute() == eval(code)
    except AssertionError:
        print("AssertionError")
    except SyntaxError as err:
        # debug("err:", err)
        print("SYNTAX ERROR")

    except Exception as err:
        # print("err:", err)
        print("SEMANTIC ERROR")

    try:
        # print(ast.execute())
        ast.execute()
        debug("executed successfully")
    except AssertionError:
        print("AssertionError")
    except Exception as err:
        print("err:", err)
        print("SEMANTIC ERROR")


# test_one("(1<2) andalso False;")
# print('------------')


def filecompare(fn1, fn2):
    f1 = open(fn1, "r")
    f2 = open(fn2, "r")
    for line1 in f1:

        for line2 in f2:
            line2 = line2.replace("false", "False").replace("true", "True")
            if line1.strip() == line2.strip():
                print("SAME\n")
            else:
                print("l1: '", line1, "'")
                print("l2: '", line2, "'")
            assert line1.strip() == line2.strip()
            break
    f1.close()
    f2.close()


def file_tests(i=1, j=41):
    for i in range(i, j):
        print(i, ":")
        infile = "./cases/input_{}.txt".format(i)
        comparefile = "./cases/output_{}.txt".format(i)

        fd = open(infile, 'r')
        codes = []
        for line in fd:
            codes.append(line.strip())
        print("input:", codes)

        # codes = [
        #     "('a','b');",
        #     "(1,2);",
        #     "1.2 - 1;",
        #     "2.1 ** 2;",
        #     "(1-2)------(1-2 );",
        #     "2--2;",
        #     "1-2;",
        #     "2+0;",
        #     "2/0;",
        #     "100*22;",
        #     "2 4;",
        #     # "'Hello World'"
        # ]
        outfile = "./result.txt"

        with open(outfile, 'w+') as outf:
            for code in codes:
                code = code.replace("and", "andalso").replace('or', 'orelse').replace("false", "False").replace("true",
                                                                                                                "True").replace(
                    '//', "div").replace("%", "mod")
                print(code)
                try:
                    # lex.input(code)
                    # while True:
                    #     token = lex.token()
                    #     if not token:
                    #         break
                    # print(token)

                    ast = yacc.parse(code)
                    debug("ast:", ast)
                    result = ast.execute()
                    debug("result:", result)
                    outf.write(str(result))
                    # print(comparefile)
                    # assert ast.execute() == eval(code)
                except AssertionError:
                    print("AssertionError")
                except SyntaxError:
                    print("SYNTAX ERROR")

                except Exception as err:
                    debug(err)
                    print("SEMANTIC ERROR")
                    outf.write("SEMANTIC ERROR\n")
        filecompare(outfile, comparefile)


# file_tests(1, 42)


if len(sys.argv) != 2:
    sys.exit("invalid arguments")

infile = sys.argv[1]
fd = open(infile, 'r')
codes = []
for line in fd:
    codes.append(line.strip())
debug(codes)

for code in codes:
    if code == "":
        continue
    try:
        # lex.input(code)
        # while True:
        #     token = lex.token()
        #     if not token:
        #         break
        # print(token)

        ast = yacc.parse(code)
        debug("ast:", ast)
        result = ast.execute()
        debug("result:", result)
    except SyntaxError:
        print("SYNTAX ERROR")

    except Exception as err:
        print("SEMANTIC ERROR")
