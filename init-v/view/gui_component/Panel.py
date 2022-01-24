from .Content import Content
from .GUIComponent import GUIComponent
from .TitleBar import TitleBar


class Panel(GUIComponent):
    DESC_POSTFIX = "pnl"
    MAIN_PANEL_CLASS = "main-pnl"
    OVERLAY_CLASS = "overlay"

    titlebar = None
    content = None

    def __init__(self, desc_prefix: str, title="", is_overlay=False, is_main_panel=False, classes=None):
        super().__init__(desc_prefix, classes)
        if is_overlay:
            self.toggle_overlay()
        if is_main_panel:
            self.toggle_main_panel()
        self.set_titlebar(title)
        self.set_content()

    def get_children(self):
        component_list = [self.titlebar, self.content]
        self.components = [c.layout for c in component_list]
        return super().get_children()

    def set_titlebar(self, title=""):
        has_max_btn = False if self.is_main_panel() or self.is_overlay() else True
        has_close_btn = True if self.is_overlay() else False
        self.titlebar = TitleBar(self.id, title, has_max_btn, has_close_btn)
        return self.titlebar

    def set_content(self):
        self.content = Content(self.id)
        return self.content

    def is_overlay(self):
        return self.OVERLAY_CLASS in self.classes

    def toggle_overlay(self):
        op = self.classes.remove if self.is_overlay() else self.classes.append
        op(self.OVERLAY_CLASS)

    def is_main_panel(self):
        return self.MAIN_PANEL_CLASS in self.classes

    def toggle_main_panel(self):
        op = self.classes.remove if self.is_main_panel() else self.classes.append
        op(self.MAIN_PANEL_CLASS)

    def get_menu(self):
        return self.titlebar.menu

    def get_max_btn(self):
        return self.titlebar.max_btn

    def get_close_btn(self):
        return self.titlebar.close_btn
