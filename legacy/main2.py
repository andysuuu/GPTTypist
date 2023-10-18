# import uiautomator2 as u2
# import pprint
# import time
# import openai
# import action
# import outer_prompt
# import prompt
# import scan
# import tkinter as tk
# import utils

#
# def get_basic_info(e_component: dict):
#     key_list = ['id', 'text', 'label', 'text-hint', 'app_name']
#     key_at_list = ['resource-id', 'text', 'label', 'content-desc', 'package']
#     dict_info = {}
#
#     for i in range(len(key_list)):
#         dict_info[key_list[i]] = None
#         for e_property in e_component:
#             if key_at_list[i] in e_property.lower():
#                 dict_info[key_list[i]] = e_component[e_property]
#                 break
#
#     return dict_info
#
#
# def chooseFromPos(all_components: list, bounds: list):
#     same_horizon_components = []
#     same_vertical_components = []
#
#     for e_component in all_components:
#         e_bounds = e_component['@bounds']
#         if e_bounds == bounds:
#             continue
#         if (e_bounds[1], e_bounds[3]) == (bounds[1], bounds[3]):
#             same_horizon_components.append(e_component)
#         if (e_bounds[0], e_bounds[2]) == (bounds[0], bounds[2]):
#             same_vertical_components.append(e_component)
#
#     return same_horizon_components, same_vertical_components
#
#
# def getOutput(question: str):
#     openai.api_key = "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"
#     # start_sequence = "\nA:"
#     # restart_sequence = "\n\nQ: "
#
#     response = openai.Completion.create(
#         model="text-davinci-003",
#         prompt=question,
#         temperature=0.3,
#         max_tokens=2000,
#         top_p=1,
#         frequency_penalty=0,
#         presence_penalty=0,
#     )
#
#     return response["choices"][0].text
#
#
# def based_on_all_information_perform_action(input_history: str):
#     pass
#
#
# def add_history_content(the_history_content, the_dict_info):
#     if dict_info['text'] != '':
#         the_history_content.append(the_dict_info['text'])
#     elif dict_info['id'] != '':
#         the_history_content.append(the_dict_info['id'])
#     return the_history_content


