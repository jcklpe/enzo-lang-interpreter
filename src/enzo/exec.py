def eval_ast(node):
    typ, *rest = node
    if typ == "num":
        return rest[0]
    if typ == "add":
        a, b = rest
        return eval_ast(a) + eval_ast(b)
