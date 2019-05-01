# Wei Chen
# 110926494
# 4/25/19
import ply.lex as lex
import sys
import ply.yacc as yacc

debugging = True
debugging = False


def debug(s, t=""):
    global debugging
    if debugging:
        print(s, t)


class Stack:
    def __init__(self):
        self.stack = [{}]

    def push(self, dic):
        self.stack.append(dic)

    def pop(self):
        return self.stack.pop()

    def peep(self,index = -1):
        return self.stack[index]


# global stack
stack = Stack()


# var_dictionary of names
# var_dict = {}


class Node:
    def __init__(self):
        self.value = -1

    def execute(self):
        return self.value


# def var_lookup(v):
#     global var_dict
#     debug(var_dict)
#     return var_dict[v]


class IdNode(Node):
    def __init__(self, s):
        super().__init__()
        self.value = s
        debug("IDNode init = ", self.value)

    def execute(self):
        debug("IDNode execute: returns:", stack.stack)
        return stack.peep()[self.value]


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

    def execute(self):
        return self.value


class IntNode(NumberNode):
    def __init__(self, v):
        super().__init__(v)
        self.value = int(v)

    def execute(self):
        return self.value


class FloatNode(NumberNode):
    def __init__(self, v):
        super().__init__(v)
        self.value = float(v)

    def execute(self):
        return self.value


class UminusNode(Node):
    def __init__(self, v):
        super().__init__()
        # print(v,)
        self.value = -v.execute()

    def execute(self):
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

    def execute(self):
        v1 = self.v1.execute()
        v2 = self.v2.execute()
        debug("ComparisonNode: v1= ", v1)
        # debug("ComparisonNode: self v1= ", self.v1.execute())

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
            raise Exception("ComparisonNode ERROR")


class BoolOpNode(BooleanNode):
    def __init__(self, comparator, v1, v2):
        super().__init__(False)
        self.comparator = comparator
        self.v1 = v1
        self.v2 = v2

    def execute(self):
        v1 = self.v1.execute()
        v2 = self.v2.execute()
        if not (isinstance(v1, bool) and isinstance(v2, bool)):
            raise ValueError
        try:
            if self.comparator == 'andalso':
                self.value = (v1 and v2)
            elif self.comparator == 'orelse':
                self.value = (v1 or v2)
            return self.value
        except Exception:
            raise ValueError("bool op error")


class BopNode(Node):
    def __init__(self, op, v1, v2):
        super().__init__()
        self.v1 = v1
        self.v2 = v2
        self.op = op
        self.value = 0

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
            raise Exception("bop error")


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
        debug("Lsit Node get element")
        if index < 0:
            raise Exception("list node ERROR")
        return self.value[index]

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

    def execute(self):
        return tuple([x.execute() for x in self.value])


class PrintNode(Node):
    def __init__(self, v):
        super().__init__()
        # if isinstance(v, str):
        #     v = "'" + v + "'"
        self.value = v

    def execute(self):
        # self.value = self.value.evaluate
        debug("print node exe = ", self.value)
        print(self.value.execute())


def set_var(v, val, index=None):
    # global var_dict

    if index is None:
        stack.peep()[v] = val.execute()
    else:
        debug('set_var: v = {}, val = {}, index = {}'.format(v, val, index))
        if isinstance(v, Node):
            v.execute()[index] = val.execute()
        else:
            stack.peep()[v][index] = val.execute()

    debug('set_var: {}->{}'.format(v, val))


class AssignNode(Node):
    def __init__(self, id_node, value, index=None):
        super().__init__()
        self.id = id_node.value
        self.value = value
        self.index = index
        debug("AssignNode Init id= ", self.id)

    def execute(self):
        index = self.index
        if index is not None:
            index = index.execute()
        debug("AssignNode execute: id = {}, v = {}, i = {}".format(self.id, self.value, index))
        set_var(self.id, self.value, index)

        # debug("AssignNode execute = ", var_lookup(self.id).execute())


class BlockNode(Node):
    def __init__(self, sl):
        super().__init__()
        self.statementList = sl

    def execute(self):
        debug("blocknode statements: {}".format(self.statementList))
        for statement in self.statementList:
            statement.execute()


class IndexingNode(Node):
    def __init__(self, v, index,offset=0):
        super().__init__()
        self.value = v
        self.index = index
        self.offset = offset

    def execute(self):
        index = self.index.execute()-self.offset
        v = self.value
        debug('Indexing Node exe index = {}, v = {}'.format(index, v))
        debug("indexing node exe v = ", v)
        if isinstance(index, bool) or not isinstance(index, int):
            raise ValueError("IndexingNode")
        if isinstance(v, Node):
            v = v.execute()
            debug("indexing node after exe v = ", v)

        debug("indexing node return  v = ", v[index])
        return v[index]


class InNode(Node):
    def __init__(self, v1, v2):
        super().__init__()
        self.v1 = v1
        self.v2 = v2

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

    def execute(self):
        return [self.v1.execute()] + self.v2.execute()


class NotNode(Node):
    def __init__(self, v):
        super().__init__()
        self.v = v

    def execute(self):
        v = self.v.execute()
        if not isinstance(v, bool):
            raise ValueError
        return not v


