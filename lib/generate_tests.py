import json
import subprocess
import re
import ast
import gpt_api
import backend_api
import dependency_graph

TEST_PROMPTS_FILE = "prompts/test_prompts.json"
TEST_CODE_FILE = "tests.py"
MY_MODULE_FILE = "mymodule.py"



class FunctionResponse:

    def __init__(self):
        self.function_names = []
        self.tests = []
        self.errors = []
        self.explanations = []

    @staticmethod
    def fromText(tests, errors):
        function_names, function_sources = FunctionResponse.__extract_functions(tests)
        function_names = [function.name for function in function_names]
        errors_dict = FunctionResponse.__extract_errors(errors)

    @staticmethod
    def __extract_errors(source):
        errors = dict()
        row_pattern = "(FAIL|ERROR):[^-]*"
        function_name_pattern = "(FAIL|ERROR):(.*)\("
        for match in re.finditer(row_pattern, source):
            full_text = match.group(0)
            func_name = list(re.finditer(function_name_pattern, full_text))[0].group(2).strip()
            errors[func_name] = full_text
        return errors

    @staticmethod
    def __extract_functions(source_code):
        function_sources = []
        ast_tree = ast.parse(source_code)
        unit_tests_class = [item for item in ast_tree.body if type(item) == ast.ClassDef][0]
        function_names = dependency_graph.extract_functions(unit_tests_class)
        for function in function_names:
            function_source = backend_api.ServerSide.get_function_source(source_code, function.name,
                                                                         tree=unit_tests_class)
            function_sources.append(function_source)
        return function_names, function_sources


def parse_base_response(response):
    pattern = "```"
    regex = re.compile(pattern)
    matches = list(regex.finditer(response))
    response = response[matches[0].end(): matches[1].start()]
    if response.startswith("python"):
        response = response[6:]
    return response


def run_tests(source_code):
    """Generate tests for the python function given in source-code,
    where the documentations of the functions it depends on are listed in
    'dependencies_documentations', and are assumed to be valid and working. """
    with open(TEST_PROMPTS_FILE) as f:
        prompts = json.load(fp=f)
    with open(MY_MODULE_FILE, 'w') as f:
        f.write(source_code)

    GPT = gpt_api.GPT()
    GPT.add_system_message(prompts.get('base_prompt')[0])
    function_codes_generator = backend_api.ServerSide.get_sources(source_code)
    funcResponses = []
    for function_code in function_codes_generator:
        GPT.clear_messages()
        response = GPT.chat(function_code)
        parsed_response = parse_base_response(response)
        with open(TEST_CODE_FILE, 'w') as tests_file:
            tests_file.write(parsed_response)
        p = subprocess.Popen(f"python3 {TEST_CODE_FILE}", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        _, err = p.communicate()
        error = err.decode('utf-8')
        function_response = FunctionResponse.fromText(parsed_response, error)
        funcResponses.append(function_response)
    return funcResponses


if __name__ == '__main__':
    file = r"C:\Users\alonv\PycharmProjects\ex8_(1)\nonogram.py"
    with open(file, 'r') as f:
        code = f.read()
    run_tests(code)
