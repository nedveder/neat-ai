import ast

import generate_tests
import generate_coding_style
from function_improvements import FunctionImprovements
from lib import dependency_graph


class ServerSide:
    @staticmethod
    def get_suggestions(code, preferences):
        """
        The function will recieve a python code string and return a list of suggestions based on the preferences
            specified.
        :param preferences: A dictionary of preferences
        :param code: python code in string format
        :return: A dictinary of suggestions, each key is a function name and the value is a list of FunctionImprovements
         objects
        """
        suggestions = dict()

        if preferences['style']:
            suggestions = generate_coding_style.get_suggestions(code, preferences['style'])

        if preferences['tests']:
            suggestions = generate_tests.get_suggestions(code, preferences['tests'])

        return suggestions

    @staticmethod
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

    def get_sources(self, code):
        """
        Gets source code and returns source codes of functions by topological sort order.
        :param code:
        :return:
        """
        functions = dependency_graph.build_topological_sort(code)
        ast_tree = ast.parse(code)
        for function_name in reversed(functions):
            function_source = self.get_function_source(code, function_name, tree=ast_tree)
            yield function_source
