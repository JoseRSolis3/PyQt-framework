from typing import Any
from log_util import advanced_log

class_name = lambda var: var.__class__.__name__

class Check():
    @staticmethod
    def none(*args):
        for arg in args:
            if arg is None:
                advanced_log("warning",f"{arg} is None.")
                raise ValueError(f"Error: {arg} is None.")
        return True
    
    @staticmethod
    def Number(*args: int | float | None, decimal = False, exception = False):
        for arg in args:
            if decimal == True:
                if not isinstance(arg, (int, float)):
                    advanced_log("warning",f"Number is not a string nor a float.")
                    if exception:
                        return None
                    raise ValueError("Number is not a string nor a float.")
            else:
                if not isinstance(arg, int):
                    advanced_log("warning",f"Number is not a string nor a float.")
                    raise ValueError("Number is not a string nor a float.")
        if exception:
            return None
        return True

    @staticmethod
    def String(*args: str | None, exception: bool = False):
        """
            Validate that all arguments are non-empty strings.
            Args:
                *args: Strings to validate (or None if exception=True).
                exception: If True, return None instead of raising for invalid input.
            Returns:
                True if all args are valid strings, None if exception=True and invalid.
        """
        for arg in args:
            if not isinstance(arg, str) or arg.strip() == "":
                advanced_log("warning",f"{arg} is not a string.")
                if exception:
                    return None
                raise ValueError(f"{arg} is not a string.")
        return True
    
    @staticmethod
    def Dictionary(*args: dict):
        for arg in args:
            if not isinstance(arg, dict):
                advanced_log("warning",f"{arg} is not a dictionary.")
                raise ValueError(f"{arg} is not a dictionary.")
        return True

    @staticmethod
    def List(*args: list):
        for arg in args:
            if not isinstance(arg, list):
                advanced_log("warning",f"{arg} is not a list.")
                raise ValueError(f"{arg} is not a list.")
        return True
    
    @staticmethod
    def Tuple(*args: tuple):
        for arg in args:
            if not isinstance(arg, tuple):
                advanced_log("warning",f"{arg} is not a tuple.")
                raise ValueError(f"{arg} is not a tuple.")
        return True