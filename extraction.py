import os
import sys
import ast

from llmCall import llm_call


def extract_functions_and_variables(filename):
    """
    Extracts functions and variables from a Python file.

    Args:
        filename (str): Path to the Python file.

    Returns:
        dict: A dictionary containing function names as keys and function bodies as values.
        set: A set containing variable names.
    """
    functions = {}
    variables = set()

    with open(filename, 'r') as file:
        file_content = file.read()
        tree = ast.parse(file_content, filename=filename)

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                function_body = ast.get_source_segment(file_content, node)
                functions[node.name] = function_body

            elif isinstance(node, ast.Name):
                variables.add(node.id)

    return functions, variables


# def combine_functions_with_calls(functions, module_path):
#     """
#     Combines functions if one function calls another.

#     Args:
#         functions (dict): A dictionary containing function names and their bodies.

#     Returns:
#         dict: A dictionary containing all function names and their combined bodies.
#     """
#     combined_functions = {}
#     for func_name, func_body in functions.items():
#         for called_func in functions.keys():
#             if called_func in func_body and called_func != func_name:
#                 func_body = func_body + "\n" + functions[called_func]

#         combined_functions[func_name] = func_body
#         # calling llm with function body
#         #llm_call(func_body, module_path)

#     return combined_functions

def merge_all_functions(functions,module_path):
    extracted_functions=""
    for func_name, func_body in functions.items():
        extracted_functions+=func_body
        extracted_functions+="\n\n"
        
    llm_call(extracted_functions, module_path)
    

def process_file(file_path):
    """
    Processes a single Python file.

    Args:
        file_path (str): Path to the Python file.

    Returns:
        dict: A dictionary containing all function names and their bodies.
        set: A set containing all variable names.
    """
    
    functions, variables = extract_functions_and_variables(file_path)
    merged_functions = merge_all_functions(functions,file_path)
    return functions, variables


def process_directory(directory):
    """
    Processes all Python files in a directory and its subdirectories.

    Args:
        directory (str): Path to the directory.

    Returns:
        dict: A dictionary containing all function names and their combined bodies.
        set: A set containing all variable names.
    """
    all_functions = {}
    all_variables = set()

    for root, _, files in os.walk(directory):
        file_paths = [os.path.join(root, file_name) for file_name in files if file_name.endswith('.py')]
        for file_path in file_paths:
            functions, variables = process_file(file_path)
            all_functions.update(functions)
            all_variables.update(variables)

    return all_functions, all_variables


def gen_test(path):
    
    process_directory(path)
    
    # print("Functions:")
    # for function_name, function_body in functions.items():
    #     print(f"Function: {function_name}")
    #     print(f"Function Body:\n{function_body}")
    #     print("-------------------------")
