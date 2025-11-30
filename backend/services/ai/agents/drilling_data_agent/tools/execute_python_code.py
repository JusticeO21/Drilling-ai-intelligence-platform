import pandas as pd
from typing import Any
import sys
from io import StringIO


def execute_python_safely(code: str, context: dict) -> Any:
    """
    Execute Python code in a restricted environment.

    Args:
        code: Python code string to execute
        context: Variables to make available (e.g., {'df': dataframe})

    Returns:
        The value of 'result' variable after execution
    """
    # Create restricted namespace
    safe_globals = {
        "__builtins__": {
            "len": len,
            "range": range,
            "enumerate": enumerate,
            "zip": zip,
            "map": map,
            "filter": filter,
            "sum": sum,
            "min": min,
            "max": max,
            "abs": abs,
            "round": round,
            "sorted": sorted,
            "list": list,
            "dict": dict,
            "set": set,
            "str": str,
            "int": int,
            "float": float,
            "bool": bool,
        },
        "pd": pd,
    }

    # Add context variables (like df)
    safe_locals = context.copy()

    # Capture stdout (for print statements)
    old_stdout = sys.stdout
    sys.stdout = captured_output = StringIO()

    try:
        exec(code, safe_globals, safe_locals)

        result = safe_locals.get("result", None)

        # If result is a DataFrame, limit size
        if isinstance(result, pd.DataFrame):
            if len(result) > 100:
                result = result.head(50)
            result = result.to_dict("records")

        # If result is a Series, convert to list
        elif isinstance(result, pd.Series):
            result = result.tolist()

        # If result is numpy type, convert to Python native
        elif hasattr(result, "item"):
            result = result.item()

        return result

    except Exception as e:
        raise RuntimeError(f"Code execution failed: {str(e)}")

    finally:
        sys.stdout = old_stdout


def execute_python_with_timeout(code: str, context: dict, timeout: int = 5) -> Any:
    """
    Execute code with timeout protection.
    """
    import signal

    def timeout_handler(signum, frame):
        raise TimeoutError("Code execution exceeded time limit")

    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout)

    try:
        result = execute_python_safely(code, context)
        signal.alarm(0)
        return result
    except TimeoutError:
        signal.alarm(0)
        raise RuntimeError("Execution timeout: code took too long to run")
