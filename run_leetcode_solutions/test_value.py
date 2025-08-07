from typing import Any, Callable


class TestValue:
    def __init__(self, inputs: list[Any], expected: Any):
        self.inputs = inputs
        self.expected = expected

    def run(self, _method: Callable) -> tuple[bool, Any]:
        output = _method(*self.inputs)
        if output != self.expected:
            return False, self.expected
        return True, output

    def __str__(self):
        return f"Test(inputs={self.inputs}, expected={self.expected})"

    def __repr__(self):
        return f"<inputs={self.inputs}, expected={self.expected}>"
