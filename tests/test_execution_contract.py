from app.services.execution_service import ExecutionService


def test_python_function_contract_uses_question_signature_without_guessing():
    assert ExecutionService.validate_function_contract(
        "def find_largest(arr):\n    return max(arr)",
        "python",
        "find_largest(arr: list[int]) -> int",
    ) is None
    message = ExecutionService.validate_function_contract(
        "def largest(arr):\n    return max(arr)",
        "python",
        "find_largest(arr: list[int]) -> int",
    )
    assert message == "Define the required function `find_largest` from the starter template."


def test_non_python_contracts_are_not_checked_as_python_functions():
    assert ExecutionService.validate_function_contract("function largest(arr) {}", "javascript", "find_largest(arr)") is None
    assert ExecutionService.validate_function_contract("public class Main {}", "java", "find_largest(arr)") is None
    assert ExecutionService.validate_function_contract("int main() {}", "cpp", "find_largest(arr)") is None
