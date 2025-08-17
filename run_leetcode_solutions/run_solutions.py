import importlib.util
import os


def load_solution_class(file_number, folder = "questions"):
    file_name = os.path.join(folder, f"{file_number}.py")
    if not os.path.exists(file_name):
        raise FileNotFoundError(f"{file_name} not found in '{folder}/' directory.")

    spec = importlib.util.spec_from_file_location("solution_module", file_name)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if not hasattr(module, "Solution"):
        raise AttributeError(f"{file_name} must define a class named 'Solution'.")

    return module.Solution()


def get_method(solution):
    method_name = getattr(solution, '__solution_method__', None)
    if not method_name:
        raise Exception("__solution_method__ attribute not found in Solution class.")

    method = getattr(solution, method_name, None)
    if not callable(method):
        raise Exception(f"Method '{method_name}' not found or not callable in Solution class.")

    return method_name, method
