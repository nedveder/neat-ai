import ast
import networkx as nx
import matplotlib.pyplot as plt


def extract_functions(node):
    """
    Extracts all function definitions from an AST node.
    """
    functions = []
    for body_item in node.body:
        if isinstance(body_item, ast.FunctionDef):
            functions.append(body_item)
    return functions


def extract_function_calls(node):
    """
    Extracts all function calls from an AST node.
    """
    function_calls = []
    if isinstance(node, ast.Call):
        if isinstance(node.func, ast.Name):
            function_calls.append(node.func.id)
    for child_node in ast.iter_child_nodes(node):
        function_calls.extend(extract_function_calls(child_node))
    return function_calls


def build_dependency_graph(functions):
    """
    Builds a dependency graph of functions in a Python code file.
    """
    graph = nx.DiGraph()
    for function in functions:
        function_name = function.name
        graph.add_node(function_name)
        function_calls = extract_function_calls(function)
        for called_function in function_calls:
            if function_name == called_function:
                continue
            if called_function not in functions:
                continue
            graph.add_edge(function_name, called_function)
    return graph


def draw_dependency_graph(graph):
    """
    Draws the dependency graph using NetworkX and Matplotlib.
    """
    pos = nx.spring_layout(graph)
    nx.draw_networkx(graph, pos, with_labels=True, node_size=1000, node_color='lightblue', edge_color='gray',
                     arrowsize=20)
    plt.title("Function Dependency Graph")
    plt.axis('off')
    plt.show()


def build_topological_sort(source_code):
    """Returns a list of functions sorted topologically"""
    ast_tree = ast.parse(source_code)
    functions = extract_functions(ast_tree)
    graph = build_dependency_graph(functions)
    sorted_functions = list(nx.topological_sort(graph))
    return sorted_functions


if __name__ == '__main__':
    file = r"C:\Users\alonv\PycharmProjects\ex8_(1)\nonogram.py"
    with open(file, 'r') as f:
        code = f.read()
    print(build_topological_sort(code))
