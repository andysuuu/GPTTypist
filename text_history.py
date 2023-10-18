import uiautomator2 as u2
import scan
from components import Components
import task
from history import History
from exception.exit_app_exception import ExitAppException

def output_txt(histories: History, page_type: str):
    output_file_path = f'/Users/andysu/Downloads/history{page_type}.txt'

    # 打开文件以写入模式
    with open(output_file_path, 'w') as file:
        # 遍历类列表，并逐行写入文件
        for each_page in histories.pages:
            for each_components in each_page:
                file.write(str(each_components) + '\n')


if __name__ == '__main__':
    print('Connect to device...')
    d = u2.connect()
    print('Device connected.')
    print(d.info)
    # Choose language
    print("\n1:English\n2:中文")
    # language_selection = input()
    language_selection = 1

    times = 0
    page = ["_empty", "_input", "_register", "_back", "_new_page"]

    task = task.Task()
    history = History()
    while True:
        # Get tasks
        try:
            task.get_app_tasks()
        except ExitAppException:
            continue

        # Get all components and create components class
        all_components = scan.scan_page(d)
        components = Components(all_components)

        history_page_index = history.load_history(components.clickable_enabled_comp)
        new_history = components.combine_components(history.get_page(history_page_index))
        history.set_page(history_page_index, new_history)
        components.set_operated_variable(history.find_operated_components(history_page_index))

        # output_txt(history, page[times])
        times += 1
