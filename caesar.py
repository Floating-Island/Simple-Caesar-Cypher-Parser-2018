# -----------------------------------------------------------------------------
# caesar.py
#
# Caesar Message Cipher.
# -----------------------------------------------------------------------------

#Lexer

tokens = (
    'NUMBER',
    'lower_LETTER', 'upper_LETTER',
    )

# Tokens

t_lower_LETTER = r'[a-z]'

t_upper_LETTER = r'[A-Z]'

def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Value too big to integer %d", t.value)
        t.value = 0
    return t


# ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("invalid character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# lexer creation
import ply.lex as lex
lexer = lex.lex()
import sys

#Parser

# global key and auxiliary function
key = 0

def cipherNumber(number):#Numbers need to be transformed to string and then be ciphered
    palabra = str(number)
    lista = list(palabra)
    cifrado = ''
    for l in lista:
        cifrado+= chr(  ((ord(l) + key - ord('0')) % 10) + ord('0')  )
    return cifrado

# Precedence and production rules



def p_start_message(t):
    'start : NUMBER seen_NUMBER message'#seen_NUMBER used to realize an embedded action
    t[0] = t[3]

def p_seen_NUMBER(t):
    'seen_NUMBER :'#needed to store key value before parsing the rest of the symbols
    global key
    key = t[-1]

def p_message_message(t):
    'message : message message'
    t[0] = (t[1],t[2])

def p_message_lower_letter(t):
    'message : lower_LETTER'
    t[0] = t[1]
    sys.stdout.write( chr(  ((ord(t[1])+ key - ord('a'))% 26) + ord('a')  ) )
    sys.stdout.flush()

def p_message_upper_letter(t):
    'message : upper_LETTER'
    t[0] = t[1]
    sys.stdout.write( chr(  ((ord(t[1])+ key - ord('A'))% 26) + ord('A')  ) )
    sys.stdout.flush()

def p_message_number(t):
    'message : NUMBER'
    t[0] = t[1]
    sys.stdout.write( cipherNumber(t[1]) )
    sys.stdout.flush()

def p_error(t):
    print("Syntax error at: '%s'" % t.value)



import ply.yacc as yacc
parser = yacc.yacc()

while True:
    try:
        print('\n-----\nCaesar Cipher:\n')
        s = raw_input(' Key and source text:\n') #Python 3 uses input() instead of raw_input()
    except EOFError:
        break
    print(' Ciphered text: ')
    parser.parse(s)
    print('\n-----\n')