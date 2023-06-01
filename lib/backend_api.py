import ast
from typing import Dict, List

import generate_tests
import generate_coding_style
from function_improvements import FunctionImprovements
from lib import dependency_graph


class ServerSide:
    def __init__(self, code=None):
        if code is not None:
            self.code_ = code
            self.functions_ = dependency_graph.build_topological_sort(code)
            self.ast_tree_ = ast.parse(code)

    def set_code(self, code):
        self.code_ = code
        self.functions_ = dependency_graph.build_topological_sort(code)
        self.ast_tree_ = ast.parse(code)

    def get_suggestions(self, preferences: Dict) -> Dict[str, List[FunctionImprovements]]:
        """
        The function will recieve a python code string and return a list of suggestions based on the preferences
            specified.
        :param preferences: A dictionary of preferences
        :return: A dictionary of suggestions, each key is a function name and the value is a list of FunctionImprovements
         objects
        """
        if self.code_ is None:
            raise Exception("Code is not set, please call set_code first")

        suggestions = {f: [] for f in self.functions_}
        if preferences['style']:
            style_suggestions = generate_coding_style.get_suggestions(self)
            for function_name, function_suggestions in style_suggestions.items():
                suggestions[function_name].extend(function_suggestions)

        if preferences['tests']:
            test_suggestions = generate_tests.get_suggestions(self, self.code_, preferences['tests'])
            for function_name, function_suggestions in test_suggestions.items():
                suggestions[function_name].extend(function_suggestions)

        return suggestions

    def get_function_source(self, function_name):
        # Get the start and end line numbers of the function definition
        function_node = None
        function_index = 0
        for index, node in enumerate(self.ast_tree_.body):
            if isinstance(node, ast.FunctionDef) and node.name == function_name:
                function_node = node
                function_index = index
                break
        if not function_node:
            return None

        start_line = function_node.lineno
        # Extract the lines containing the function
        lines = self.code_.split('\n')

        if function_index == len(self.ast_tree_.body) - 1:
            function_lines = lines[start_line - 1:]
        else:
            function_lines = lines[start_line - 1: self.ast_tree_.body[function_index + 1].lineno - 1]
        # Join the lines back into a string
        function_source = '\n'.join(function_lines)
        return function_source

    def get_sources(self):
        """
        Gets source code and returns source codes of functions by topological sort order.
        :return:
        """
        for function_name in reversed(self.functions_):
            function_source = self.get_function_source(function_name)
            yield function_source


if __name__ == '__main__':
    code = ""
    with open("test_code/test1.py") as f:
        code = f.read()
    server_side = ServerSide(code)
