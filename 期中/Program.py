from arrows import *

DIGITS = '0123456789'

class Error:
    def __init__(self, start_pos, end_pos, error_name, details):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error_name}: {self.details}\n'
        result += f'File {self.start_pos.filename}, line {self.start_pos.line + 1}'
        result += '\n\n' + string_with_arrows(self.start_pos.file_text, self.start_pos, self.end_pos)
        return result
    
class SyntaxError(Error):
    def __init__(self, start_pos, end_pos, details=''):
        super().__init__(start_pos, end_pos, 'Syntax Error', details)

class IllegalCharacterError(Error):
    def __init__(self, start_pos, end_pos, details):
        super().__init__(start_pos, end_pos, 'Illegal Character', details)

class RuntimeError(Error):
    def __init__(self, start_pos, end_pos, details, context):
        super().__init__(start_pos, end_pos, 'Runtime Error', details)
        self.context = context

    def as_string(self):
        result = self.generate_traceback()
        result += f'{self.error_name}: {self.details}'
        result += '\n\n' + string_with_arrows(self.start_pos.file_text, self.start_pos, self.end_pos)
        return result

    def generate_traceback(self):
        result = ''
        pos = self.start_pos
        ctx = self.context

        while ctx:
            result= f'File {pos.filename}, line {str(pos.line + 1)}, in {ctx.display_name}\n' + result
            pos= ctx.parent_entry_pos
            ctx = ctx.parent

        return 'Traceback (most recent call last):\n' + result

class Position:
    def __init__(self, idx, line, col, filename, file_text):
        self.idx = idx
        self.line = line
        self.col = col
        self.filename = filename
        self.file_text = file_text

    def advance(self, current_char=None):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.line += 1
            self.col = 0

        return self

    def copy(self):
        return Position(self.idx, self.line, self.col, self.filename, self.file_text)

TOKEN_PLUS= 'PLUS'
TOKEN_MINUS = 'MINUS'
TOKEN_POW = 'POW'
TOKEN_MUL = 'MUL'
TOKEN_DIV = 'DIV'
TOKEN_INT = 'INT'
TOKEN_FLOAT = 'FLOAT'
TOKEN_LPAREN = 'LPAREN'
TOKEN_RPAREN ='RPAREN'
TOKEN_EOF = 'EOF'

class Token:
    def __init__(self, type_, value=None, start_pos=None, end_pos=None):
        self.type = type_
        self.value = value

        if start_pos:
            self.start_pos = start_pos.copy()
            self.end_pos = start_pos.copy()
            self.end_pos.advance()

        if end_pos:
            self.end_pos = end_pos

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'

class Lexer:
    def __init__(self, filename, text):
        self.filename = filename
        self.text = text
        self.pos = Position(-1, 0, -1, filename, text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def make_tokens(self):
        tokens = []

        while self.current_char is not None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char== '+':
                tokens.append(Token(TOKEN_PLUS, start_pos=self.pos))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TOKEN_MINUS, start_pos=self.pos))
                self.advance()
            elif self.current_char == '^':
                tokens.append(Token(TOKEN_POW, start_pos=self.pos))
                self.advance()

            elif self.current_char == '*':
                tokens.append(Token(TOKEN_MUL, start_pos=self.pos))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TOKEN_DIV, start_pos=self.pos))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TOKEN_LPAREN, start_pos=self.pos))
                self.advance()
            elif self.current_char ==')':
                tokens.append(Token(TOKEN_RPAREN, start_pos=self.pos))
                self.advance()
            else:
                start_pos = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharacterError(start_pos, self.pos, "'" + char + "'")

        tokens.append(Token(TOKEN_EOF, start_pos=self.pos))
        return tokens, None

    def make_number(self):
        num_str= ''
        dot_count =0
        start_pos =self.pos.copy()

        while self.current_char is not None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(TOKEN_INT, int(num_str), start_pos, self.pos)
        else:
            return Token(TOKEN_FLOAT, float(num_str), start_pos, self.pos)

class NumberNode:
    def __init__(self, token):
        self.token = token

        self.start_pos= self.token.start_pos
        self.end_pos= self.token.end_pos

    def __repr__(self):
        return f'{self.token}'

class BinaryOperationNode:
    def __init__(self, left_node, operator_token, right_node):
        self.left_node = left_node
        self.operator_token = operator_token
        self.right_node = right_node

        self.start_pos = self.left_node.start_pos
        self.end_pos = self.right_node.end_pos

    def __repr__(self):
        return f'({self.left_node}, {self.operator_token}, {self.right_node})'

class UnaryOperationNode:
    def __init__(self, operator_token, node):
        self.operator_token = operator_token
        self.node = node

        self.start_pos = self.operator_token.start_pos
        self.end_pos = node.end_pos

    def __repr__(self):
        return f'({self.operator_token}, {self.node})'

