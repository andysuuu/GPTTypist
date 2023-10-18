from components import Components


class OuterChinesePrompt:
    # text_header = "问题: "
    # text_app_name = "这是一个名为<app name>的安卓的应用程序的页面。"
    # text_activity_name = "在当前页面，有一些输入组件。"
    # text_label = "这一个组件的标签是'<label>'。"
    # text_text = "这一个组件的提示输入是'<text>'。"
    # text_context_info = "以下是在这个输入组件旁的其他组件的信息:\n<context information>"
    # text_id = "这个输入组件可能的功能是'<EditText id>'. "
    # text_ask = "我们应该往这个组件里面填什么信息?\n"
    # horizontal_info = "在它旁边水平方向还有一个组件。"
    # vertical_info = "在它旁边水平方向还有一个组件。"
    # persona = "假设你是Dean, 一个资深的程序测试员并且回复高效和准确的回答。请给我一个可以填到输入框里面的例子。你的回答应该遵循格式，把结果放到[]里。还有，告诉我为什么你会给我那个答案?"

    text_header = "问题: "
    text_app_name = "这是一个名为<app name>的安卓的应用程序的页面。"
    text_activity_name = "在当前页面，有一些输入组件。我给你的组件格式是: {(@Index),(@text),(@resource-id),(@content-desc),(@bounds)}."
    clickable_enabled_component = "有可点击并启用的组件："
    clickable_disabled_component = "有可点击但当前禁用的组件："
    edit_text_component = "有带有提示文本的组件："
    # scroll_component = ""
    persona = "假设您是 Tom，一位拥有多年测试经验的专业软件测试人员。 "\
              "如果没有可用的组件可供您操作，您应该[Back]。"
    restriction = "额外注意，在当前页面不要使用[back]。"
    action_required = "您可以返还四种类型的操作： [Tap],[Back],[Input],[Scroll]. " \
                      "请告诉我您要对哪些 UI 组件执行的下一个操作或多个操作。 " \
                      "请严格遵守格式： 对于 [Tap] 操作使用格式 [action]{component index}; e.g.[" \
                      "Tap]{3}; 对于 [Back] 操作使用格式 [Back]; e.g. [Back]; 对于 [Input] 操作使用格式 [" \
                      "Input]{component index}{input content}; . e.g. [Input]{1}{""Iphone 11""}; 对于 [Scroll]  " \
                      "操作使用格式 [Scroll]{direction}; e.g.[Scroll]{Up}; 您应该在答案中保留方括号和大括号。 " \
                      "另外，告诉我你为什么给我这个答案以及为什么在这个特定的"\
                      "顺序？"


class OuterEnglishPrompt:
    # text_header = "Question: "
    # text_app_name = "This is a <app name> app. "
    # text_activity_name = "On current page, there are few UI components. "
    # clickable_enabled_component = "Clickable and enabled component: "
    # clickable_disabled_component = "Clickable but currently disabled component: "
    # edit_text_component = "Input component with hint text: "
    # scroll_component = ""
    # persona = "Pretend you are Zac, A professional software tester with many years test experience.Your goal is to fully testing the app."
    # action_required = "Now I need you to help me to select one action for the testing." \
    #                   "Please tell me the action you want to perform based on the given action list. " \
    #                   "ActionList: "
    # end = "Please strict follow the format [action number], e.g. [1]. Also, tell me the reason why do you give me that answer? "

    text_header = "Question: "
    text_app_name = "This is a <app name> app. "
    text_activity_name = "On current page, there are few UI components: I give you the component format:{(@Index),(@text),(@resource-id),(@content-desc),(@bounds)}."
    clickable_enabled_component = "Clickable and enabled component: "
    clickable_disabled_component = "Clickable but currently disabled component:"
    edit_text_component = "Component with hint text: "
    # scroll_component = ""
    persona = "Pretend you are Tom, A professional software tester with many years test experience. " \
              "If there is no available components for you to operate, you should [Back], otherwise select components to operate first."
    restriction = "Extra notice，please don't use [back] in current page。"
    action_required = "There are four type of actions you could perform: [Tap],[Back],[Input],[Scroll]. " \
                      "Please tell me the next action or actions you are going to perform on which UI components. " \
                      "Please strict follow the format: For [Tap] action use format [action]{component index}; e.g.[" \
                      "Tap]{3}; For [Back] action use format [Back]; e.g. [Back]; For [Input] action use format [" \
                      "Input]{component index}{input content}; . e.g. [Input]{1}{""Iphone 11""}; For [Scroll] action " \
                      "use format [Scroll]{direction}; e.g.[Scroll]{Up}; You should keep the square bracket and curly bracket in your answer. " \
                      "Also, tell me the reason why do you give me that answer and why doing in this particular " \
                      "sequence? "
    # history_actions = "Too add on, here are the previous 10 history actions you already did to the app, try not to do repetitive " \
    #                   "actions on the same UI component again. History: "
    # "Also, tell me the reason why do you give me that answer? "

    # "Please strict follow the format [action]{component index}{content}, e.g. [Input]{1}{Iphone 11},[Tap]{3} or " \
    # "[Scroll]{4}{up} or [Back]. " \


