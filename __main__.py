import argparse
import ast
import importlib.util
import os
import sys

from base_solution import BaseSolution


def load_solution_class(file_number):
    file_name = os.path.join("questions", f"{file_number}.py")
    if not os.path.exists(file_name):
        raise FileNotFoundError(f"{file_name} not found in 'questions/' directory.")

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


def parse_args():
    parser = argparse.ArgumentParser(description="Run solution interactively or with test cases.")
    parser.add_argument("--question", type=str, help="Question number (e.g., 1 for 1.py)")
    parser.add_argument("--mode", type=str, choices=["a", "m"], help="Run mode: a (auto) or m (manual)")
    parser.add_argument("--inputs", type=str, help="Manual inputs as Python list string (e.g., \"[1, 2]\")")
    return parser.parse_args()


def main():
    args = parse_args()

    question_number = args.question or input("Enter question number: ").strip()
    mode = args.mode or input("Run in (A)utomatic or (M)anual mode? ").strip().lower()
    inputs_from_cli = None

    if args.inputs:
        try:
            inputs_from_cli = ast.literal_eval(args.inputs)
            if not isinstance(inputs_from_cli, list):
                raise ValueError("Inputs must be a list.")
        except Exception as e:
            print(f"Error parsing inputs: {e}")
            sys.exit(1)

    solution: BaseSolution = load_solution_class(question_number)
    print(f"\nQuestion: {getattr(solution, 'title', 'No question description found.')}\n")

    if mode == "a":
        solution.run_automatic()
    elif mode == "m":
        solution.run_manual(inputs_from_cli)
    else:
        print("Invalid mode. Choose 'a' or 'm'.")


if __name__ == "__main__":
    main()
