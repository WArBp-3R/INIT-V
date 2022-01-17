from .GUIComponent import GUIComponent
from .InteractElement import InteractElement


class Menu(GUIComponent):
    DESC_POSTFIX = "menu"

    def __getitem__(self, item):
        return self.menu_items[item]

    def __init__(self, desc_prefix):
        super().__init__(desc_prefix)
        self.menu_items: dict[str, InteractElement] = {}

    def get_children(self):
        component_list = self.menu_items.values()
        self.components = [c.layout for c in component_list]
        return super().get_children()

    def add_menu_item(self, label, btn_content=None, href=None, target=None, classes=None):
        self.menu_items[label] = InteractElement(self.format_specifier(label), btn_content, href, target, classes)
        return self.menu_items[label]
