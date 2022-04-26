import re
from pprint import pprint
from typing import NamedTuple

tokens = {
    'R_BRAC' : r'\}',
    'L_BRAC' : r'\{',
    'R_PAR' : r'\)',
    'L_PAR' : r'\(',
    'COMA' : r'\,',
    'COLON' : r'\:',
    'DOT' : r'\.',
    'SEMICOLON' : r'\;',
    'L_ARROW' : r'\<\-',
    'PLUS' : r'\+',
    'MINUS' : r'\-',
    'MUL' : r'\*',
    'DIV' : r'\/',
    'LESS' : r'\<',
    'LESS_EQUAL' : r'\<\=',
    'EQUAL' : r'\=',
    'R_WORD' : r'class|Main|main|inherits|IO|Object|let|in|String|out_string|Integer|true|false|not|new|isvoid|case|of|esac|while|loop|pool|if|then|wlaw|fi|SELF_TYPE|self',
    'STRING' : r'"( |[!-[]|[\]-\u10ffff]|\\(["\\\/bfnrt]|u[0-9a-zA-Z]{4}))*"',
    'NUMBER' : r'-?(0|[1-9][0-9]*)(\.[0-9]+)?([eE][+-][0-9]+)?',
    'SPACE' : r'\s+',
    'ID' : r'[a-zA-Z_][a-zA-Z_0-9]*'
}

PATTERN = '|'.join('(?P<%s>%s)' % pair for pair in tokens.items())
REGEX = re.compile(PATTERN)

class Token(NamedTuple):
    type: str
    value: str

def tokenize(code):
    for matchObject in REGEX.finditer(code):
        type = matchObject.lastgroup
        value = matchObject.group()
        if type =='SPACE':
            continue
        elif type in ('NUMBER', 'STRING'):
            value = eval(value)
        
        yield Token(type, value)


def lex(code):
    return list(tokenize(code))



exemplo1 = '''class Main inherits IO {\\nmain(): Object {
        let hello: String <- "Hello, ",
            name: String <- "",
            ending: String <- "!\\n"
            in {
            out_string("Please enter your name:\\n");
            name <- in_string();
            out_string(hello.concat(name.concat(ending)));
        }
    };
};'''



exemplo2 = '''class Main inherits IO {
 main() : SELF_TYPE {
 {
 out_string((new Object).type_name().substr(4,1)).
 out_string((isvoid self).type_name().substr(1,3));
 out_string("\\n");
 }
 };
};'''

pprint(lex(exemplo1))
#pprint(lex(exemplo2))