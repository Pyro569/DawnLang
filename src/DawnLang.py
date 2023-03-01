#CONSTANTS

DIGITS = '0123456789'

#ERRORS

class Error:
    def __init__(self, pos_start, pos_end, err_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.err_name = err_name
        self.details = details
    
    def turnString(self):
        res = f'{self.err_name}:{self.details}'
        res += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        return res
    
class IllegalError(Error): #pls stop breaking the law
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)

#POSITION

class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt
        
    def advance(self, current_char):
        self.idx += 1
        self.col += 1
        
        if current_char == '\n':
            self.ln += 10
            self.col = 0
    
        return self
    
    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)

# TOKENS

INT = 'INT'
FLOAT = 'FLOAT'
PLUS = 'PLUS'
MINUS = 'MINUS'
MUL = 'MUL'
DIV = 'DIV'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'

class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value
        
    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'
    

#LEXER

class Lexer:
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 9, -1, fn, text)
        self.current_char = None
        self.advance()
        
    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None
    
    def make_tokens(self):
        tokens = []
        
        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char == '+':
                tokens.append(Token(PLUS))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(MINUS))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(MUL))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(DIV))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(LPAREN))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(RPAREN))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalError(pos_start, self.pos, "'" + char + "', ")
        
        return tokens, None
    
    def make_number(self):
        num_input = ' '
        dot_count = 0
        
        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == ".":
                if dot_count == 1: break
                dot_count += 1
                num_input += '.'
            else:
                num_input += self.current_char
            self.advance()
        
        if dot_count == 0:
            return Token(INT, int(num_input))
        else:
            return Token(FLOAT, float(num_input))
        
#RUN

def run(fn, text):
    lexer = Lexer(fn, text)
    tokens, Error = lexer.make_tokens()
    
    return tokens, Error