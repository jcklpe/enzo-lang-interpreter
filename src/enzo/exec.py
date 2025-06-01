from enzo.parser import parse

_env = {}          # global environment

# ── helpers ─────────────────────────────────────────
def _interp(s: str):
    """expand <expr> inside a string literal"""
    if "<" not in s:
        return s
    out, i = [], 0
    while i < len(s):
        j = s.find("<", i)
        if j == -1:
            out.append(s[i:]); break
        out.append(s[i:j])
        k = s.find(">", j + 1)
        if k == -1:
            raise ValueError("unterminated interpolation")
        expr_ast = parse(s[j+1:k].strip())
        out.append(str(eval_ast(expr_ast)))
        i = k + 1
    return "".join(out)

# ── evaluator ───────────────────────────────────────
def eval_ast(node):
    typ, *rest = node

    # literals / lookup
    if typ == "num":   return rest[0]
    if typ == "str":   return _interp(rest[0])
    if typ == "list":  return [eval_ast(el) for el in rest[0]]
    if typ == "table": return {k: eval_ast(v) for k, v in rest[0].items()}
    if typ == "var":
        name = rest[0]
        if name not in _env:
            raise NameError(f"undefined: {name}")
        return _env[name]

    # arithmetic
    if typ == "add": a, b = rest; return eval_ast(a) + eval_ast(b)
    if typ == "sub": a, b = rest; return eval_ast(a) - eval_ast(b)
    if typ == "mul": a, b = rest; return eval_ast(a) * eval_ast(b)
    if typ == "div": a, b = rest; return eval_ast(a) / eval_ast(b)

    # selectors
    if typ == "index":
        base_ast, idx_ast = rest
        seq  = eval_ast(base_ast)
        idx  = eval_ast(idx_ast)
        if not isinstance(seq, list):
            raise TypeError("index applies to lists")
        if not isinstance(idx, int):
            raise TypeError("index must be a number")
        i = idx - 1
        if i < 0 or i >= len(seq):
            raise IndexError("list index out of range")
        return seq[i]

    if typ == "attr":
        base_ast, prop = rest
        tbl = eval_ast(base_ast)
        if not isinstance(tbl, dict):
            raise TypeError("property access applies to tables")
        if prop not in tbl:
            raise KeyError(prop)
        return tbl[prop]

    # binding
    if typ == "bind":
        name, expr = rest
        if name in _env:
            raise NameError(f"{name} already defined")
        _env[name] = eval_ast(expr); return _env[name]

    if typ == "rebind":
        name, expr = rest
        _env[name] = eval_ast(expr);  return _env[name]

    if typ == "expr": return eval_ast(rest[0])

    raise ValueError(f"unknown node: {typ}")
