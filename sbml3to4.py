# Wei Chen
# 110926494
# 4/5/19
import ply.lex as lex
import sys
import ply.yacc as yacc

debugging = True
# debugging = False


def debug(s, t=""):
    global debugging
    if debugging:
        print(s, t)


# var_dictionary of names
var_dict = {}


class Node:
    def __init__(self):
        self.value = -1

    def evaluate(self):
        return self.value

    def execute(self):
        return self.value


def var_lookup(v):
    global var_dict
    debug(var_dict)
    return var_dict[v]


class IdNode(Node):
    def __init__(self, s):
        super().__init__()
        self.value = s
        debug("IDNode init = ", self.value)

    def evaluate(self):
        debug("IDNode evaluate:", var_dict[self.value])
        debug("ffwff")
        return var_dict[self.value]
        # return var_lookup(self.value)
        # return var_lookup(self.value)
        # return self.value

    def execute(self):
        return var_dict[self.value]


        # return self.evaluate().execute()


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
        if '.' in v:
            self.value = float(v)
        else:
            self.value = int(v)
        debug("NumberNode init = ", self.value)

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
        debug("ComparisonNode: self v1= ", self.v1.execute())

        debug("ComparisonNode: v2= ", v2)
        debug("ComparisonNode: ", self.comparator)
        if isinstance(v1, bool) or isinstance(v2, bool):
            raise ValueError("is bool")
        if not ((isinstance(v1, (int, float)) and isinstance(v2, (int, float))) or (
                isinstance(v1, str) and isinstance(v2, str))):
            raise ValueError(v1)
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

            return self.value
        except Exception:
            raise Exception("SEMANTIC ERROR")

    def execute(self):
        v1 = self.v1.execute()
        v2 = self.v2.evaluate()
        debug("ComparisonNode: v1= ", v1)
        debug("ComparisonNode: self v1= ", self.v1.execute())

        debug("ComparisonNode: v2= ", v2)
        debug("ComparisonNode: ", self.comparator)
        if isinstance(v1, bool) or isinstance(v2, bool):
            raise ValueError("is bool")
        if not ((isinstance(v1, (int, float)) and isinstance(v2, (int, float))) or (
                isinstance(v1, str) and isinstance(v2, str))):
            raise ValueError(v1)
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
            debug("ComparisonNode: value= ", self.value)

            return self.value
        except Exception:
            raise Exception("SEMANTIC ERROR")


class BoolOpNode(BooleanNode):
    def __init__(self, comparator, v1, v2):
        super().__init__(False)
        self.comparator = comparator
        self.v1 = v1
        self.v2 = v2

    def evaluate(self):
        v1 = self.v1.evaluate()
        v2 = self.v2.evaluate()
        if not (isinstance(v1, bool) and isinstance(v2, bool)):
            raise ValueError
        try:
            if self.comparator == 'andalso':
                self.value = (v1 and v2)
            elif self.comparator == 'orelse':
                self.value = (v1 or v2)
            return self.value
        except Exception:
            raise ValueError("SEMANTIC ERROR")

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
        res = self.operate(v1, v2)
        debug("BopNode eval ", self.value)
        return res

    def execute(self):
        v1 = self.v1.execute()
        v2 = self.v2.execute()
        self.operate(v1, v2)
        debug("BopNode exe", self.value)
        return self.value

    def operate(self, v1, v2):

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

            # debug(self.value)
            return self.value
        except Exception as e:
            debug(e)
            raise Exception("SEMANTIC ERROR")


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
        debug("List Node evall", self.value)

        return [x.evaluate() for x in self.value]

    def execute(self):
        debug("List Node exe")
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


class PrintNode(Node):
    def __init__(self, v):
        super().__init__()
        # if isinstance(v, str):
        #     v = "'" + v + "'"
        self.value = v

    def evaluate(self):
        debug("print node eval = ", self.value.evaluate())
        return self.value.evaluate()

    def execute(self):
        # self.value = self.value.evaluate
        # print(self.evaluate())
        debug("print node exe = ", self.value)
        print(self.value.execute())
        # return self.evaluate()


def set_var(v, val, index=None):
    global var_dict

    if index is None:
        var_dict[v] = val.evaluate()
    else:
        v.execute()[index] = val.evaluate()
    debug('set_var: {}->{}'.format(v,val))


