from pathlib import Path
from lark import Lark, Transformer

_parser = Lark(
    Path(__file__).with_name("grammar.lark").read_text(),
    parser="lalr",
    start="start",
)

class AST(Transformer):
    # ── literals ──────────────────────────────────
    def number(self, tok):
        return ("num", int(tok[0]))

    def string(self, tok):
        return ("str", tok[0][1:-1])          # drop quotes

    def list(self, vals):
        return ("list", vals)

    def kvpair(self, v):
        key_tok, val = v
        return (key_tok.value[1:], val)       # strip leading $

    def table(self, pairs):
        return ("table", dict(pairs))

    def var(self, tok):
        return ("var", tok[0].value)

    # ── arithmetic ───────────────────────────────
    def add(self, v):  return ("add", *v)
    def sub(self, v):  return ("sub", *v)
    def mul(self, v):  return ("mul", *v)
    def div(self, v):  return ("div", *v)
    def paren(self, v): return v[0]

    # ── selector chain (.3  .$i  .prop …) ────────
    def index_chain(self, v):
        base, *toks = v
        node = base
        for t in toks:
            if t.type == "DOTINT":          # .3
                idx = ("num", int(t[1:]))
                node = ("index", node, idx)
            elif t.type == "DOTVAR":        # .$i
                idx = ("var", t[2:])
                node = ("index", node, idx)
            else:                           # .prop
                node = ("attr", node, t[1:])
        return node

    # ── statements ───────────────────────────────
    def bind(self, v):       n, e = v; return ("bind", n.value, e)
    def rebind(self, v):     n, e = v; return ("rebind", n.value, e)
    def rebind_lr(self, v):  e, n = v; return ("rebind", n.value, e)
    def expr_stmt(self, v):  return ("expr", v[0])

def parse(src: str):
    return AST().transform(_parser.parse(src))
