from typing import Dict

prompt = "Given the following code and documentation, generate a basic test for this function," \
         "that covers common cases and some edge cases." \
         "required format is json with values for each paramater in the input and output."
code = "some function."


def test_function(source_code: str, dependencies_documentations: Dict[str, str]):
    """Generate tests for the python function given in source-code,
    where the documentations of the functions it depends on are listed in
    'dependencies_documentations', and are assumed to be valid and working. """
    pass
