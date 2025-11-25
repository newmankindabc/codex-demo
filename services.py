import operator
from typing import Any, Callable, Dict, Tuple


def _extract_operands(data: Dict[str, Any]) -> Tuple[Any, Any]:
    """Extract operands from request payload.

    The function intentionally relies on direct key access to keep the
    behavior consistent with the original implementation, which raises
    errors when fields are missing.
    """

    return data["a"], data["b"]


def calculate(data: Dict[str, Any], op: Callable[[Any, Any], Any]) -> Dict[str, Any]:
    """Execute a binary operation using request payload fields.

    The return structure mirrors the original endpoints to maintain API
    compatibility.
    """

    a, b = _extract_operands(data)
    result = op(a, b)
    return {"code": 0, "data": result}


def add_operation(data: Dict[str, Any]) -> Dict[str, Any]:
    return calculate(data, operator.add)


def multiply_operation(data: Dict[str, Any]) -> Dict[str, Any]:
    return calculate(data, operator.mul)
