import dash_html_components as html

from .Dropdown import Dropdown
from .GUIComponent import GUIComponent


class InteractElement(GUIComponent):
    DESC_POSTFIX = "ie"

    btn = None
    href = None
    dropdown = None

    def __init__(self, desc_prefix, btn_content=None, href=None, target=None, classes=None):
        super().__init__(desc_prefix, classes)
        self.set_btn(btn_content)
        self.set_href(href, target) if href else None

    def get_children(self):
        self.components = self.href if self.href else [self.btn, self.dropdown.layout if self.dropdown else None]
        return super().get_children()

    def set_btn(self, children):
        self.btn = html.Button(id=self.format_specifier("btn"), children=children)
        return self.btn

    def set_href(self, href, target=None):
        self.href = None
        self.href = html.A(href=href,
                           target=target if target else "_blank",
                           children=self.get_children())
        return self.href

    def set_dropdown(self):
        self.dropdown = Dropdown(self.id)
        return self.dropdown
