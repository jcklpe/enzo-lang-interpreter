from pathlib import Path
from lark import Lark, Transformer

_grammar = Lark(
    Path(__file__).with_name("grammar.lark").read_text(),
    parser="lalr",
    start="start",
)

class AST(Transformer):
    def number(self, tok):
        return ("num", int(tok[0]))
    def add(self, vals):
        left, right = vals
        return ("add", left, right)

def parse(code: str):
    return AST().transform(_grammar.parse(code))
