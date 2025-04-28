import ast


class CodeInterpreter:
    def __init__(self):
        self._ctx = {}

    def run_code(self, python_code: str) -> str:
        parsed = ast.parse(python_code, mode="exec")
        if parsed.body and isinstance(parsed.body[-1], ast.Expr):
            *body, last = parsed.body
            mod_body = ast.Module(body=body, type_ignores=[])
            mod_last = ast.Expression(last.value)
            exec(compile(mod_body, filename="<stdin>", mode="exec"), self._ctx)
            result = eval(compile(mod_last, filename="<stdin>", mode="eval"), self._ctx)
            return repr(result)
        else:
            exec(compile(parsed, filename="<stdin>", mode="exec"), self._ctx)
            return ""


if __name__ == "__main__":
    interpreter = CodeInterpreter()
    interpreter.run_code(open("ai_function_stub.py", "r").read())
    print(interpreter.run_code("df"))
