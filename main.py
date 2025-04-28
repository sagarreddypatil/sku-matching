import json
from openai import OpenAI
from code_interpreter import CodeInterpreter

client = OpenAI()
interp = CodeInterpreter()
interp_stub = """
import pandas as pd
df = pd.read_csv("data/product_df.csv")
"""
interp.run_code(interp_stub)

system_prompt = open("system_prompt.txt", "r").read()
email_input = open("email_input.txt", "r").read()

inputs = [
    {
        "role": "developer",
        "content": [
            {
                "type": "input_text",
                "text": system_prompt,
            }
        ],
    },
    {
        "role": "user",
        "content": [{"type": "input_text", "text": email_input}],
    },
]

output_schema = {
    "format": {
        "type": "json_schema",
        "name": "ranked_skus_schema",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "ranked_skus": {
                    "type": "array",
                    "description": "A list of ranked SKUs. Minimum 1 item",
                    "items": {"type": "string"},
                }
            },
            "required": ["ranked_skus"],
            "additionalProperties": False,
        },
    }
}

tools = [
    {
        "type": "function",
        "name": "python_interpreter",
        "description": "Python interpreter where there exists a variable called `df`, a pandas dataframe containing the part catalog.",
        "parameters": {
            "type": "object",
            "properties": {
                "python_code": {
                    "type": "string",
                    "description": "A snippet of python code to run in the interpreter.",
                },
            },
            "additionalProperties": False,
            "required": ["python_code"],
        },
        "strict": True,
    }
]

kwargs = {
    "model": "o4-mini",
    "reasoning": {"effort": "high", "summary": "auto"},
    "text": output_schema,
    "tools": tools,
    "store": True,
}

end = False
out = None
while not end:
    response = client.responses.create(**kwargs, input=inputs)
    for output in response.output:
        inputs.append(output)

        if output.type == "reasoning":
            for item in output.summary:
                print(item.text)
        elif output.type == "function_call":
            call_id = output.call_id
            args = output.arguments
            args = json.loads(args)
            code = args["python_code"]
            res = interp.run_code(code)
            inputs.append(
                {"type": "function_call_output", "call_id": call_id, "output": res}
            )

            print("```python")
            for line in code.splitlines():
                print(f">>> {line}")
            print(res)
            print("```")
        else:
            out = json.loads(output.content[0].text)
            end = True
            break

print("final_output", out)
