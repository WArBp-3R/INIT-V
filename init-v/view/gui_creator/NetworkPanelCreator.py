import dash_core_components as dcc
import dash_cytoscape as cyto

from .PanelCreator import PanelCreator


class NetworkPanelCreator(PanelCreator):
    TITLE = "Network"

    def __init__(self, desc_prefix="network"):
        super().__init__(desc_prefix)
        self.topology_graph = None
        self.active_protocols = None

    def generate_menu(self):
        net_menu = self.panel.get_menu()
        net_menu.add_menu_item("protocols", "Protocols").set_dropdown()

    def generate_content(self):
        content = self.panel.content

        # TODO - simultaneously define network graph with more detail and remove placeholder
        self.topology_graph = cyto.Cytoscape(
            id="topology-graph",
            layout={'name': 'preset'},
            style={'width': '100%', 'height': '400px'},
            elements=[
                {'data': {'id': 'one', 'label': 'Node 1'}, 'position': {'x': 75, 'y': 75}},
                {'data': {'id': 'two', 'label': 'Node 2'}, 'position': {'x': 200, 'y': 200}},
                {'data': {'source': 'one', 'target': 'two'}}
            ]
        )

        # TODO - get protocols from view interface(?)
        self.active_protocols = dcc.Checklist(id="active_protocols",
                                              options=[
                                                  {"label": "protocol placeholder1", "value": "P"},
                                                  {"label": "TCP", "value": "TCP"},
                                                  {"label": "PROFINET", "value": "PROFINET"}
                                              ])

        protocol_list_content = self.panel.get_menu()["protocols"].dropdown.set_content()
        protocol_list_content.components = [self.active_protocols]
