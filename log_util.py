import logging as log
import inspect
import os

file_name = os.path.basename(__file__)

log.basicConfig(
    level = log.DEBUG,
    format = "%(levelname)s | @ %(asctime)s %(message)s",
    datefmt = "%Y-%m-%d %H:%M:%S",
    handlers = [
        log.FileHandler("app.log"),
        log.StreamHandler()
    ]
)
def advanced_log(log_type, text):
    caller_frame = inspect.currentframe()
    if caller_frame is None or caller_frame.f_back is None:
        return # Cannot determine caller

    caller = caller_frame.f_back
    func_name = caller.f_code.co_name
    file_name = os.path.basename(caller.f_code.co_filename)
    
    cls_name = "<MODULE>" # Default value if no class is found

    # 1. Standard Method Check (Checks for 'self')
    if "self" in caller.f_locals:
        cls_name = type(caller.f_locals["self"]).__name__
    
    # 2. Static Method Check (Search the calling module's globals)
    # This works because static methods are defined within the class scope, 
    # and we can search for the function object within that scope.
    elif func_name != '<module>':
        # Search the global namespace of the calling module for the function
        calling_module_globals = caller.f_globals
        for name, obj in calling_module_globals.items():
            if inspect.isclass(obj):
                # Use getattr to see if the function is defined inside this class
                if hasattr(obj, func_name):
                    method_obj = getattr(obj, func_name)
                    # Check if the object we found is actually the function that called us
                    if inspect.isfunction(method_obj) and method_obj.__code__ == caller.f_code:
                        cls_name = obj.__name__
                        break # Found the class, stop searching

    tag = f"|{file_name}|{cls_name}|{func_name.upper()}|:"

    if log_type.lower() not in ["debug", "info", "warning", "error", "critical"]:
        raise ValueError(f"Invalid log_type: {log_type}")

    log_method = getattr(log, log_type.lower())
    log_method(f"{tag} {text}")

# You'll need to update the rest of your log_util.py file with this new function.
advanced_log("info", "TEST LOG FROM log_util.py")
