import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input

from view.ViewInterface import ViewInterface


def get_input_id():
    ctx = dash.callback_context
    return ctx.triggered[0]['prop_id'].split('.')[0] if ctx.triggered else None


def get_input_parameter():
    ctx = dash.callback_context
    return ctx.triggered[0]['prop_id'].split('.')[1] if ctx.triggered else None


class GUIHandler:
    def __init__(self, interface: ViewInterface):
        self.app = dash.Dash(__name__)
        self.app.config.suppress_callback_exceptions = True
        self.interface = interface

        from view.callback_manager.CallbackManager import CallbackManager
        self.cb_mgr = CallbackManager(self)

        # import main panel creators
        from .gui_creator.ComparePanelCreator import ComparePanelCreator
        from .gui_creator.DashboardPanelCreator import DashboardPanelCreator
        from view.gui_creator.PanelCreator import PanelCreator

        dashboard_panel_creator = DashboardPanelCreator(self)
        compare_panel_creator = ComparePanelCreator(self)

        self.panel_creators = {}
        self.generate_panel_creators([dashboard_panel_creator, compare_panel_creator])
        self.default_panel_creator: PanelCreator = self.panel_creators[dashboard_panel_creator.panel.desc_prefix]

        self.url = dcc.Location(id="url")
        self.window = html.Div(id="window")

        self.app.layout = self.get_layout()

        self.app.callback(
            Output("window", "children"),
            Input("url", "pathname")
        )(self.display_page)

        # self.callback_manager.register_callback(
        #     self.display_page,
        #     [Output("window", "children")],
        #     Input("url", "pathname"),
        #     default_outputs=[self.default_panel_creator.panel.layout]
        # )

        self.cb_mgr.finalize_callbacks()

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
        if path_str in self.panel_creators:
            self.panel_creators[path_str].generate_content()
            return [self.panel_creators[path_str].panel.layout]
        else:
            self.default_panel_creator.generate_content()
            return [self.default_panel_creator.panel.layout]

    def run_app(self):
        print("--------------------------------")
        print("| DASH APP NOW RUNNING...")
        print("--------------------------------")
        self.app.run_server(debug=True)

    # aux functions
    def register_overlay_callback(self, overlay_pc, open_button):
        overlay_panel = overlay_pc.panel
        self.cb_mgr.register_multiple_callbacks(
            [Output(overlay_panel.id, "style")], {
                Input(open_button.id, "n_clicks"): (lambda x: [{"display": "flex"}], None),
                Input(overlay_panel.get_close_btn().id, "n_clicks"): (lambda x: [{"display": "none"}], None),
            },
            [{}]
        )
