from IPython.core.interactiveshell import InteractiveShell
from IPython.utils.capture import capture_output

# Code to run as if it were a cell in a Jupyter notebook
code = """
a = 10
b = 20
print(a + b)
print(a + b)
print(a + b)
print(a + b)
a + b
"""

# Get the InteractiveShell instance
shell = InteractiveShell.instance()

# Capture the output
with capture_output() as captured:
    shell.run_cell(code)

# The captured output is now in captured.stdout
output = captured.stdout.strip()  # Remove any trailing newlines or spaces
print(output)