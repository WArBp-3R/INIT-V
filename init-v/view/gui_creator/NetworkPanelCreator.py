import os

import dash_core_components as dcc
import dash_cytoscape as cyto
import dash_html_components as html
from dash.dependencies import Output, Input, State

from view.utility.UniqueColors import UNIQUE_COLORS
from .PanelCreator import PanelCreator

cyto.load_extra_layouts()


class NetworkPanelCreator(PanelCreator):
    TITLE = "Network"

    def __init__(self, handler, desc_prefix="network"):
        self.active_protocols = None
        self.sidebar = None
        self.topology_graph = None
        self.layout_options = None
        self.edge_view_mode = None

        # Dash dependencies
        self.topology_outputs = None
        self.topology_graph_state = None

        self.current_stylesheet = None

        super().__init__(handler, desc_prefix)

    def generate_menu(self):
        net_menu = self.panel.get_menu()
        protocols = net_menu.add_menu_item("protocols", "Protocols").set_dropdown()
        protocols.style = {"display": "none"}

        net_menu.add_menu_item("layout", "Layout").set_dropdown()
        net_menu.add_menu_item("edge_mode", "Edge Mode").set_dropdown()


        generate_image = net_menu.add_menu_item("generate_image", "Generate Image").set_dropdown().set_menu()
        generate_image.add_menu_item("png", "as .png")
        generate_image.add_menu_item("svg", "as .svg")

        reset_button = net_menu.add_menu_item("reset", "Reset")

    def generate_content(self):
        self.sidebar = html.Div(id=self.panel.format_specifier("sidebar"))

        # TODO - define network graph with more detail
        self.topology_graph = cyto.Cytoscape(
            id=self.panel.format_specifier("topology-graph"),
            layout={'name': 'preset'},
            style={},
            stylesheet=[
                {
                    "selector": "node",
                    "style": {
                        "content": "data(id)"
                    }
                },
                {
                    "selector": ".hover",
                    "style": {
                        "background-color": "#f06000",
                        "line-color": "#f06000"
                    }
                },
                {
                    "selector": "edge",
                    "style": {
                        'curve-style': 'bezier'
                    }
                }
            ]
        )

        self.panel.content.components = [self.sidebar, self.topology_graph]

        self.active_protocols = dcc.Checklist(id=self.panel.format_specifier("active_protocols"))
        self.panel.get_menu()["protocols"].dropdown.set_content().components = [self.active_protocols]

        self.edge_view_mode = dcc.RadioItems(id=self.panel.format_specifier("edge_view_mode"),
                                             options=[{"label": "Edge for connection", "value": "connection"},
                                                      {"label": "Edge for protocol", "value": "protocol"}],
                                             value="connection")
        self.panel.get_menu()["edge_mode"].dropdown.set_content().components = [self.edge_view_mode]

        self.layout_options = dcc.RadioItems(id=self.panel.format_specifier("layout_options"),
                                             options=[{"label": x, "value": x} for x in
                                                      ["cose", "circle", "breadthfirst", "grid", "concentric",
                                                       "random"]],
                                             value="cose")
        self.panel.get_menu()["layout"].dropdown.set_content().components = [self.layout_options]

    def define_callbacks(self):
        super().define_callbacks()

        self.topology_outputs = [Output(self.topology_graph.id, "elements"), Output(self.sidebar.id, "children"),
                                 Output(self.topology_graph.id, "stylesheet")]
        self.topology_graph_state = [State(self.topology_graph.id, "elements")]

        generate_image_menu = self.panel.get_menu()["generate_image"].dropdown.menu

        self.register_dropdown_list_update_callback(self.active_protocols, "protocols", self.update_protocols)

        """Callback for changing layout"""
        self.handler.cb_mgr.register_callback(
            [Output(self.topology_graph.id, "layout")],
            Input(self.layout_options.id, "value"),
            lambda x: [{"name": x}],
            default_outputs=[{'name': 'cose'}]
        )

        """Callback for exporting cytoscape images"""
        self.handler.cb_mgr.register_multiple_callbacks(
            [Output(self.topology_graph.id, "generateImage")], {
                Input(generate_image_menu["png"].id, "n_clicks"): (
                    self.generate_image_for_download, [State(generate_image_menu["png"].id, "id")]),
                Input(generate_image_menu["svg"].id, "n_clicks"): (
                    self.generate_image_for_download, [State(generate_image_menu["svg"].id, "id")])
            },
            default_outputs=[{}]
        )

        """Callbacks regarding sidebar displays"""
        self.handler.cb_mgr.register_multiple_callbacks(
            self.topology_outputs, {
                # Input(self.active_protocols.id, "value"): (self.create_topology_by_protocol, None),
                Input(self.panel.format_specifier("topology-graph"),
                      "mouseoverNodeData"): (self.hover_node, self.topology_graph_state),
                Input(self.panel.format_specifier("topology-graph"),
                      "mouseoverEdgeData"): (self.hover_edge, self.topology_graph_state),
                Input(self.panel.format_specifier("topology-graph"),
                      "tapNodeData"): (self.hover_node, self.topology_graph_state),
                Input(self.panel.format_specifier("topology-graph"),
                      "tapEdgeData"): (self.hover_edge, self.topology_graph_state),
            },
            [list(), "No session loaded"]
        )

        """Callbacks"""
        self.handler.cb_mgr.register_multiple_callbacks(
            self.topology_outputs, {
                Input(self.edge_view_mode.id, "value"): (
                    lambda e, p: self.update_topology_graph(e, p), [State(self.active_protocols.id, "value")]),
                Input(self.active_protocols.id, "value"): (
                    lambda p, e: self.update_topology_graph(e, p), [State(self.edge_view_mode.id, "value")]),
            }
        )

        self.handler.cb_mgr.register_callback(
            [Output(self.panel.format_specifier("active_protocols"), "options"),
             Output(self.panel.get_menu()["protocols"].dropdown.id, "style")],
            Input(self.edge_view_mode.id, "value"),
            self.update_protocol_mode,
            [State(self.panel.get_menu()["protocols"].dropdown.id, "style")]
        )
        self.handler.cb_mgr.register_callback(
            self.topology_outputs,
            Input(self.panel.get_menu()["reset"].id, "n_clicks"),
            self.reset_graph,
            [State(self.edge_view_mode.id, "value"), State(self.active_protocols.id, "value")]
        )
    # CALLBACK METHODS
    def update_protocols(self, btn):
        protocol_options = []
        protocol_set = self.handler.interface.get_highest_protocol_set()
        for p in protocol_set:
            protocol_options.append({"label": p, "value": p})
        style_result = {"display": "flex"} if btn % 2 == 1 else {"display": "none"}
        return [protocol_options, style_result]

    def generate_image_for_download(self, btn, filetype):
        return [{"filename": self.handler.interface.get_session_path().split(os.sep)[-1].split(".")[0],
                 "type": filetype.split("_")[-2],
                 "action": "download"}]

    def create_topology_nodes(self):
        elements = []
        topology = self.handler.interface.get_network_topology()
        for d in topology.devices:
            elements.append({"data": {"id": d.mac_address}})
        return elements

    def create_topology(self, null):
        return self.update_topology_graph("connection", [])

    def activate_hover_color(self, elements, data):
        elements_data_only = [e["data"] for e in elements]
        el_idx = elements_data_only.index(data)
        for e in elements:
            e["classes"] = ""
        elements[el_idx]["classes"] = "hover"
        return elements

    def hover_node(self, node_data, graph):
        result = []
        for d in self.handler.interface.get_network_topology().devices:
            if d.mac_address == node_data["id"]:
                result = [f"MAC: {d.mac_address}", html.Br()]
                if len(d.ip_address) > 0:
                    result += ["Associated IP Addr.: ", html.Br()]
                    for ip in d.ip_address:
                        result += [f"{ip}", html.Br()]
        return [self.activate_hover_color(graph, node_data), result, self.current_stylesheet]

    def hover_edge(self, edge_data, graph):
        result = []
        for c in self.handler.interface.get_network_topology().connections:
            first_source_second_target = c.first_device.mac_address == edge_data[
                "source"] and c.second_device.mac_address == edge_data[
                                             "target"]
            first_target_second_source = c.first_device.mac_address == edge_data[
                "target"] and c.second_device.mac_address == edge_data[
                                             "source"]
            if first_source_second_target or first_target_second_source:
                if edge_data["protocol"] == "all":
                    result += ["Used Protocols: ", html.Br()]
                    for protocol in c.protocols:
                        result += [f"{protocol}, "]
                    result[-1].removesuffix(", ")
                    result.append(html.Br())
                    for stat_name, stat_value in c.connection_information.items():
                        result += [f"{stat_name} = {stat_value}", html.Br()]
                    break
                else:
                    protocol = edge_data["protocol"]
                    result += [f"Protocol: {protocol}", html.Br()]
                    for stat_name, stat_value in c.protocol_connection_information[protocol].items():
                        result += [f"{stat_name} = {stat_value}", html.Br()]
                    break
        return [self.activate_hover_color(graph, edge_data), result, self.current_stylesheet]

    def update_protocol_mode(self, mode, style_result):
        protocol_options: list = []
        if mode == "connection":
            for protocol in self.handler.interface.get_network_topology().highest_protocols:
                protocol_options.append({"label": protocol, "value": protocol})
        else:
            for protocol in self.handler.interface.get_network_topology().protocols:
                protocol_options.append({"label": protocol, "value": protocol})
        return [protocol_options, style_result]

    def update_topology_graph(self, view_mode, active_protocols):
        topology = self.handler.interface.get_network_topology()
        graph_elements: list = self.create_topology_nodes()
        selected_protocols = active_protocols if active_protocols is not None else (
            topology.protocols if view_mode == "protocol" else topology.highest_protocols)
        new_stylesheet = [
            {
                "selector": "label",
                "style": {
                    "color": "#ffffff"
                }
            },
            {
                "selector": "node",
                "style": {
                    "content": "data(id)"
                }
            },
            {
                "selector": ".hover",
                "style": {
                    "background-color": "#f06000",
                    "line-color": "#f06000"
                }
            },
            {
                "selector": "edge",
                "style": {
                    'curve-style': 'bezier'
                }
            }
        ]
        for connection in topology.connections:
            if view_mode == "connection":
                for protocol in connection.protocols:
                    if protocol in selected_protocols:
                        graph_elements.append({"data": {"source": connection.first_device.mac_address,
                                                        "target": connection.second_device.mac_address,
                                                        "protocol": "all"}})
                        break
            else:
                for protocol in connection.protocols:
                    if protocol in selected_protocols:
                        graph_elements.append({"data": {"source": connection.first_device.mac_address,
                                                        "target": connection.second_device.mac_address,
                                                        "protocol": protocol}})
                for protocol, color in zip(topology.protocols, UNIQUE_COLORS[0: len(topology.protocols)]):
                    new_stylesheet.append({
                        "selector": f"[protocol = \"{protocol}\"]",
                        "style": {
                            "line-color": f"{color}"
                        }
                    })
                    pass
        self.current_stylesheet = new_stylesheet
        return [graph_elements, "Hover over nodes or edges for details", new_stylesheet]

    def reset_graph(self, button, v, a):
        return self.update_topology_graph(v, a)
