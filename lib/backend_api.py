import generate_tests
import generate_coding_style


class ServerSide:
    def __init__(self):
        pass

    def get_suggestions(self, code, preferences):
        """
        The function will recieve a python code string and return a list of suggestions based on the preferences specified.
        :param preferences: A dictionary of preferences
        :param code: python code in string format
        :return: A list of suggestions for fixes of the code
        """
        suggestions = []

        if preferences['style']:
            suggestions += generate_coding_style.get_suggestions(code, preferences['style'])

        if preferences['tests']:
            suggestions += generate_tests.get_suggestions(code, preferences['tests'])

        return suggestions