class AssignNode(Node):
    def __init__(self, id_node, value, index=None):
        super().__init__()
        self.id = id_node.value
        self.value = value
        self.index = index
        debug("AssignNode Init id= ", self.id)

    def evaluate(self):
        index = self.index
        if index is not None:
            index = index.evaluate()
        # FIXME: or can take index out of set_var, by get value then set it
        set_var(self.id, self.value, index)
        # debug("AssignNode evaluate = ", var_lookup(self.id))

    def execute(self):
        index = self.index
        if index is not None:
            index = index.execute()
        # FIXME: or can take index out of set_var, by get value then set it
        set_var(self.id, self.value, index)
        # debug("AssignNode execute = ", var_dict[self.id])

        # self.evaluate()
        # debug("AssignNode execute = ", var_lookup(self.id).execute())


class BlockNode(Node):
    def __init__(self, sl):
        super().__init__()
        self.statementList = sl

    def evaluate(self):
        for statement in self.statementList:
            statement.evaluate()

    def execute(self):
        for statement in self.statementList:
            statement.execute()


class IndexingNode(Node):
    def __init__(self, v, index):
        super().__init__()
        self.value = v
        self.index = index

    def evaluate(self):
        index = self.index.evaluate()
        v = self.value
        debug("indexing node eval v = ", v)
        if isinstance(index, bool) or not isinstance(index, int):
            raise ValueError("IndexingNode")
        if isinstance(v, Node):
            v = v.evaluate()
            debug("indexing node eval v = ", v)

        return v[index]

    def execute(self):
        debug("indexing node exe v = ", self.value)
        return self.evaluate()


class InNode(Node):
    def __init__(self, v1, v2):
        super().__init__()
        self.v1 = v1
        self.v2 = v2

    def evaluate(self):
        v1 = self.v1.evaluate()
        v2 = self.v2.evaluate()
        if isinstance(v2, (list, str)):
            condition = v1 in v2
            return BooleanNode(condition)
        else:
            raise ValueError

    def execute(self):
        v1 = self.v1.execute()
        v2 = self.v2.execute()
        if isinstance(v2, (list, str)):
            condition = v1 in v2
            return condition
        else:
            raise ValueError


class ConsNode(Node):
    def __init__(self, v1, v2):
        super().__init__()
        self.v1 = v1
        self.v2 = v2

    def evaluate(self):
        self.v2.cons(self.v1)

    def execute(self):
        return self.evaluate()


class NotNode(Node):
    def __init__(self, v):
        super().__init__()
        self.v = v

    def evaluate(self):
        v = self.v.evaluate()
        if not isinstance(v, bool):
            raise ValueError
        return not v

    def execute(self):
        return self.evaluate()


reserved = {
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'while': 'WHILE',
    'print': 'PRINT',
    'mod': 'MOD',
    'div': 'DIV',
    'in': 'IN',
    'not': 'NOT',
    'andalso': 'ANDALSO',
    'orelse': 'ORELSE',
    # 'True' : 'BOOLEAN',
    # 'False' : 'BOOLEAN',

}

tokens = [
             'NUMBER', 'INTEGER', 'REAL', 'STRING', 'BOOLEAN',
             'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'POWER',
             'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET', 'LCURLY', 'RCURLY',
             'COMMA', 'HASHTAG', 'SEMICOLON', 'CONS',
             'LES', 'GRT', 'LEQ', 'GEQ', 'EQUALEQUAL', 'LESORGRT',
             'ID', 'EQUAL',
         ] + list(reserved.values())

# Tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LCURLY = r'\{'
t_RCURLY = r'\}'
t_COMMA = r','
t_SEMICOLON = r';'
t_HASHTAG = r'[#]'
t_POWER = r'\*\*'
t_CONS = r'::'
t_EQUALEQUAL = r'=='
t_LES = r'<'
t_GRT = r'>'
t_LEQ = r'<='
t_GEQ = r'>='
t_LESORGRT = r'<>'
t_EQUAL = r'='




