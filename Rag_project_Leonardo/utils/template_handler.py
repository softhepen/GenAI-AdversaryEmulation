# Loads and returns the content of a text file from the given path
def load_template(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# Replaces placeholder variables in a template string with actual values
def compile_template(template, variables):
    for key, value in variables.items():
        template = template.replace(f"{{{{{key}}}}}", value)
    return template
