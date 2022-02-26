import dash_core_components as dcc
import dash_cytoscape as cyto
import dash_html_components as html
from dash.dependencies import Output, Input

from .PanelCreator import PanelCreator


class NetworkPanelCreator(PanelCreator):
    TITLE = "Network"

    def __init__(self, handler, desc_prefix="network"):
        super().__init__(handler, desc_prefix)
        self.active_protocols = dcc.Checklist(id=self.panel.format_specifier("active_protocols"))
        # TODO - simultaneously define network graph with more detail and replace stub
        self.sidebar = html.Div(id=self.panel.format_specifier("sidebar"))

        self.topology_graph = cyto.Cytoscape(
            id=self.panel.format_specifier("topology-graph"),
            layout={'name': 'circle'},
            style={},
        )

        self.define_callbacks()

    def generate_menu(self):
        net_menu = self.panel.get_menu()
        protocols = net_menu.add_menu_item("protocols", "Protocols").set_dropdown()
        protocols.set_content()
        protocols.style = {"display": "none"}

    def generate_content(self):
        content = self.panel.content
        content.components = [self.sidebar, self.topology_graph]

        protocol_list_content = self.panel.get_menu()["protocols"].dropdown.set_content()
        protocol_list_content.components = [self.active_protocols]

    def define_callbacks(self):
        super().define_callbacks()

        self.handler.cb_mgr.register_callback(
            [Output(self.panel.format_specifier("active_protocols"), "options"),
             Output(self.panel.get_menu()["protocols"].dropdown.id, "style")],
            Input(self.panel.get_menu()["protocols"].btn.id, "n_clicks"),
            self.update_protocols,
            default_outputs=[[], {"display": "none"}]
        )

        self.handler.cb_mgr.register_callback(
            [Output(self.topology_graph.id, "elements")],
            Input(self.active_protocols.id, "value"),
            self.create_topology_by_protocol,
        )

        self.handler.cb_mgr.register_multiple_callbacks(
            [Output(self.panel.format_specifier("sidebar"), "children")],
            {
                Input(self.panel.format_specifier("topology-graph"),
                      "mouseoverNodeData"): (self.hover_node, None),
                Input(self.panel.format_specifier("topology-graph"),
                      "mouseoverEdgeData"): (self.hover_edge, None),
            },
            ["Hover over nodes or edges for details"]
        )

    # CALLBACK METHODS
    def create_topology_nodes(self):
        elements = []
        topology = self.handler.interface.get_network_topology()
        for d in topology.devices:
            elements.append({"data": {"id": d.mac_address, "label": d.mac_address}})
        return elements

    def create_topology(self, null):
        topology = self.handler.interface.get_network_topology()
        elements: list = self.create_topology_nodes()
        for c in topology.connections:
            elements.append({"data": {"source": c.first_device, "target": c.second_device}})
        return [elements]

    def create_topology_by_protocol(self, protocols):
        topology = self.handler.interface.get_network_topology()
        elements: list = self.create_topology_nodes()
        for c in topology.connections:
            for p in c.protocols:
                if p in protocols:
                    elements.append(
                        {"data": {"source": c.first_device, "target": c.second_device}})
        return [elements]

    def hover_node(self, node_data):
        result = "None"
        for d in self.handler.interface.get_network_topology().devices:
            if d.mac_address == node_data["label"]:
                result = "MAC: {}\nIP: {}".format(d.mac_address, d.ip_address if d.ip_address else "None")
        return [result]

    def hover_edge(self, edge_data):
        result = "None"
        for c in self.handler.interface.get_network_topology().connections:
            first_source_second_target = c.first_device == edge_data["source"] and c.second_device == edge_data[
                "target"]
            first_target_second_source = c.first_device == edge_data["target"] and c.second_device == edge_data[
                "source"]
            if first_source_second_target or first_target_second_source:
                result = "Protocols: {}".format(c.protocols)
        return [result]

    def update_protocols(self, btn):
        protocol_options = []
        protocol_set = self.handler.interface.get_highest_protocol_set()
        for p in protocol_set:
            protocol_options.append({"label": p, "value": p})
        style_result = {"display": "flex"} if btn % 2 == 1 else {"display": "none"}
        return [protocol_options, style_result]
