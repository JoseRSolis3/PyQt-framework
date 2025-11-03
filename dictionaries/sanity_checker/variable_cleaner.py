from log_util import advanced_log

def cleaner(variable):
    advanced_log("info", f"Cleaning variable: {variable}")
    result = []
    default_text = "ENTER TEXT HERE"

    if isinstance(variable, list):
        for item in variable:
            if item is None:
                advanced_log("warning", f"{item} is None, replacing with default text.")
                result.append(default_text)
                continue

            if isinstance(item, str):
                cleaned_string = item.strip().lower()
                if cleaned_string == "":
                    cleaned_string = default_text
                result.append(cleaned_string)
            elif isinstance(item, (int, float)):
                advanced_log("info", f"variable is numeric: {item}")
                result.append(item)
            else:
                advanced_log("warning", f"Unsupported type: {type(item)}, replacing with default text.")
                result.append(default_text)
        return result
    else:
        if variable is None:
                advanced_log("warning", "Variable is None, replacing with default text.")
                return default_text

        if isinstance(variable, str):
            cleaned_string = variable.strip().lower()
            if cleaned_string == "":
                cleaned_string = default_text
            return cleaned_string
        elif isinstance(variable, (int, float)):
            advanced_log("info", f"variable is numeric: {variable}")
            return variable
        else:
            advanced_log("warning", f"Unsupported type: {type(variable)}, replacing with default text.")
            return default_text

    
                