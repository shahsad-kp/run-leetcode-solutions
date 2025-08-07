import ast
import inspect
from typing import Callable, Optional, Any

from test_cases import TestCases
from test_value import TestValue


class BaseSolution:
    title: str
    automatic_tests: TestCases
    leetcode_link: str
    __solution_method__: str

    def get_solution_method(self) -> Callable:
        method_name = getattr(self, "__solution_method__", None)
        if not method_name:
            raise AttributeError("Meta must define 'solution_method'.")

        method = getattr(self, method_name, None)
        if not callable(method):
            raise TypeError(f"'{method_name}' is not callable.")
        return method

    def run_manual(self, inputs: Optional[list[Any]] = None, expected: Optional[Any] = None) -> None:
        method = self.get_solution_method()
        sig = inspect.signature(method)
        args = inputs or [
            ast.literal_eval(input(f"{param.name} ({param.annotation}): "))
            for param in sig.parameters.values()
        ]
        expected = expected or ast.literal_eval(input(f"({sig.return_annotation}): "))
        test_cases = TestCases(
            TestValue(
                inputs=args,
                expected=expected,
            ),
            method=method
        )
        test_cases.run()

    def run_automatic(self):
        auto_test = getattr(self, "automatic_tests", None)
        if not auto_test:
            raise ValueError("No automatic tests defined.")
        auto_test.run(self.get_solution_method())

    def __str__(self):
        return self.title

    def __repr__(self):
        title = self.title or ''
        link = self.leetcode_link
        return f"<Solution [{title} - {link}]>"
