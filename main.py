import uiautomator2 as u2
# import pprint
import time
import openai
import action
import action_list
import outer_prompt
import scan
from components import Components
# import tkinter as tk
import utils
import task
from history import History
import sys
import outputResult
from exception.exit_app_exception import ExitAppException


def getOutput(question: str):
    openai.api_key = "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"
    # start_sequence = "\nA:"
    # restart_sequence = "\n\nQ: "

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=question,
        temperature=0.3,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    return response["choices"][0].text


if __name__ == '__main__':
    print('Connect to device...')
    d = u2.connect()
    print('Device connected.')
    # Choose language
    print("\n1:English\n2:中文")
    language_selection = input()

    task = task.Task()
    history = History()
    # result_output = outputResult.OutputResult()

    # Set the test time limit
    start_time = time.time()
    time_limit = 180

    app_name = task.app_name
    # result_output.init_configuration(language_selection, app_name)

    iteration_count = 1

    while True:
        # Get tasks
        try:
            task.get_app_tasks()
        except ExitAppException:
            continue

        # Get all components and create components class
        all_components = scan.scan_page(d)
        components = Components(all_components)

        if len(components.clickable_enabled_comp) == 0:
            continue

        history_page_index = history.load_history(components.clickable_enabled_comp)
        new_history = components.combine_components(history.get_page(history_page_index))
        history.set_page(history_page_index, new_history)
        components.set_operated_variable(history.find_operated_components(history_page_index))

        # Get the final outer input text455
        available_actions = []
        if int(language_selection) == 1:
            outer_input_text = outer_prompt.generate_prompt_simplify(outer_prompt.OuterEnglishPrompt, components, history_page_index)
        else:
            outer_input_text = outer_prompt.generate_prompt_simplify(outer_prompt.OuterChinesePrompt, components, history_page_index)

        # Get the output from GPT
        output = getOutput(outer_input_text)
        print(output)

        # for i in range(len(output)):
        #     if output[i] == '[':
        #         if output[i+1] == 'T':

        # Get the next few actions to operate
        next_action_list = action_list.get_action_list(output, components.operated_components)

        # Start the action execution
        page_change = False
        resource_id_in_list = True

        for i in range(len(next_action_list)):

            if i != 0:
                all_components = scan.scan_page(d)

            next_action = next_action_list[i]
            next_component_index = next_action.index

            # First find if next action's component still existed
            if next_action.action_type == "Tap":
                resource_id, boundary = utils.find_id_bound_based_index(components.clickable_enabled_comp,
                                                                        int(next_component_index))
                if resource_id == -1:
                    resource_id_in_list = False
                    break
                page_change = utils.check_component_existed_in_all(all_components, resource_id, boundary)
                if not page_change:
                    res = utils.calculate_matched_boundary(all_components, resource_id, boundary)
                    action.tap_action(res)
                    history.mark_component_as_operated(history_page_index, int(next_action.index))
                else:
                    break

            elif next_action.action_type == "Back":
                action.back_action()
            elif next_action.action_type == "Input":
                # Scan page
                resource_id, boundary = utils.find_id_bound_based_index(components.clickable_enabled_comp,
                                                                        int(next_component_index))
                e_component = utils.find_component_based_on_id_boundary(all_components, resource_id, boundary)
                if not e_component:
                    page_change = True
                    break

                # Get the bounds and input
                res = utils.calculate_input_boundary(e_component)
                action.input_action(res, next_action.input_content)
                history.mark_component_as_operated(history_page_index, int(next_action.index))

                # e_id = e_component['@resource-id']
                # e_id = e_id.split('/')[-1]
                # print(e_id)
            elif next_action.action_type == "Scroll":
                scroll_action_type = next_action.index
                if scroll_action_type == "Up":
                    action.scroll_up_action()
                if scroll_action_type == "Down":
                    action.scroll_down_action()
            time.sleep(1)

            # result_output.write_info(iteration_count, task.activityLst, task.visitedActivityLst)
            iteration_count += 1

            # Check the time limit to exit the code
            current_time = time.time()
            if current_time - start_time > time_limit:
                # result_output.summary_info(history)
                sys.exit(0)

            try:
                task.get_app_tasks()
            except ExitAppException:
                break
