import ast

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

    def get_suggestions(self, preferences):
        """
        The function will recieve a python code string and return a list of suggestions based on the preferences
            specified.
        :param preferences: A dictionary of preferences
        :param code: python code in string format
        :return: A dictinary of suggestions, each key is a function name and the value is a list of FunctionImprovements
         objects
        """
        suggestions = {}

        if preferences['style']:
            suggestions = generate_coding_style.get_suggestions(self.code_, preferences['style'])

        if preferences['tests']:
            suggestions = generate_tests.get_suggestions(self.code_, preferences['tests'])

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
            function_source = ServerSide.get_function_source(self.code_, function_name)
            yield function_source
