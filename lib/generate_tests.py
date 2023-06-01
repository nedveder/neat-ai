import dependency_graph
import ast
import json
import gpt_api
import subprocess

TEST_PROMPTS_FILE = "prompts/test_prompts.json"
TEST_CODE_FILE = "tests.py"
MY_MODULE_FILE = "mymodule.py"


def test_code(source_code, language='python'):
    """Generate tests for the python function given in source-code,
    where the documentations of the functions it depends on are listed in
    'dependencies_documentations', and are assumed to be valid and working. """
    GPT = gpt_api.GPT()
    function_codes_generator = get_sources(source_code)
    with open(TEST_PROMPTS_FILE) as f:
        prompt = json.load(fp=f).get('test_case')[0].replace('{LANGUAGE}', language)
        GPT.add_system_message(prompt)
    with open(MY_MODULE_FILE, 'w') as f:
        f.write(source_code)
    for function_code in function_codes_generator:
        response = GPT.chat(function_code)
        code_response = response[response.find(r"```python") + 9:response.rfind(r"```")]
        with open(TEST_CODE_FILE, 'w') as f:
            f.write(code_response)

        p = subprocess.Popen(f"python3 {TEST_CODE_FILE}", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = p.communicate()
        error = err.decode('utf-8')
        if len(error) == 0:
            print(f"Function tested successfully!")
        else:
            print(f"There were some failed tests... AI creating tests review.")
            print(error)
            response = GPT.chat(error)
            print(response)
            exit()


def get_function_source(source_code, function_name, tree=None):
    if tree is None:
        tree = ast.parse(source_code)
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


def get_sources(code):
    """
    Gets source code and returns source codes of functions by topological sort order.
    :param code:
    :return:
    """
    functions = dependency_graph.build_topological_sort(code)
    ast_tree = ast.parse(code)
    for function_name in reversed(functions):
        function_source = get_function_source(code, function_name, tree=ast_tree)
        yield function_source


if __name__ == '__main__':
    file = r"C:\Users\alonv\PycharmProjects\ex8_(1)\nonogram.py"
    with open(file, 'r') as f:
        code = f.read()
    test_code(code)
