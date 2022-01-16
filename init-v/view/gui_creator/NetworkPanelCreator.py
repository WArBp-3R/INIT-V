import dash_core_components as dcc
import dash_cytoscape as cyto

from .PanelCreator import PanelCreator


class NetworkPanelCreator(PanelCreator):
    TITLE = "Network"

    def __init__(self, desc_prefix="network"):
        super().__init__(desc_prefix)
        self.topology_graph: cyto.Cytoscape
        self.active_protocols: dcc.Checklist

    def generate_menu(self):
        net_menu = self.panel.get_menu()
        net_menu.add_menu_item("protocol", "Protocols").set_dropdown()

    def generate_content(self):
        pass
        # TODO
