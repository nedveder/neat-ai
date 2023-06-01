import json
import re

import gpt_api
from function_improvements import FunctionImprovements
STYLE_PROMPTS_FILE = "prompts/style_prompts.json"


def parse_base_response(response):
    pattern = "```"
    regex = re.compile(pattern)
    matches = list(regex.finditer(response))
    code = response[matches[0].end(): matches[1].start()]
    if response.startswith("python"):
        code = code[6:]
    return code, response[matches[1].end():]


def get_suggestions(server_side):
    with open(STYLE_PROMPTS_FILE) as f:
        prompts = json.load(fp=f)
    GPT = gpt_api.GPT()
    GPT.add_system_message(prompts.get('base_prompt')[0])

    suggestions = {f: [] for f in server_side.functions_}
    for func in suggestions.keys():
        GPT.clear_messages()
        old_code = server_side.get_function_source(func)
        response = GPT.chat(server_side.get_function_source(func))
        new_code, explanation = parse_base_response(response)
        suggestions[func] = FunctionImprovements(old_code, new_code, explanation)
    return suggestions
