import json
import subprocess
import re
import ast
import gpt_api
import backend_api
import dependency_graph
from tqdm import tqdm

TEST_PROMPTS_FILE = "prompts/test_prompts.json"
TEST_CODE_FILE = "tests.py"
MY_MODULE_FILE = "mymodule.py"


class TestResponse:
    def __init__(self, name, source_code, error=None, explanation=None):
        self.name = name
        self.source_code = source_code
        self.error = error
        self.explanation = explanation


def generate_responses(test_names, test_contents, errors):
    responses = []
    for name, content, error in zip(test_names, test_contents, errors):
        responses.append(TestResponse(name, content, error))
    return responses


def responseFromText(tests, errors):
    test_names, test_contents = extract_functions(tests)
    test_names = [function.name for function in test_names]
    errors_dict = extract_errors(errors)
    errors = [None] * len(test_names)
    for test_name, test_content in errors_dict.items():
        errors[test_names.index(test_name)] = test_content
    return generate_responses(test_names, test_contents, errors)


def extract_errors(source):
    errors = dict()
    row_pattern = "(FAIL|ERROR):[^-]*"
    function_name_pattern = "(FAIL|ERROR):(.*)\("
    for match in re.finditer(row_pattern, source):
        full_text = match.group(0)
        func_name = list(re.finditer(function_name_pattern, full_text))[0].group(2).strip()
        errors[func_name] = full_text
    return errors


def extract_functions(source_code):
    function_sources = []
    ast_tree = ast.parse(source_code)
    unit_tests_class = [item for item in ast_tree.body if type(item) == ast.ClassDef][0]
    function_names = dependency_graph.extract_functions(unit_tests_class)
    for function in function_names:
        function_source = get_function_source(source_code=source_code, tree=unit_tests_class,
                                              function_name=function.name)
        function_sources.append(function_source)
    return function_names, function_sources


def parse_base_response(response):
    pattern = "```"
    regex = re.compile(pattern)
    matches = list(regex.finditer(response))
    if len(matches) == 0:
        return response
    response = response[matches[0].end(): matches[1].start()]
    if not response.startswith("python"):
        response = response[6:]
    return response


def get_suggestions(server_side, source_code):
    """Generate tests for the python function given in source-code,
    where the documentations of the functions it depends on are listed in
    'dependencies_documentations', and are assumed to be valid and working. """

    with open(TEST_PROMPTS_FILE) as f:
        prompts = json.load(fp=f)
    with open(MY_MODULE_FILE, 'w') as f:
        f.write(source_code)

    GPT = gpt_api.GPT()
    GPT.add_system_message(prompts.get('base_prompt')[0])
    # function_codes_generator = server_side.get_sources()
    # funcResponses = []
    # for function_code in tqdm(function_codes_generator):
    #     GPT.clear_messages()
    #     response = GPT.chat(function_code)
    #     parsed_response = parse_base_response(response)
    #     with open(TEST_CODE_FILE, 'w') as tests_file:
    #         tests_file.write(parsed_response)
    #     p = subprocess.Popen(f"python3 {TEST_CODE_FILE}", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    #     _, err = p.communicate()
    #     error = err.decode('utf-8')
    #     function_response = FunctionResponse.fromText(parsed_response, error)
    #     funcResponses.append(function_response)
    funcResponse = None
    response = GPT.chat(source_code)
    parsed_response = parse_base_response(response)
    with open(TEST_CODE_FILE, 'w') as tests_file:
        tests_file.write(parsed_response)
    p = subprocess.Popen(f"python3 {TEST_CODE_FILE}", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    _, err = p.communicate()
    error = err.decode('utf-8')
    function_response = responseFromText(parsed_response, error)
    return function_response


def get_function_source(source_code, tree, function_name):
    # Get the start and end line numbers of the function definition
    function_node = None
    function_index = 0
    for index, node in enumerate(tree.body):
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            function_node = node
            function_index = index
            break
    if not function_node:
        return None

    start_line = function_node.lineno
    # Extract the lines containing the function
    lines = source_code.split('\n')

    if function_index == len(tree.body) - 1:
        function_lines = lines[start_line - 1:]
    else:
        function_lines = lines[start_line - 1: tree.body[function_index + 1].lineno - 1]
    # Join the lines back into a string
    function_source = '\n'.join(function_lines)
    return function_source


if __name__ == '__main__':
    # file = r"C:\Users\alonv\PycharmProjects\neat-ai\lib\test_code\test1.py"
    file = r"C:\Users\alonv\PycharmProjects\neat-ai\lib\test_code\test2.py"
    with open(file, 'r') as f:
        code = f.read()
    responses = get_suggestions(backend_api.ServerSide(code), code)
    print(responses)