# 请给我一个可以填到输入框里面的例子。Please directly give me a valid example that I can fill it in the input text " \
#               "field. Your answer should follow the format and put the result in [].


def generate_prompt(language, app_name, no_hint_text, clickable_enabled_C, clickable_disabled_C):
    action_count = 1

    text_app_name = language.text_app_name.replace('<app name>', app_name)
    tap_actions = []
    for tap_action in clickable_enabled_C:
        tap_action_des = ""
        if tap_action['@text'] != '':
            tap_action_des = "Action [" + str(action_count) + "]: [Tap] the button have resource id{" + tap_action[
                '@resource-id'] + "} with button text (" + tap_action['@text'] + ") and in component class(" + \
                             tap_action['@class'] + ") \n"
        else:
            tap_action_des = "Action [" + str(action_count) + "]: [Tap] the button have resource id{" + tap_action[
                '@resource-id'] + "} and in component class(" + tap_action['@class'] + ") \n "
        action_count += 1
        tap_actions.append(tap_action_des)

    input_actions = []
    for input_action in no_hint_text:
        if input_action['@text'] != '':
            input_action_des = "Action [" + str(
                action_count) + "]: [Input] some text into the component field have resource id{" + input_action[
                                   '@resource-id'] + "} with button text (" + input_action[
                                   '@text'] + ") and in component class(" + input_action['@class'] + ") \n"
        else:
            input_action_des = "Action [" + str(
                action_count) + "]: [Input] some text into the component field have resource id{" + input_action[
                                   '@resource-id'] + "} and in component class(" + input_action['@class'] + ") \n"
        action_count += 1
        input_actions.append(input_action_des)

    back_action = "Action [" + str(action_count) + "]: [Back] to the previous page of the application. \n"
    input_actions.append(back_action)

    all_action_list = tap_actions + input_actions
    question = language.text_header + text_app_name + language.text_activity_name + language.persona + language.action_required + str(
        tap_actions) + str(input_actions) + language.end

    # question = language.text_header + text_app_name + language.text_activity_name + language.clickable_enabled_component + "("+ clickable_enabled_C + ")" +\
    #            language.clickable_disabled_component + "(" + clickable_disabled_C+ ")"+ language.edit_text_component +"(" + no_hint_text + ")" +\
    #            language.persona + language.action_required
    return all_action_list, question


def find_editable(components: Components, language):
    editable_index = []
    for component in components.clickable_enabled_comp:
        if component['editable'] and int(component['@index']) not in components.operated_components:
            editable_index.append(component['@index'])
    if language is OuterEnglishPrompt:
        if len(editable_index) > 0:
            return ". Notice. only @index" + str(
                editable_index) + " are available to use [Input] action. You can use other actions " \
                                  "for other components. "
        else:
            return ". Notice, you cannot use [Input] action. You only can use [Tap], [Scroll], [Back]. "
    elif language is OuterChinesePrompt:
        if len(editable_index) > 0:
            return "。 注意，只有@index 等于" + str(
                editable_index) + " 的组件可以被进行 [Input] 的指令. 你可以对其他的组件进行除了[Input]指令之外的操作。"
        else:
            return "。 注意, 你不可以使用[Input]指令. 你只可以使用[Tap], [Scroll], [Back]。 "


def find_operated_variable(operated_variable: list, language):
    if len(operated_variable) > 0:
        if language is OuterEnglishPrompt:
            return "Notice, you cannot use components with @index " + str(operated_variable) + ". "
        elif language is OuterChinesePrompt:
            return "注意, 你不可以使用 @index 为" + str(operated_variable) + "的组件。 "
    else:
        return ""


def convert_component_string(component_list: list):
    formatted_strings = []

    # 遍历列表中的字典
    for item in component_list:
        cleaned_dict = {key: value for key, value in item.items() if key != 'editable'}

        formatted_string = '{' + ", ".join([f"({value})" for key, value in cleaned_dict.items()]) + '}'
        formatted_strings.append(formatted_string)

    result_string = ', '.join(formatted_strings)
    return str(result_string)


def generate_prompt_simplify(language, components: Components, history_page_index):
    # historyAc_copy = historyAc.copy()
    text_app_name = language.text_app_name.replace('<app name>', components.app_name)
    question = None
    if history_page_index == 0:
        question = language.text_header + text_app_name + language.text_activity_name + \
                   find_operated_variable(components.operated_components, language) + \
                   convert_component_string(components.clickable_enabled_comp) + "\n" + \
                   language.edit_text_component + "(" + language.persona + language.restriction + language.action_required + find_editable(components,language)
    else:
        question = language.text_header + text_app_name + language.text_activity_name + \
                   find_operated_variable(components.operated_components, language) + \
                   convert_component_string(components.clickable_enabled_comp) + "\n" + \
                   language.edit_text_component + "(" + language.persona + language.action_required + find_editable(components,language)
    return question
