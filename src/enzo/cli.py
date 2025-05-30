from enzo.parser import parse
from enzo.exec    import eval_ast

def main() -> None:
    while True:
        try:
            line = input("enzo> ")
        except (EOFError, KeyboardInterrupt):
            break
        if not line.strip():
            continue
        try:
            ast = parse(line)
            print(eval_ast(ast))
        except Exception as e:
            print("error:", e)