# if __name__ == '__main__':
#     print('Connect to device...')
#     d = u2.connect()
#     print('Device connected.')
#     print(d.info)
#     # Choose language
#     print("\n1:English\n2:中文")
#     language_selection = input()
#
#     while True:
#         # Store history
#         history_content = []
#
#         # Outer loop
#
#         # Get 3 types of components
#         components_index = 1  # Set the index of each components for question
#         no_hint_text, all_components = scan.scan_page(d)
#
#         # The reference list of the index and resource-id of each component
#         all_interact_components_list_r = []
#
#         clickable_enabled_simplify_C, edited_index = utils.find_enabled_clickable_simplify(all_components, components_index,
#                                                                              all_interact_components_list_r)
#         components_index += len(clickable_enabled_simplify_C)  # update the index of components
#
#         clickable_disabled_simplify_C = utils.find_disabled_clickable_simplify(all_components, components_index,
#                                                                                all_interact_components_list_r)
#         components_index += len(clickable_disabled_simplify_C)  # update the index of components
#
#         print(clickable_enabled_simplify_C)
#         print(clickable_disabled_simplify_C)
#
#         # clickable_enabled_C = utils.find_enabled_clickable(all_components)
#         # clickable_disabled_C = utils.find_disabled_clickable(all_components)
#         # print(clickable_enabled_C)
#         # print(clickable_disabled_C)
#         print(all_components)
#         # print(str(all_components))
#
#         # Get the app_name for outer prompt
#         app_name = "x"
#         for e_component in all_components:
#             if '@package' in e_component:
#                 app_name = e_component['@package']
#                 break
#         # print(app_name)
#         # app_name = json_data['app_name'].split('.')[-1]
#
#         # Get the final outer input text455
#         outer_input_text = ""
#         available_actions = []
#         if int(language_selection) == 1:
#             outer_input_text = outer_prompt.generate_prompt_simplify(outer_prompt.OuterEnglishPrompt,
#                                                                      app_name, no_hint_text,
#                                                                      clickable_enabled_simplify_C,
#                                                                      clickable_disabled_simplify_C, edited_index)
#         else:
#             outer_input_text = outer_prompt.generate_prompt_simplify(outer_prompt.OuterChinesePrompt, app_name,
#                                                                      all_components,
#                                                                      clickable_enabled_simplify_C,
#                                                                      clickable_disabled_simplify_C)
#         # print(outer_input_text)
#
#         # Get the output from GPT
#         output = getOutput(outer_input_text)
#         print(output)
#
#         # for i in range(len(output)):
#         #     if output[i] == '[':
#         #         if output[i+1] == 'T':
#
#         # Get the next few actions to operate
#         next_action_list = []
#         action_num = len(output.split(';'))
#         unfiltered_action = output.split(';')
#         print(str(action_num))
#         for i in range(action_num - 1):
#             if i == 0:
#                 j = 0
#                 while j < len(unfiltered_action[i]):
#                     if unfiltered_action[i][j] == '[':
#                         break
#                     else:
#                         j += 1
#                 action1 = unfiltered_action[i][j:]
#                 next_action_list.append(action1)
#             else:
#                 next_action_list.append(unfiltered_action[i])
#         print(next_action_list)
#         print("\n\n\n")
#         # print(output.split('[')[0])
#         # next_action = available_actions[int(output.split("[")[1].split("]")[0]) - 1]
#
#         # Start the action execution
#         page_change = False
#         resource_id_in_list = True
#
#         for i in range(len(next_action_list)):
#             if i != 0:
#                 no_hint_text, all_components = scan.scan_page(d)
#
#             next_action = next_action_list[i]
#             next_component_index = next_action.split("{")[1].split("}")[0]
#
#             # First find if next action's component still existed
#             if "Tap" in next_action:
#                 next_component_index = next_action.split("{")[1].split("}")[0]
#                 resource_id, boundary = utils.find_id_bound_based_index(all_interact_components_list_r,
#                                                                 int(next_component_index))
#                 if resource_id == -1:
#                     resource_id_in_list = False
#                     break
#                 page_change = utils.check_component_exsited_in_all(all_components, resource_id, boundary)
#                 if not page_change:
#                     res = utils.calculate_matched_boundary(all_components, resource_id, boundary)
#                     action.tap_action(res)
#                 else:
#                     break
#
#             elif "Back" in next_action:
#                 action.back_action()
#             elif "Input" in next_action:
#                 # Scan page
#                 resource_id, boundary = utils.find_id_bound_based_index(all_interact_components_list_r,
#                                                                         int(next_component_index))
#                 e_component = utils.find_component_based_on_id_boundary(all_components, resource_id, boundary)
#                 if e_component == False:
#                     page_change = True
#                     break
#                 dict_info = get_basic_info(e_component)
#
#                 real_ans = next_action.split("{")[2].split("}")[0]
#                 # Get the bounds and input
#                 res = utils.calculate_input_boundary(e_component)
#                 action.input_action(res, real_ans)
#
#                 # Store the history
#                 history_content = add_history_content(history_content, dict_info)
#
#                 # e_id = e_component['@resource-id']
#                 # e_id = e_id.split('/')[-1]
#                 # print(e_id)
#             elif "Scroll" in next_action:
#                 pass
#             time.sleep(1)

            # if "Tap" in next_action:
            #     resource_id = next_action.split("{")[1].split("}")[0]
            #     res = utils.calculate_matched_boundary(all_components, resource_id)
            #     action.tap_action(res)
            # elif "Back" in next_action:
            #     action.back_action()
            # elif "Input" in next_action:
            #     for i in range(10):
            #         # Scan page
            #         no_hint_text, all_components = scan.scan_page(d)
            #
            #         # Get total number that can be inputted
            #         total_num = len(no_hint_text)
            #
            #         # Extract one input field
            #         try:
            #             e_component = no_hint_text[i]
            #         except IndexError:
            #             break
            #
            #         # for e_component in no_hint_text:
            #         print('---------------')
            #         # pprint.pprint(e_component)
            #         print('---------------')
            #         # Get the bounds
            #         bounds = e_component['@bounds']
            #         dict_info = get_basic_info(e_component)
            #
            #         # Get the components in the same horizontal and vertical area
            #         (same_horizon_components, same_vertical_components) = chooseFromPos(all_components, bounds)
            #         dict_info['same-horizon'] = []
            #         dict_info['same-vertical'] = []
            #         for e_hor_component in same_horizon_components:
            #             dict_info['same-horizon'].append(get_basic_info(e_hor_component))
            #         for e_ver_component in same_vertical_components:
            #             dict_info['same-vertical'].append(get_basic_info(e_ver_component))
            #         dict_info['activity_name'] = ''
            #         # pprint.pprint(dict_info)
            #
            #         # Get the prompt
            #         final_text = ""
            #         if int(language_selection) == 1:
            #             final_text = prompt.generate_prompt(prompt.EnglishPrompt, dict_info, i, total_num,
            #                                                 history_content)
            #         else:
            #             final_text = prompt.generate_prompt(prompt.ChinesePrompt, dict_info, i, total_num,
            #                                                 history_content)
            #         print(final_text)
            #
            #         # Get the answer from ChatGPT
            #         output = getOutput(final_text)
            #         print(output)
            #         if len(output.split("[")) == 2:
            #             real_ans = output.split("[")[1]
            #             if len(output.split("]")) == 2:
            #                 real_ans = real_ans.split("]")[0]
            #         else:
            #             exit(1)
            #         print('We think you should use (' + real_ans + ') as hint text.')
            #
            #         # Get the bounds and input
            #         res = utils.calculate_input_boundary(e_component)
            #         action.input_action(res, real_ans)
            #
            #         # Store the history
            #         history_content = add_history_content(history_content, dict_info)
            #
            #         e_id = e_component['@resource-id']
            #         e_id = e_id.split('/')[-1]
            #         print(e_id)
            #         # insert_code(e_id, real_ans, f_path)
            #         # Based on all the input field, doing next step
            #         if i == total_num - 1:
            #             print("Do sth")
            # time.sleep(1)
