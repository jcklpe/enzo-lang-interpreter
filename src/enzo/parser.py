from pathlib import Path
from lark import Lark, Transformer

_parser = Lark(
    Path(__file__).with_name("grammar.lark").read_text(),
    parser="lalr",
    start="start",
)

class AST(Transformer):
    # literals
    def number(self, tok):          return ("num", int(tok[0]))
    def var(self, tok):             return ("var", tok[0].value)

    # arithmetic
    def add(self, vals):            return ("add", *vals)
    def sub(self, vals):            return ("sub", *vals)   # ← NEW
    def paren(self, vals):          return vals[0]

    # statements
    def bind(self, vals):           name, expr = vals; return ("bind", name.value, expr)
    def rebind(self, vals):         name, expr = vals; return ("rebind", name.value, expr)
    def rebind_lr(self, vals):      expr, name = vals; return ("rebind", name.value, expr)
    def expr_stmt(self, vals):      return ("expr", vals[0])

def parse(src: str):
    return AST().transform(_parser.parse(src))
