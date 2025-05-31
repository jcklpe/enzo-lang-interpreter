from enzo.parser import parse
from enzo.exec   import eval_ast

# built-in helper
def say(val): print(val)

def main() -> None:
    print("enzo repl — ctrl-D to exit")
    while True:
        try:
            line = input("enzo> ")
        except (EOFError, KeyboardInterrupt):
            break
        if not line.strip():
            continue
        try:
            ast = parse(line)
            out = eval_ast(ast)
            if out is not None:
                print(out)
        except Exception as e:
            print("error:", e)
