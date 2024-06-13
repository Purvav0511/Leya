from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter
import re

def format_answer(answer):
    # Regex to find all embedded Python code blocks
    code_pattern = re.compile(r"```python(.*?)```", re.DOTALL)
    # Iterate over all matches and replace them with highlighted code
    for code_match in code_pattern.finditer(answer):
        original_code = code_match.group(0)  # Full match including ```python```
        code_only = code_match.group(1).strip()  # Just the code inside the markers
        # Highlight syntax using Pygments
        highlighted_code = highlight(code_only, PythonLexer(), TerminalFormatter())
        # Replace the original code block in the answer with the highlighted version
        answer = answer.replace(original_code, highlighted_code)

    return answer