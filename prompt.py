import re
import utils


class ChinesePrompt:
    text_header = "问题: "
    text_app_name = "这是一个名为<app name>的安卓的应用程序的页面。"
    text_activity_name = "在当前页面，有一个输入组件。"
    text_label = "这一个组件的标签是'<label>'。"
    text_text = "这一个组件的提示输入是'<text>'。"
    text_context_info = "以下是在这个输入组件旁的其他组件的信息:\n<context information>"
    text_id = "这个输入组件可能的功能是'<EditText id>'. "
    text_ask = "我们应该往这个组件里面填什么信息?\n"
    horizontal_info = "在它旁边水平方向还有一个组件。"
    vertical_info = "在它旁边水平方向还有一个组件。"
    persona = "假设你是Dean, 一个资深的程序测试员并且回复高效和准确的回答。请给我一个可以填到输入框里面的例子。你的回答应该遵循格式，把结果放到[]里。还有，告诉我为什么你会给我那个答案?"


class EnglishPrompt:
    text_header = "Question: "
    text_app_name = "This is a <app name> app. "
    text_activity_name = "On its page, it has an input component. "
    text_label = "The label of this component is '<label>'. "
    text_text = "The text on this component is '<text>'. "
    text_context_info = "Below is the relevant prompt information of the input component:\n<context information>"
    text_id = "The purpose of this input component may be '<EditText id>'. "
    text_ask = "What is the hint text of this input component?\n"
    horizontal_info = "There is a component on the same horizontal line as this input component. "
    vertical_info = "There is a component on the same vertical line as this input component. "
    persona = "Pretend you are Dean, A professional software tester with many years test experience. 请给我一个可以填到输入框里面的例子。Please directly give me a valid example that I can fill it in the input text " \
              "field. Your answer should follow the format and put the result in []. Also, tell me the reason why do you give me that answer?"


def component_basic_info(json_data: dict):
    text_id = "The purpose of this component may be \"<EditText id>\". "
    text_label = "The label of this component is '<label>'. "
    text_text = "The text on this component is '<text>'. "
    text_hint = "The hint text of this component is '<hint>'. "

    if json_data['id'] == "" or json_data['id'] is None:
        text_id = ""
    else:
        edit_text_id = json_data['id'].split('/')[-1]
        edit_text_id = edit_text_id.replace('_', ' ')
        text_id = text_id.replace('<EditText id>', edit_text_id)

    if json_data['label'] == "" or json_data['label'] is None:
        text_label = ""
    else:
        label = json_data['label']
        text_label = text_label.replace('<label>', label)

    if json_data['text'] == "" or json_data['text'] is None:
        text_text = ""
    else:
        text = json_data['text']
        text_text = text_text.replace('<text>', text)

    if json_data['text-hint'] == "" or json_data['text-hint'] is None:
        text_hint = ""
    else:
        hint = json_data['text-hint']
        text_hint = text_hint.replace('<hint>', hint)

    return text_id + text_label + text_text + text_hint + '\n'


def generate_prompt(language, json_data: dict, current_num, total_num, history_content):
    app_name = json_data['app_name'].split('.')[-1]
    text_app_name = language.text_app_name.replace('<app name>', app_name)

    if json_data['label'] == "" or json_data['label'] is None:
        text_label = ""
    else:
        label = json_data['label']
        text_label = language.text_label.replace('<label>', label)

    if json_data['text'] == "" or json_data['text'] is None:
        text_text = ""
    else:
        text = json_data['text']
        text_text = language.text_text.replace('<text>', text)

    context_info = ""
    if len(json_data['same-horizon']) > 0:
        count = 0
        for e in json_data['same-horizon']:
            if not utils.isEnglish(
                    utils.turn_null_to_str(e['label']) + utils.turn_null_to_str(e['text']) + utils.turn_null_to_str(
                        e['text-hint'])):
                continue
            context_info += language.horizontal_info
            current_context_info = component_basic_info(e)
            if len(history_content) > count:
                pattern = r"'(.*?)'"
                current_context_info = re.sub(pattern, lambda match: f"'{history_content[count]}'",
                                              current_context_info)
                count += 1
                context_info += current_context_info
            else:
                context_info += component_basic_info(e)

    if len(json_data['same-vertical']) > 0:
        count = 0
        for e in json_data['same-vertical']:
            if not utils.isEnglish(
                    utils.turn_null_to_str(e['label']) + utils.turn_null_to_str(e['text']) + utils.turn_null_to_str(
                        e['text-hint'])):
                continue
            context_info += language.vertical_info
            current_context_info = component_basic_info(e)
            if len(history_content) > count:
                pattern = r"'(.*?)'"
                current_context_info = re.sub(pattern, lambda match: f"'{history_content[count]}'",
                                              current_context_info)
                count += 1
                context_info += current_context_info
            else:
                context_info += component_basic_info(e)

    if len(json_data['same-horizon']) > 0 or len(json_data['same-vertical']) > 0:
        text_context_info = language.text_context_info.replace('<context information>', context_info)
    else:
        text_context_info = ""

    if json_data['id'] == "" or json_data['id'] is None:
        text_id = ""
    else:
        edit_text_id = json_data['id'].split('/')[-1]
        edit_text_id = edit_text_id.replace('_', ' ')
        text_id = language.text_id.replace('<EditText id>', edit_text_id)

    question_info_add = "In current app page there are " + str(
        total_num) + " input components, following information is about the " + str(current_num + 1) + " component. "
    question = language.text_header + text_app_name + question_info_add + language.text_activity_name + text_label + text_text + text_context_info + text_id + language.text_ask
    final_text = question + language.persona
    return final_text