class ConditionalNode(Node):
    def __init__(self, boolean, block, block2=None):
        super().__init__()
        self.boolean = boolean
        self.block = block
        self.block2 = block2

    def set_else_block(self, b):
        self.block2 = b

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
    def __init__(self, b, block):
        super().__init__()
        self.boolean = b
        self.block = block

    def execute(self):
        boolean = self.boolean.execute()
        if not (isinstance(boolean, bool) and isinstance(self.block, BlockNode)):
            raise ValueError("not bool or block")
        while self.boolean.execute():
            self.block.execute()


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
    'fun': 'FUN',
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
    raise SyntaxError("SYNTAX ERROR_token not found", t)


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

''' fun x(y) = {y = 1;}y;
    x(1);   FunctionNode.execute(1);
'''


class FunctionNode(Node):
    def __init__(self, id, args, block, ret_exp):
        super().__init__()
        self.id = id
        self.args = args
        self.block = block
        self.ret_exp = ret_exp

    def execute(self):
        debug("Function Node exe: {}".format(self.id))
        # execute block first then the expression is evaluated and the value is returned.
        # store this func on stack
        stack.peep()[self.id.value] = self

    def run(self, argv):
        debug("hg76ydv6yn6``````````, args:{}, argv:{}".format(self.args,argv))
        frame = {self.id: self} # FIXME: func are static?
        for i in range(len(argv)):
            frame[self.args.get_element(i).value] = argv[i].execute()
        stack.push(frame)
        self.block.execute()

        print("return exp:{}".format(self.ret_exp.execute()))
        x = self.ret_exp.execute()
        frame =  stack.pop()
        return x


class ProgramNode(Node):
    def __init__(self, block, funcs=None):
        super().__init__()
        self.block = block
        self.funcs = funcs

    def execute(self):
        print("ProgramNode: block:{}, fucs = {}".format(self.block,self.funcs))
        if self.funcs is not None:
            # [func.execute() for func in self.funcs]
            self.funcs.execute()

        print("prognode end&*%^&*(")
        self.block.execute()


def p_program(p):
    '''
    program : funcs block
    '''
    print("p_program")
    p[0] = ProgramNode(p[2], p[1])


def p_program_block(p):
    '''
    program : block
    '''
    print("p_program_block")
    p[0] = ProgramNode(p[1])


def p_program_funcs(p):
    '''
    funcs : funcs func
          | func
    '''
    if len(p) > 2:
        p[1].append(p[3])
        p[0] = p[1]
        # print("p_expression_elements if", t[0].execute())
    else:
        # print("p_expression_elements else", )

        p[0] = ListNode(p[1])
        # print(t[0].execute())


def p_function(p):
    '''
    func : FUN ID LPAREN elements RPAREN EQUAL block expression SEMICOLON
    '''
    # FIXME: ID instead of expression^?

    p[0] = FunctionNode(p[2], p[4], p[7], p[8])


def p_id_elements(t):
    '''elements : elements COMMA ID
                | ID'''
    if len(t) > 2:
        t[1].append(t[3])
        t[0] = t[1]
        # print("p_expression_elements if", t[0].execute())
    else:
        # print("p_expression_elements else", )

        t[0] = ListNode(t[1])
        # print(t[0].execute())


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


def p_while(p):
    '''
    while_statement : WHILE LPAREN expression RPAREN block
    '''
    p[0] = WhileNode(p[3], p[5])


def p_statement_ifelse(p):
    '''
    ifelse_statement : if_statement ELSE block
    '''
    debug("p_statement_ifelse", p[3])
    p[1].set_else_block(p[3])
    p[0] = p[1]


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

class FuncCallNode(Node):
    def __init__(self, id, args):
        self.id = id
        self.args = args

    def execute(self):
        # debug("FuncCall execute: id={}, args = {}".format(self.id.execute(),self.args.value))
        debug("stack********",stack.peep(0))
        return stack.peep(0)[self.id.value].run(self.args.value)


def p_expression_func_call(p):
    '''
    expression : ID LPAREN elements RPAREN
    '''
    p[0] = FuncCallNode(p[1],p[3])
def p_elements(t):
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
    if len(t) > 4:
        # t[0] = t[4].get_element(index)
        t[0] = IndexingNode(t[4], t[2],1)
    else:
        # t[0] = t[3].get_element(index)
        t[0] = IndexingNode(t[3], t[2],1)


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

    var = t[3]
    debug("p_expression_list_index index= ", var)
    t[0] = IndexingNode(t[1], t[3])


def p_expression_in(t):
    'expression : expression IN expression'

    t[0] = InNode(t[1], t[3])


def p_expression_cons(t):
    '''expression : expression CONS expression'''

    t[0] = ConsNode(t[1], t[3])


def p_expression_comparison(t):
    """expression : expression LES expression
                      | expression GRT expression
                      | expression LEQ expression
                      | expression GEQ expression
                      | expression EQUALEQUAL expression
                      | expression LESORGRT expression"""
    t[0] = ComparisonNode(t[2], t[1], t[3])


def p_expression_bool_op(t):
    """expression :  expression ANDALSO expression
                  | expression ORELSE expression"""
    t[0] = BoolOpNode(t[2], t[1], t[3])


def p_expression_not(t):
    'expression : NOT expression'
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
    t[0] = t[1]


def p_error(t):
    raise SyntaxError("SYNTAX ERROR pattern not found ", t)
    # print("Syntax error at '%s'" % t.value)


yacc.yacc(debug=0)

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
