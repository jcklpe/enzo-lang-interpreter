from pathlib import Path
from lark import Lark, Transformer

_parser = Lark(
    Path(__file__).with_name("grammar.lark").read_text(),
    parser="lalr",
    start="start",
)

class AST(Transformer):
    # ── literals ─────────────────────────────────────────────
    def number(self, tok):   return ("num", int(tok[0]))
    def string(self, tok):   return ("str", tok[0][1:-1])
    def list(self, vals):    return ("list", vals)
    def var(self, tok):      return ("var", tok[0].value)

    # ── arithmetic ──────────────────────────────────────────
    def add(self, v):  return ("add", *v)
    def sub(self, v):  return ("sub", *v)
    def mul(self, v):  return ("mul", *v)
    def div(self, v):  return ("div", *v)
    def paren(self, v): return v[0]

    # ── dot-indexing (.3  .$i) ─────────────────────────────
    def index_chain(self, v):
        base, *toks = v
        if not toks:
            return base
        node = base
        for t in toks:
            if t.type == 'DOTINT':                 # '.3'
                idx = ("num", int(t[1:]))
            else:                                  # '.$i'
                idx = ("var", t[1:])               # drop '.$'
            node = ("index", node, idx)
        return node

    # ── statements / assignments ───────────────────────────
    def bind(self, v):       name, expr = v; return ("bind", name.value, expr)
    def rebind(self, v):     name, expr = v; return ("rebind", name.value, expr)
    def rebind_lr(self, v):  expr, name = v; return ("rebind", name.value, expr)
    def expr_stmt(self, v):  return ("expr", v[0])

def parse(src: str):
    return AST().transform(_parser.parse(src))
