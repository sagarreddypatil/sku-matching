import ast
import traceback

class CodeInterpreter:
    def __init__(self):
        self._ctx = {}

    def run_code(self, python_code: str) -> str:
        try:
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
        except Exception:
            return traceback.format_exc()


if __name__ == "__main__":
    interpreter = CodeInterpreter()
    print(interpreter.run_code("raise Exception('test')"))
