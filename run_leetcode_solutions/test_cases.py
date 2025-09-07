from typing import Optional, Callable
from run_leetcode_solutions.test_value import TestValue

class TestCases:
    def __init__(self, *cases: TestValue, method: Optional[Callable] = None):
        self.cases = cases
        self._method = method

    def run(self, _method: Optional[Callable] = None) -> bool:
        if (self._method or _method) is None:
            raise ValueError("Test method not resolved")
        _method = _method or self._method
        passed = 0
        for idx, case in enumerate(self.cases, 1):
            try:
                success, output = case.run(_method)
            except Exception as e:
                print(f"💣 {idx}: {str(case)}: {str(e)}\n")
            else:
                if success:
                    passed += 1
                    print(f"✅ {idx}: {str(case)}: {output}\n")
                else:
                    print(f"❌ {idx}: {str(case)}: {output}\n")
        print(f"\n{passed}/{len(self.cases)} test case(s) passed.")
        return passed == len(self.cases)

    def __str__(self):
        return f"TestCases({len(self.cases)} cases)"

    def __repr__(self):
        return self.__str__()
