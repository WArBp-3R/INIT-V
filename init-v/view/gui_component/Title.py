from .GUIComponent import GUIComponent


class Title(GUIComponent):
    DESC_POSTFIX = "title"

    def __init__(self, desc_prefix, title=""):
        super().__init__(desc_prefix, components=title)
