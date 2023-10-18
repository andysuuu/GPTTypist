import re
import warnings


class ActionInfo:
    def __init__(self, action_type, index, input_content):
        self.action_type = action_type
        self.index = index
        self.input_content = input_content

def get_action_list(output: str, operated_comp_list: list):
    action_list = []
    reused_comp = []

    pattern = r'\[([^\]]+)\](?:\{(\d+)\})?(\{[^\}]+\})?[;.]'
    matches = re.findall(pattern, output)

    for match in matches:
        action_type = match[0]
        index = match[1] if match[1] else None
        input_content = match[2][1:-1] if match[2] else None

        action_info = ActionInfo(action_type, index, input_content)
        action_list.append(action_info)

    for action in action_list:
        for operated_comp in operated_comp_list:
            if action.index is not None and int(action.index) == int(operated_comp):
                reused_comp.append(action.index)

    if len(reused_comp) != 0:
        warnings.formatwarning = warning_on_one_line
        warnings.warn("\nComponent" + str(reused_comp) + " is operated but reused.", stacklevel=2)
    return action_list

def warning_on_one_line(message, category, filename, lineno, file=None, line=None):
    return '%s\n' % message
