_env = {}   # simple global environment

def eval_ast(node):
    typ, *rest = node

    # ── literals & lookup ──────────────────────────
    if typ == "num":    return rest[0]
    if typ == "list":   return [eval_ast(x) for x in rest[0]]
    if typ == "var":
        name = rest[0]
        if name not in _env:
            raise NameError(f"undefined: {name}")
        return _env[name]

    # ── arithmetic ─────────────────────────────────
    if typ == "add": a, b = rest; return eval_ast(a) + eval_ast(b)
    if typ == "sub": a, b = rest; return eval_ast(a) - eval_ast(b)
    if typ == "mul": a, b = rest; return eval_ast(a) * eval_ast(b)
    if typ == "div": a, b = rest; return eval_ast(a) / eval_ast(b)

    # ── list indexing (1-based) ────────────────────
    if typ == "index":
        base, idx1 = rest
        seq = eval_ast(base)
        if not isinstance(seq, list):
            raise TypeError("indexing applies to lists")
        i = idx1 - 1   # convert to 0-based
        if i < 0 or i >= len(seq):
            raise IndexError("list index out of range")
        return seq[i]

    # ── bind / rebind ──────────────────────────────
    if typ == "bind":
        name, expr = rest
        if name in _env:
            raise NameError(f"{name} already defined")
        _env[name] = eval_ast(expr); return _env[name]

    if typ == "rebind":
        name, expr = rest
        if name not in _env:
            raise NameError(f"{name} undefined")
        _env[name] = eval_ast(expr); return _env[name]

    if typ == "expr":   return eval_ast(rest[0])

    raise ValueError(f"unknown node: {typ}")