def t_NUMBER(t):
    r'\d*(\d\.|\.\d)\d*([eE]-?\d+)?|\d+'
    try:
        t.value = NumberNode(t.value)
        debug(t.value.value)
    except ValueError:
        raise SyntaxError("SYNTAX ERROR_NUMBER")
        # t.value = 0
    return t


def t_STRING(t):
    r'(\'(\\\n|\\\\|\\\"|\\\'|\\\t|[^\\\'])*\')|(\"(\\\n|\\\\|\\\"|\\\'|\\\t|[^\\\"])*\")'

    try:
        debug(t.value[1:-1])
        # string = str(t.value.replace("\\\\", "\\")
        #              .replace('\\\n', '\n')
        #              .replace('\\\'', '\'')
        #              .replace('\\\"', '\"')
        #              .replace('\\\t', '\t')
        #              )

        t.value = StringNode(t.value[1:-1])
    except ValueError:
        raise SyntaxError("SYNTAX ERROR STR")
        # t.value = ''
    debug(t)
    return t


def t_BOOLEAN(t):
    r'(True)|(False)'
    t.value = BooleanNode(t.value)
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    if t.type == 'ID':
        t.value = IdNode(t.value)
    return t


# Ignored characters
t_ignore = " \t"


def t_error(t):
    raise SyntaxError("SYNTAX ERROR_token not found")


# Build the lexer
lex.lex(debug=0)

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


def p_block2(p):
    '''
     block : LCURLY block RCURLY
    '''
    # [s.execute() for s in p[2]]
    p[0] = p[2]


def p_block(p):
    '''
     block : LCURLY statement_list RCURLY
    '''
    p[0] = BlockNode(p[2])

def p_block_empty(p):
    '''
     block : LCURLY RCURLY
    '''
    p[0] = BlockNode([])

def p_statement_list(p):
    '''
     statement_list : statement_list statement
    '''
    p[0] = p[1] + [p[2]]


def p_statement_list_val(p):
    '''
    statement_list : statement
    '''
    p[0] = [p[1]]


def p_statements(t):
    '''statement : block
                 | assignment SEMICOLON
                 | print SEMICOLON
                 | expression SEMICOLON
                 | ifelse_statement
                 | if_statement
                 | while_statement
    '''
    debug("p_statements:** ", t[1])
    t[0] = t[1]


class ConditionalNode(Node):
    def __init__(self, boolean, block, block2=None):
        super().__init__()
        self.boolean = boolean
        self.block = block
        self.block2 = block2

    def set_else_block(self, b):
        self.block2 = b

    def evaluate(self):
        boolean = self.boolean.evaluate()
        if not (isinstance(boolean, bool) and isinstance(self.block, BlockNode)):
            raise ValueError("not bool or block")
        if boolean:
            self.block.evaluate()
        else:
            if self.block2 is not None:
                self.block2.evaluate()

    def execute(self):
        boolean = self.boolean.execute()
        if not (isinstance(boolean, bool) and isinstance(self.block, BlockNode)):
            raise ValueError("not bool or block")
        if boolean:
            self.block.execute()
        else:
            if self.block2 is not None:
                self.block2.execute()

class WhileNode(Node):
    def __init__(self, bool, block):
        super().__init__()
        self.boolean = bool
        self.block = block

    def evaluate(self):
        boolean = self.boolean.evaluate()
        if not (isinstance(boolean, bool) and isinstance(self.block, BlockNode)):
            raise ValueError("not bool or block")

        while self.boolean.evaluate():
            self.block.evaluate()


    def execute(self):
        boolean = self.boolean.execute()
        if not (isinstance(boolean, bool) and isinstance(self.block, BlockNode)):
            raise ValueError("not bool or block")
        while self.boolean.execute():
            self.block.execute()

def p_while(p):
    '''
    while_statement : WHILE LPAREN expression RPAREN block
    '''
    p[0] = WhileNode(p[3],p[5])

def p_statement_ifelse(p):
    '''
    ifelse_statement : if_statement ELSE block
    '''
    debug("p_statement_ifelse", p[3])
    p[1].set_else_block(p[3])
    p[0] =p[1]


def p_statement_if(p):
    '''
    if_statement : IF LPAREN expression RPAREN block
    '''
    debug("p_statement_if", p[5])
    p[0] = ConditionalNode(p[3], p[5])


