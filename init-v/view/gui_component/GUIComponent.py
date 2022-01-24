import dash_html_components as html


class GUIComponent:
    DESC_POSTFIX = ""

    def __getattr__(self, item):
        attr_dict = {
            "children": self.get_children,
            "id": self.get_id,
            "className": self.get_class_name,
            "layout": self.get_layout
        }
        return attr_dict[item]()

    def __init__(self, desc_prefix, classes=None, components=None):
        if components is None:
            components = []
        if classes is None:
            classes = []
        self.desc_prefix: str = desc_prefix
        self.classes = [self.DESC_POSTFIX] + classes
        self.components = components

    @staticmethod
    def format_descriptor(desc_prefix, desc_postfix, sep='_'):
        return "{}{}{}".format(desc_prefix, sep, desc_postfix)

    def format_specifier(self, postfix, sep="_"):
        return self.format_descriptor(self.id, postfix, sep)

    def get_children(self):
        return self.components

    def get_id(self):
        return self.format_descriptor(self.desc_prefix, self.DESC_POSTFIX)

    def get_class_name(self):
        return ' '.join(self.classes)

    def get_layout(self):
        return html.Div(id=self.id, className=self.className, children=self.children)
