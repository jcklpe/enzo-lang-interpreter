_env = {}   # global environment

def eval_ast(node):
    typ, *rest = node

    # ── literals & lookup ──────────────────────────
    if typ == "num":   return rest[0]
    if typ == "str":   return rest[0]
    if typ == "list":  return [eval_ast(x) for x in rest[0]]
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
        base_ast, idx_ast = rest
        seq      = eval_ast(base_ast)
        idx_val  = eval_ast(idx_ast)
        if not isinstance(seq, list):
            raise TypeError("indexing applies to lists")
        if not isinstance(idx_val, int):
            raise TypeError("index must be a number")
        i = idx_val - 1                       # to 0-based
        if i < 0 or i >= len(seq):
            raise IndexError("list index out of range")
        return seq[i]

    # ── bind / rebind ──────────────────────────────
    if typ == "bind":
        name, expr = rest
        if name in _env:
            raise NameError(f"{name} already defined")
        _env[name] = eval_ast(expr)
        return _env[name]

    if typ == "rebind":
        name, expr = rest
        # create if missing, overwrite if present
        _env[name] = eval_ast(expr)
        return _env[name]

    if typ == "expr":
        return eval_ast(rest[0])

    raise ValueError(f"unknown node: {typ}")