def p_statement_assignment(t):
    '''assignment : ID EQUAL expression
                  | expression LBRACKET expression RBRACKET EQUAL expression '''
    debug("p_statement_assignment: ")
    if len(t) == 4:

        t[0] = AssignNode(t[1], t[3])
    else:
        # name = t[1].evaluate()
        # index = t[3].evaluate()
        # if not isinstance(name, IdNode) or isinstance(index, int):  # FIXME: int or IntNode?
        #     raise ValueError("p_statement_assignment semantic")
        # t[0] = AssignNode(name, t[5], index)
        t[0] = AssignNode(t[1], t[6], t[3])

    # print(t[1])


def p_statement_print(t):
    'print : PRINT LPAREN expression RPAREN'
    debug("p_statement_print:", t[3])
    t[0] = PrintNode(t[3])


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
    debug("p_expression_binop", t[0])


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
    # index = t[2].evaluate()
    # if isinstance(index, bool) or not isinstance(index, int):
    #     raise ValueError("p_expression_tuple_index")
    if len(t) > 4:
        # t[0] = t[4].get_element(index)
        t[0] = IndexingNode(t[4],t[2])
    else:
        # t[0] = t[3].get_element(index)
        t[0] = IndexingNode(t[3], t[2])


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
    # index = t[3].evaluate()
    var = t[3]
    debug("p_expression_list_index index= ", var)
    # if isinstance(index, bool) or not isinstance(index, int) or not isinstance(t[1], (ListNode, StringNode, IdNode)):
    #     raise ValueError("p_expression_list_index")
    # t[0] = t[1].get_element(index)
    t[0] = IndexingNode(t[1], t[3])


def p_expression_in(t):
    'expression : expression IN expression'

    t[0] = InNode(t[1], t[3])


def p_expression_cons(t):
    '''expression : expression CONS expression'''
    # t3 must be list
    # print(t[1])

    t[0] = ConsNode(t[1], t[3])
    # t[0] = t[3].cons(t[1])


def p_expression_comparison(t):
    """expression : expression LES expression
                      | expression GRT expression
                      | expression LEQ expression
                      | expression GEQ expression
                      | expression EQUALEQUAL expression
                      | expression LESORGRT expression"""
    # print(t[2])
    # print(t[1].value, t[1])
    # print(t[3].value, t[3])
    t[0] = ComparisonNode(t[2], t[1], t[3])
    # print(t[0].value, t[0])


def p_expression_bool_op(t):
    """expression :  expression ANDALSO expression
                  | expression ORELSE expression"""
    # print(t[2])
    # print(t[1].value, t[1])
    # print(t[3].value, t[3])
    t[0] = BoolOpNode(t[2], t[1], t[3])
    # print(t[0].value, t[0])


def p_expression_not(t):
    'expression : NOT expression'
    # FIXME: replace value with evaluate
    # if not isinstance(t[2].evaluate(), bool):
    #     raise ValueError
    # debug("p_expression_not: ", t[2].value)
    # t[0] = BooleanNode(not t[2].evaluate())
    # debug("p_expression_not: ", t[0].value)
    t[0] = NotNode(t[2])


def p_expression_uminus(t):
    'expression : MINUS expression %prec UMINUS'
    t[0] = UminusNode(t[2])


def p_expression_factor(t):
    '''expression : factor
                  | indexing'''

    t[0] = t[1]


def p_factor(t):
    '''factor : ID
              | NUMBER
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
    raise SyntaxError("SYNTAX ERROR pattern not found ")
    # print("Syntax error at '%s'" % t.value)


yacc.yacc(debug=0)




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

with open(infile, 'r') as myfile:
    code = myfile.read().replace('\n', '')
# root = parser.parse(data)
# root.evaluate()

debug(">>>", code)
if code == "":
    exit(0)
try:
    lex.input(code)
    while True:
        token = lex.token()
        if not token:
            break
        debug(token)
    debug('_______________')

    ast = yacc.parse(code)
    debug("ast:", ast)
    result = ast.execute()
    debug("result:", result)
except SyntaxError as err:
    debug("err:", err)
    print("SYNTAX ERROR")

except Exception as err:
    debug("err:", err)

    print("SEMANTIC ERROR")