class ParseResult:
    def __init__(self):
        self.error =None
        self.node = None

    def register(self, res):
        if isinstance(res, ParseResult):
            if res.error: self.error = res.error
            return res.node

        return res

    def success(self, node):
        self.node= node
        return self

    def failure(self, error):
        self.error= error
        return self

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_idx = -1
        self.advance()

    def advance(self):
        self.token_idx += 1
        if self.token_idx < len(self.tokens):
            self.current_token = self.tokens[self.token_idx]
        return self.current_token

    def parse(self):
        result = self.expression()
        if not result.error and self.current_token.type != TOKEN_EOF:
            return result.failure(SyntaxError(
                self.current_token.start_pos, self.current_token.end_pos,
                "Expected '+', '-', '*' or '/'"
            ))
        return result

    def factor(self):
        result = ParseResult()
        token =self.current_token

        if token.type in (TOKEN_PLUS, TOKEN_MINUS):
            result.register(self.advance())
            factor = result.register(self.factor())
            if result.error: return result
            return result.success(UnaryOperationNode(token, factor))

        elif token.type in (TOKEN_INT, TOKEN_FLOAT):
            result.register(self.advance())
            return result.success(NumberNode(token))

        elif token.type == TOKEN_LPAREN:
            result.register(self.advance())
            expr = result.register(self.expression())
            if result.error: return result
            if self.current_token.type == TOKEN_RPAREN:
                result.register(self.advance())
                return result.success(expr)
            else:
                return result.failure(SyntaxError(
                    self.current_token.start_pos, self.current_token.end_pos,
                    "Expected ')'"
                ))

        return result.failure(SyntaxError(
            token.start_pos, token.end_pos,
            "Expected int or float"
        ))

    def term(self):
        return self.binary_operation(self.factor, (TOKEN_MUL, TOKEN_DIV))

    def expression(self):
        return self.binary_operation(self.term, (TOKEN_PLUS, TOKEN_MINUS))

    def binary_operation(self, func, operators):
        result = ParseResult()
        left = result.register(func())
        if result.error: return result

        while self.current_token.type in operators:
            operator_token = self.current_token
            result.register(self.advance())
            right = result.register(func())
            if result.error: return result
            left = BinaryOperationNode(left, operator_token, right)

        return result.success(left)

class RuntimeResult:
    def __init__(self):
        self.value = None
        self.error = None

    def register(self, res):
        if res.error: self.error = res.error
        return res.value

    def success(self, value):
        self.value = value
        return self

    def failure(self, error):
        self.error = error
        return self

class Number:
    def __init__(self, value):
        self.value = value
        self.set_pos()
        self.set_context()

    def set_pos(self, start_pos=None, end_pos=None):
        self.start_pos = start_pos
        self.end_pos = end_pos
        return self

    def set_context(self, context=None):
        self.context = context
        return self

    def add(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None

    def subtract(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None

    def multiply(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None

    def divide(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RuntimeError(
                    other.start_pos, other.end_pos,
                    'Division by zero',
                    self.context
                )

            return Number(self.value / other.value).set_context(self.context), None

    def __repr__(self):
        return str(self.value)

class Context:
    def __init__(self, display_name, parent=None, parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos

class Interpreter:
    def visit(self, node, context):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node, context):
        raise Exception(f'No visit_{type(node).__name__} method defined')

    def visit_NumberNode(self, node, context):
        return RuntimeResult().success(
            Number(node.token.value).set_context(context).set_pos(node.start_pos, node.end_pos)
        )

    def visit_BinaryOperationNode(self, node, context):
        result = RuntimeResult()
        left = result.register(self.visit(node.left_node, context))
        if result.error: return result
        right = result.register(self.visit(node.right_node, context))
        if result.error: return result

        if node.operator_token.type == TOKEN_PLUS:
            result_value, error = left.add(right)
        elif node.operator_token.type == TOKEN_MINUS:
            result_value, error = left.subtract(right)
        elif node.operator_token.type == TOKEN_MUL:
            result_value, error = left.multiply(right)
        elif node.operator_token.type == TOKEN_DIV:
            result_value, error = left.divide(right)

        if error:
            return result.failure(error)
        else:
            return result.success(result_value.set_pos(node.start_pos, node.end_pos))

    def visit_UnaryOperationNode(self, node, context):
        result = RuntimeResult()
        number = result.register(self.visit(node.node, context))
        if result.error: return result

        error = None

        if node.operator_token.type == TOKEN_MINUS:
            number, error = number.multiply(Number(-1))

        if error:
            return result.failure(error)
        else:
            return result.success(number.set_pos(node.start_pos, node.end_pos))

def run(filename, text):
    lexer = Lexer(filename, text)
    tokens, error = lexer.make_tokens()
    if error: return None, error

    # Generate AST
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error: return None, ast.error

    # Run program
    interpreter = Interpreter()
    context = Context('<program>')
    result = interpreter.visit(ast.node, context)

    return result.value, result.error
