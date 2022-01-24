from .Content import Content
from .GUIComponent import GUIComponent


class Dropdown(GUIComponent):
    DESC_POSTFIX = "dd"

    menu = None
    content = None

    def __init__(self, desc_prefix):
        super().__init__(desc_prefix)

    def get_children(self):
        component_list = [self.menu] if self.menu else []
        component_list += [self.content] if self.content else []
        self.components = [c.layout for c in component_list]
        return super().get_children()

    def set_menu(self):
        from .Menu import Menu
        self.menu = Menu(self.id)
        return self.menu

    def set_content(self):
        self.content = Content(self.id)
        return self.content
