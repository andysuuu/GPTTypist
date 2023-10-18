import xmltodict
import utils


def scan_page(u2_info):
    utils.close_soft_keyboard()
    page_source = u2_info.dump_hierarchy(compressed=True, pretty=True)
    #save_path = r"/Users/andysu/documents/monash/fit4701/"
    save_path = r"C:\Users\13261\Desktop\Y3S2\FIT4701(FYP)\测试结果"
    xml_file = open(save_path + 'hierarchy.xml', 'w', encoding='utf-8')
    xml_file.write(page_source)
    xml_file.close()

    xml_file = open(save_path + 'hierarchy.xml', 'r', encoding='utf-8')
    print('Reading hierarchy tree...')
    data_dict = xmltodict.parse(xml_file.read())

    all_components = getAllComponents(data_dict)
    return all_components


def getAllComponents(json_data: dict):
    root = json_data['hierarchy']

    queue = [root]
    result = []

    while queue:
        current_node = queue.pop(0)

        if 'node' in current_node:
            if type(current_node['node']).__name__ == 'dict' or type(current_node['node']).__name__ == 'OrderedDict':
                queue.append(current_node['node'])
            else:
                for e in current_node['node']:
                    queue.append(e)
        else:
            if ('com.android.systemui' not in current_node['@resource-id']) and (
                    'com.android.systemui' not in current_node['@package']):
                result.append(current_node)

    return result
