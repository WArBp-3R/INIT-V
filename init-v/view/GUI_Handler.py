import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input

app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True


def get_input_id():
    ctx = dash.callback_context
    return ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None


class GUIHandler:
    def __init__(self):
        # import main panel creators
        from .gui_creator.ComparePanelCreator import ComparePanelCreator
        from .gui_creator.DashboardPanelCreator import DashboardPanelCreator
        from view.gui_creator.PanelCreator import PanelCreator

        dashboard_panel_creator = DashboardPanelCreator()
        compare_panel_creator = ComparePanelCreator()

        self.panel_creators = {}
        self.generate_panel_creators([dashboard_panel_creator, compare_panel_creator])
        self.default_panel_creator: PanelCreator = self.panel_creators[dashboard_panel_creator.panel.desc_prefix]

        self.url = dcc.Location(id="url")
        self.window = html.Div(id="window")

        app.layout = self.get_layout()

        app.callback(
            Output("window", "children"),
            Input("url", "pathname")
        )(self.display_page)

        app.run_server(debug=True)

    def generate_panel_creators(self, panel_creators):
        from view.gui_creator.PanelCreator import PanelCreator
        sub_panel_creators: dict[str, PanelCreator] = {}
        for pc in panel_creators:
            sub_panel_creators[pc.panel.desc_prefix] = pc
        for spc in sub_panel_creators.values():
            self.generate_panel_creators(spc.sub_panel_creators.values())
        self.panel_creators.update(sub_panel_creators)

    def get_layout(self):
        self.default_panel_creator.generate_content()
        return html.Div(id="app", children=[self.url, self.window])

    def display_page(self, path):  # callback
        path_str = str(path)[1:]
        print(path_str)  # dbg
        # print(self.panel_creators)
        if path_str in self.panel_creators:
            self.panel_creators[path_str].generate_content()
            return [self.panel_creators[path_str].panel.layout]
        else:
            self.default_panel_creator.generate_content()
            return [self.default_panel_creator.panel.layout]
