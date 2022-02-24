import plotly.express as px


class MethodResultContainer:
    def __init__(self, mappings: list[(float, float)], protocols: list[str], hover_data: list[str]):
        self.mappings = mappings
        self.protocols = protocols
        self.hover_data = hover_data
        self.packet_figure_x = [item[0] for item in mappings]
        self.packet_figure_y = [item[1] for item in mappings]
        self.packet_figure_dict = dict({"x": self.packet_figure_x, "y": self.packet_figure_y,
                                        "protocols": self.protocols, "hover_data": self.hover_data})
        self.figure = px.scatter(self.packet_figure_dict, x="x", y="y", color="protocols", hover_data="hover_data")


def merge_result_containers(results: list[MethodResultContainer]) -> MethodResultContainer:
    all_packet_mappings = list()
    all_packet_protocols = list()
    all_packet_hover_data = list()
    for result in results:
        all_packet_mappings += result.mappings
        all_packet_protocols += result.protocols
        all_packet_hover_data += result.hover_data
    return MethodResultContainer(all_packet_mappings, all_packet_protocols, all_packet_hover_data)
