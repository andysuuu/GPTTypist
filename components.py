import utils


class Components:
    def __init__(self, all_components: list):
        # basic variables
        self.all_components = all_components
        self.edittext_comp = []
        self.clickable_comp = []
        self.enabled_comp = []
        self.disabled_comp = []
        self.app_name = "x"
        self.__set_basic_variables()

        # other variables
        self.valid_input_comp = self.__find_valid_input_comp()
        self.comp_index = 1
        self.valid_input_index = []
        self.clickable_enabled_comp = []
        self.find_enabled_clickable()
        self.operated_components = []

    # public functions
    def find_enabled_clickable(self):
        ans = []
        for e_component in self.all_components:
            if e_component in self.enabled_comp or e_component in self.clickable_comp:
                if not is_empty_comp(e_component):
                    eligible_component = {
                        '@index': self.comp_index,
                        '@text': e_component.get('@text', ''),
                        '@resource-id': e_component.get('@resource-id', ''),
                        '@content-desc': e_component.get('@content-desc', ''),
                        'coordinate': e_component.get('@bounds', ''),
                        'editable': e_component in self.edittext_comp
                    }
                    ans.append(eligible_component)
                    if e_component in self.valid_input_comp:
                        self.valid_input_index.append(self.comp_index)
                    self.comp_index += 1
        self.clickable_enabled_comp = ans

    def set_operated_variable(self, operated_variable: list):
        self.operated_components = operated_variable

    def combine_components(self, history_components: list):
        original_num = len(history_components)
        index = len(history_components) + 1
        new_components = []
        for new_comp in self.clickable_enabled_comp:
            comp_found = False
            for existing_comp in history_components:
                if utils.are_components_equal(new_comp, existing_comp):
                    comp_found = True
                    break
            if not comp_found:
                new_comp['@index'] = index
                index += 1
                new_components.append(new_comp)
        history_components.extend(new_components)
        if len(history_components) != original_num:
            print("Add " + str(len(history_components) - original_num) + " components")
        self.clickable_enabled_comp = history_components
        return history_components

    # private functions
    def __set_basic_variables(self):
        for e_component in self.all_components:
            # find components with edit_text
            if '@class' in e_component and (e_component['@class'] == 'android.widget.EditText' or e_component['@class']
                                            == 'android.widget.AutoCompleteTextView'):
                self.edittext_comp.append(e_component)
            # find components with clickable
            if '@clickable' in e_component and (e_component['@clickable'] == 'true'):
                self.clickable_comp.append(e_component)
            # find components with enabled
            if '@enabled' in e_component and e_component['@enabled'] == 'true':
                self.enabled_comp.append(e_component)
            # find components with falsely enabled
            if '@enabled' in e_component and e_component['@enabled'] == 'false':
                self.disabled_comp.append(e_component)
            # find app name
            if '@package' in e_component:
                self.app_name = e_component['@package']

    def __find_valid_input_comp(self):
        components = []
        for e_component in self.edittext_comp:
            if e_component['@content-desc'] == '':
                components.append(e_component)
        return components


def is_empty_comp(component):
    if component['@text'] == "" and component['@resource-id'] == "" and component['@content-desc'] == "":
        return True
    else:
        return False
