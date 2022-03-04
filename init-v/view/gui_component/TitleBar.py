from .GUIComponent import GUIComponent
from .InteractElement import InteractElement
from .Menu import Menu
from .Title import Title


class TitleBar(GUIComponent):
    DESC_POSTFIX = "titlebar"
    MIN_BTN_DESC_PREFIX = "min"
    MAX_BTN_DESC_PREFIX = "max"
    CLOSE_BTN_DESC_PREFIX = "close"

    title = None
    menu = None
    min_btn = None
    max_btn = None
    close_btn = None

    def __init__(self, desc_prefix, title="", has_min_btn=False, has_max_btn=False, has_close_btn=False):
        super().__init__(desc_prefix)
        self.title = self.set_title(title)
        self.menu = self.set_menu()
        self.min_btn = self.toggle_min_ie() if has_min_btn else None
        self.max_btn = self.toggle_max_ie() if has_max_btn else None
        self.close_btn = self.toggle_close_ie() if has_close_btn else None

    def get_children(self):
        component_list = [self.title, self.menu]
        component_list += [self.min_btn] if self.min_btn else []
        component_list += [self.max_btn] if self.max_btn else []
        component_list += [self.close_btn] if self.close_btn else []
        self.components = [c.layout for c in component_list]
        return super().get_children()

    def set_title(self, title=""):
        self.title = Title(self.id, title)
        return self.title

    def set_menu(self):
        self.menu = Menu(self.id)
        return self.menu

    def toggle_min_ie(self):
        desc_prefix = self.format_specifier(self.MIN_BTN_DESC_PREFIX)
        self.min_btn = InteractElement(desc_prefix, "_") if not self.min_btn else None
        return self.min_btn

    def toggle_max_ie(self):
        desc_prefix = self.format_specifier(self.MAX_BTN_DESC_PREFIX)
        from .Panel import Panel
        self.max_btn = InteractElement(
            desc_prefix,
            "■",
            href=self.desc_prefix.replace("_{}".format(Panel.DESC_POSTFIX), "")) if not self.max_btn else None
        return self.max_btn

    def toggle_close_ie(self):
        desc_prefix = self.format_specifier(self.CLOSE_BTN_DESC_PREFIX)
        self.close_btn = InteractElement(desc_prefix, "X") if not self.close_btn else None
        return self.close_btn
