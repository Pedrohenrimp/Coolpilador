from lark import Lark

grammar = Lark(r"""
start : [class ";"]+
class : "class" TYPE ["inherits" TYPE] "{" [feature ";"]* "}"
?feature : ID "(" [formal ["," formal]*] ")" ":" TYPE "{" expr "}"
        | ID ":" TYPE ["<-" expr]
formal : ID ":" TYPE
?expr : expr
     | expr ["@"TYPE] "." ID "(" [expr ["," expr]*] ")"
     | ID "(" [expr ["," expr]*] ")"
     | "if" expr "then" expr ["else"]* expr ["fi"]
     | "while" expr "loop" expr ["pool"]
     | "{" [expr ";"]+ "}"
     | "let" ID ":" TYPE ["<-" expr] ["," ID ":" TYPE ["<-" expr]]* "in" expr
     | "case" expr "of" [ID ":" TYPE "=>" expr ";"]+ ["esac"]
     | "new" TYPE
     | "(" "new" TYPE ")"
     | "isvoid" expr
     | "(" "isvoid" expr ")"
     | expr "+" expr
     | expr "-" expr
     | expr "*" expr
     | expr "/" expr
     | "~" expr
     | expr "<" expr
     | expr "<=" expr
     | expr "=" expr
     | "not" expr
     | (expr)
     | ID -> id
     | "integer"
     | "string"
     | "true" -> bool
     | "false" -> bool
     | STRING -> string
     | ID "<-" expr
     | INTEGER -> integer

ID : /[a-zA-Z_][a-zA-Z_0-9]*/
TYPE : /[A-Z_]+[a-zA-Z_0-9]*/
STRING : /"( |[!-[]|[\]-\u10ffff]|\\(["\\\/bfnrt]|u[0-9a-zA-Z]{4}))*"/
INTEGER : /[0-9]+/

%ignore " "+ | "\n"+
""")

exemple1 = '''class Main inherits IO { main(): Object {
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



exemple2 = '''class Main inherits IO {
 main() : SELF_TYPE {
 {
 out_string((new Object).type_name().substr(4,1)).
 out_string((isvoid self).type_name().substr(1,3));
 out_string("\\n");
 }
 };
};'''

tree1 = grammar.parse(exemple1)
tree2 = grammar.parse(exemple2)

print(tree1.pretty())
print(tree2.pretty())