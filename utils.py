import json
import re
import subprocess
import platform
import action


def turn_null_to_str(prop: str):
    if prop is None:
        return ''
    else:
        return prop


def isEnglish(s: str):
    s = s.replace('\u2026', '')
    return s.isascii()


def jsonToStr(jsonText):
    y = json.dumps(jsonText)
    return y


def lstJsonToStr(jsonList):
    output = ""
    for jsonText in jsonList:
        output += jsonToStr(jsonText)
    print(output)
    return output


def find_id_bound_based_index(clickable_enabled_comp: list, component_index: int):
    for comp in clickable_enabled_comp:
        if comp['@index'] == component_index:
            return comp['@resource-id'], comp['coordinate']
    return -1, -1


def check_component_existed_in_all(all_components, resource_id, boundary):
    for i in range(len(all_components)):
        if all_components[i]['@resource-id'] == resource_id and in_reasonable_bound(all_components[i]['@bounds'], boundary):
            return False
    return True


def find_component_based_on_id_boundary(all_components, resourceId, boundary):
    for i in range(len(all_components)):
        if all_components[i]['@resource-id'] == resourceId and in_reasonable_bound(all_components[i]['@bounds'], boundary):
            return all_components[i]
    return False


def calculate_matched_boundary(all_components, resource_id, boundary_in):
    res = []
    for e_component in all_components:
        if e_component['@resource-id'] == resource_id and in_reasonable_bound(e_component['@bounds'], boundary_in):
            boundary = e_component['@bounds']
            boundary = boundary.split(',')
            res.append(boundary[0].replace('[', ''))
            mid = boundary[1].split('][')
            res.append(mid[0])
            res.append(mid[1])
            res.append(boundary[2].replace(']', ''))

            # Add the tap action to the history
            # history.append(["\"Tap\" component \"" + e_component['@resource-id'] + "\" with text \"" + e_component['@text'] + "\" on it"])
            # break

    return res


# def calculate_matched_boundary(all_components, resource_id):
#     res = []
#     for e_component in all_components:
#         if e_component['@resource-id'] == resource_id:
#             boundary = e_component['@bounds']
#             boundary = boundary.split(',')
#             res.append(boundary[0].replace('[', ''))
#             mid = boundary[1].split('][')
#             res.append(mid[0])
#             res.append(mid[1])
#             res.append(boundary[2].replace(']', ''))
#             break
#
#     return res


def calculate_input_boundary(e_component):
    res = []
    bounds = e_component['@bounds']
    bounds = bounds.split(',')
    print(bounds)
    res.append(bounds[0].replace('[', ''))
    mid = bounds[1].split('][')
    res.append(mid[0])
    res.append(mid[1])
    res.append(bounds[2].replace(']', ''))
    return res


def get_next_action_list(output):
    next_action_list = []
    unfiltered_action = output.split(';')
    for i in range(len(unfiltered_action) - 1):
        if i == 0:
            j = 0
            while j < len(unfiltered_action[i]):
                if unfiltered_action[i][j] == '[':
                    break
                else:
                    j += 1
            action1 = unfiltered_action[i][j:]
            next_action_list.append(action1)
        else:
            next_action_list.append(unfiltered_action[i])
    return next_action_list

def close_soft_keyboard():
    os_version = platform.system()
    if os_version == 'Darwin':
        command = "adb shell dumpsys input_method | grep mInputShown"
    else:
        command = "adb shell dumpsys input_method | findstr mInputShown"

    # try:
    #     result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
    #     status = result.decode("utf-8").strip()
    # except subprocess.CalledProcessError as e:
    #     status = e.output.decode("utf-8").strip()

    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        status = result.decode("utf-8", errors="replace").strip()
    except subprocess.CalledProcessError as e:
        status = e.output.decode("utf-8", errors="replace").strip()
        print("Error executing command:", e)
    except UnicodeDecodeError as e:
        print("UnicodeDecodeError:", e)

    pattern = r"mInputShown=(\w+)"
    match = re.search(pattern, status)

    if match:
        mInputShown_value = match.group(1)
        if mInputShown_value == 'true':
            action.back_action()

def in_reasonable_bound(existing_comp_bounds: str, new_comp_bounds: str):
    pattern = r'\d+'
    integers = [int(match) for match in re.findall(pattern, existing_comp_bounds)]
    existing_x_1, existing_y_1, existing_x_2, existing_y_2 = integers
    integers = [int(match) for match in re.findall(pattern, new_comp_bounds)]
    new_x_1, new_y_1, new_x_2, new_y_2 = integers

    new_x_medium = (new_x_1 + new_x_2) // 2
    new_y_medium = (new_y_1 + new_y_2) // 2

    if existing_x_1 < new_x_medium < existing_x_2 and existing_y_1 < new_y_medium < existing_y_2:
        return True
    else:
        return False

def are_components_equal(new_comp, existing_comp):
    return (
        new_comp['@resource-id'] == existing_comp['@resource-id'] and
        new_comp['@content-desc'] == existing_comp['@content-desc'] and
        in_reasonable_bound(existing_comp['coordinate'], new_comp['coordinate']) and
        (new_comp['editable'] or new_comp['@text'] == existing_comp['@text'])
    )
