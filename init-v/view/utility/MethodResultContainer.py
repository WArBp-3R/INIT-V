import plotly.express as px


class MethodResultContainer:
    def __init__(self, run, mappings: list[(float, float)], protocols: list[str], hover_data: list[dict[str, str]]):
        self.mappings = mappings
        self.protocols = protocols
        self.hover_data = hover_data
        self.packet_figure_x = [item[0] for item in mappings]
        self.packet_figure_y = [item[1] for item in mappings]
        self.packet_figure_dict = dict(
            {"run": [run for item in mappings], "x": self.packet_figure_x, "y": self.packet_figure_y,
             "protocols": self.protocols})
        self.figure = None
        if len(hover_data) > 0:
            for hover_item in hover_data[0].keys():
                self.packet_figure_dict[hover_item] = [hover_information[hover_item] for hover_information in hover_data]
            self.figure = px.scatter(self.packet_figure_dict, x="x", y="y", color="protocols",
                                     hover_data=hover_data[0].keys(), template="plotly_dark")


def merge_result_containers(run, results: list[MethodResultContainer],
                            run_names: list[str] = None) -> MethodResultContainer:
    all_packet_mappings = list()
    all_packet_protocols = list()
    all_packet_hover_data = list()
    for run_name, result in zip(run_names, results):
        all_packet_mappings += result.mappings
        all_packet_protocols += result.protocols if run_names is None else map(lambda x: f"{run_name}: {x}",
                                                                               result.protocols)
        all_packet_hover_data += result.hover_data
    return MethodResultContainer(run, all_packet_mappings, all_packet_protocols, all_packet_hover_data)
