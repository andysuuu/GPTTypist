import utils


class History:
    def __init__(self):
        self.pages = []
        self.operated_components = []

    def load_history(self, new_page: list):
        similar_page_index = self.find_similar_page(new_page)
        if similar_page_index is not None:
            print("Page found with index " + str(similar_page_index))
            return similar_page_index  # 返回相似页面的索引
        else:
            self.pages.append(new_page)
            print("New page created")
            return len(self.pages) - 1  # 返回新页面的索引

    def find_similar_page(self, new_page: list, threshold=0.8):
        page_index = None
        max_similarity = 0.0
        for index, history_page in enumerate(self.pages):
            found_comp = 0
            for new_page_comp in new_page:
                for history_page_comp in history_page:
                    if utils.are_components_equal(new_page_comp, history_page_comp):
                        found_comp += 1
                        break
            if len(history_page) != 0:
                similarity = found_comp / len(history_page)
            else:
                similarity = 0
            if similarity >= threshold and similarity > max_similarity:
                max_similarity = similarity
                page_index = index
        return page_index

    def mark_component_as_operated(self, page_index: int, component_index: int):
        # 标记组件为已经操作过，避免重复标记
        for entry in self.operated_components:
            if entry['page_index'] == page_index:
                if component_index not in entry['operated_components']:
                    entry['operated_components'].append(component_index)
                return
        # 如果页面索引不存在，创建一个新的条目
        self.operated_components.append({'page_index': page_index, 'operated_components': [component_index]})

    def is_component_operated(self, page_index, component_index):
        # 检查组件是否已经操作过
        for entry in self.operated_components:
            if entry['page_index'] == page_index and component_index in entry['operated_components']:
                return True
        return False

    def find_operated_components(self, page_index: int):
        operated_components = []
        if page_index < len(self.pages):
            page_components = self.pages[page_index]
            for i, component in enumerate(page_components):
                if self.is_component_operated(page_index, i + 1):
                    operated_components.append(component['@index'])
        return operated_components

    def set_page(self, page_index: int, new_page):
        self.pages[page_index] = new_page

    def get_page(self, page_index: int):
        return self.pages[page_index]
