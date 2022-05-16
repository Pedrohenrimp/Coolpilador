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
     | "if" expr "then" expr "else" expr "fi"
     | "while" expr "loop" expr ["pool"]
     | "{" [expr ";"]+ "}"
     | "let" ID ":" TYPE ["<-" expr] ["," ID ":" TYPE ["<-" expr]]* "in" expr
     | "case" expr "of" [ID ":" TYPE "=>" expr ";"]+ ["esac"]
     | "new" TYPE
     | "isvoid" expr
     | expr "+" expr
     | expr "-" expr
     | expr "*" expr
     | expr "/" expr
     | "~" expr
     | expr "<" expr
     | expr "<=" expr
     | expr "=" expr
     | "not" expr
     | COMMENT
     | "(" expr ")"
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
STRING : /"(| |[!-[]|[\]-\u10ffff]|\\([\\\/bfnrt]|u[0-9a-zA-Z]{4}))[^"]*"/
INTEGER : /[0-9]+/
COMMENT : /(\(\*)(\n)*(\s)*( |[!-[]|[\]-\u10ffff]|\\(["\\\/bfnrt]|u[0-9a-zA-Z]{4})|(\n)*)*(\n)*(\s)*(\*\))/ 
        | "--"/( |[!-[]|[\]-\u10ffff]|\\(["\\\/bfnrt]|u[0-9a-zA-Z]{4}))*/ 

%ignore " "+ | "\n"+ 
             | "--"/( |[!-[]|[\]-\u10ffff]|\\(["\\\/bfnrt]|u[0-9a-zA-Z]{4}))*/ 
             | COMMENT
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
 out_string((new Object2).type_name().substr(4,1)).
 out_string((isvoid self).type_name().substr(1,3));
 out_string("\\n");
 }
 };
};'''

exemple3 = '''class Main inherits IO {
 main() : SELF_TYPE {
    (let c : Complex <- (new Complex).init(1, 1) in
    {
    if c.reflect_X() = c.reflect_0()
    -- teste
    then out_string("passed\\n")
    else out_string("failed\\n")
    fi;
    if c.reflect_X().reflect_Y().equal(c.reflect_0())
    then out_string("passed\\n")
    else out_string("failed\\n")
    fi;
    }
    )
    };
};

class Complex inherits IO {
    x : Int;
    y : Int;
    init(a : Int, b : Int) : Complex {
        {
            x <- a;
            y <- b;
            self;
            }
            };
            print() : Object {
                if y = 0
                then out_int(x)
                else out_int(x).out_string("+").out_int(y).out_string("I")
                fi
                };
                reflect_0() : Complex {
                    {
                        x <- ~x;
                        y <- ~y;
                        self;
                        }
                        };
                        reflect_X() : Complex {
                            {
                                y <- ~y;
                                self;
                                }
                                };
                                reflect_Y() : Complex {
                                    {
                                        x <- ~x;
                                        self;
                                        }
                                        };
                                        equal(d : Complex) : Bool {
                                            if x = d.x_value()
                                            then
                                            if y = d.y_value()
                                            then true
                                            else false
                                            fi
                                            else false
                                            fi
                                            };
                                            x_value() : Int {
                                                x
                                                };
                                                y_value() : Int {
                                                    y
                                                    };
                                                    };'''

tree1 = grammar.parse(exemple1)
tree2 = grammar.parse(exemple2)
tree3 = grammar.parse(exemple3)

#print(tree1.pretty())
#print(tree2.pretty())
print(tree3.pretty())