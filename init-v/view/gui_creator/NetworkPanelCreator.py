import dash_core_components as dcc
import dash_cytoscape as cyto
from dash.dependencies import Output, Input

from .PanelCreator import PanelCreator
from ..GUI_Handler import app, get_input_id


class NetworkPanelCreator(PanelCreator):
    TITLE = "Network"

    def __init__(self, handler, desc_prefix="network"):
        super().__init__(handler, desc_prefix)
        self.topology_graph = None
        self.active_protocols = None

        self.define_callbacks()

    def define_callbacks(self):
        app.callback(
            Output(self.panel.format_specifier("active_protocols"), "options"),
            Output(self.panel.get_menu()["protocols"].dropdown.id, "style"),
            Input(self.panel.get_menu()["protocols"].btn.id, "n_clicks"),
        )(self.update_protocols)

    def generate_menu(self):
        net_menu = self.panel.get_menu()
        protocols = net_menu.add_menu_item("protocols", "Protocols").set_dropdown()
        protocols.set_content()
        protocols.style = {"display": "none"}

    def generate_content(self):
        content = self.panel.content

        # TODO - simultaneously define network graph with more detail and replace stub
        self.topology_graph = cyto.Cytoscape(
            id="topology-graph",
            layout={'name': 'preset'},
            style={},
            elements=[
                {'data': {'id': 'one', 'label': 'Node 1'}, 'position': {'x': 75, 'y': 75}},
                {'data': {'id': 'two', 'label': 'Node 2'}, 'position': {'x': 200, 'y': 200}},
                {'data': {'source': 'one', 'target': 'two'}}
            ]
        )
        content.components = [self.topology_graph]

        self.active_protocols = dcc.Checklist(id=self.panel.format_specifier("active_protocols"))

        protocol_list_content = self.panel.get_menu()["protocols"].dropdown.set_content()
        protocol_list_content.components = [self.active_protocols]

    # TODO - replace stub (WIP)
    def update_protocols(self, btn):
        button_id = get_input_id()
        print("update_protocols")
        # view adapter stuff
        protocol_options = [{"label": "protocol placeholder1", "value": "P"},
                            {"label": "TCP", "value": "TCP"},
                            {"label": "PROFINET", "value": "PROFINET"}, ]
        style_result = {"display": "none"}
        if button_id == self.panel.get_menu()["protocols"].btn.id:
            if btn % 2 == 1:
                style_result = {"display": "flex"}
        else:
            pass
        return protocol_options, style_result
