import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Output, Input

from .MethodResultsPanelCreator import MethodResultsPanelCreator
from .PanelCreator import PanelCreator
from .PerformancePanelCreator import PerformancePanelCreator
from ..GUI_Handler import app, get_input_id


class ComparePanelCreator(PanelCreator):
    TITLE = "Compare"
    IS_MAIN_PANEL = True

    def __init__(self, desc_prefix="cmp"):
        super().__init__(desc_prefix)
        self.run1_selector = None
        self.run2_selector = None

        self.add_sub_panel_creator(MethodResultsPanelCreator("m-res-run1", "Method Results - Run 1"))
        self.add_sub_panel_creator(MethodResultsPanelCreator("m-res-run2", "Method Results - Run 2"))
        self.add_sub_panel_creator(PerformancePanelCreator("perf-run1", "Performance - Run 1"))
        self.add_sub_panel_creator(PerformancePanelCreator("perf-run2", "Performance - Run 2"))

        self.define_callbacks()

    def define_callbacks(self):
        app.callback(
            Output("run1_selector", "options"),
            Output("run2_selector", "options"),
            Output(self.panel.get_menu()["select-run"].dropdown.id, "style"),
            Input(self.panel.get_menu()["select-run"].btn.id, "n_clicks"),
        )(self.update_run_select_list)


        # TODO - fix output lists
        app.callback(
            Output(self.sub_panel_creators["m-res-run1"].panel.format_specifier("autoencoder_graph"), "figure"),
            Output(self.sub_panel_creators["m-res-run1"].panel.format_specifier("pca_graph"), "figure"),
            Output(self.sub_panel_creators["m-res-run1"].panel.format_specifier("merged_graph"), "figure"),
            # self.sub_panel_creators["m-res-run1"].graph_outputs,
            Input("run1_selector", "value"),
            Input(self.sub_panel_creators["m-res-run1"].panel.format_specifier("active_protocols"), "value")
        )(self.update_run1_method_results_panel)

        app.callback(
            Output(self.sub_panel_creators["perf-run1"].panel.format_specifier("autoencoder_graph"), "figure"),
            Output(self.sub_panel_creators["perf-run1"].panel.format_specifier("pca_graph"), "figure"),
            Output(self.sub_panel_creators["perf-run1"].panel.format_specifier("merged_graph"), "figure"),
            # self.sub_panel_creators["perf-run1"].graph_outputs,
            Input("run1_selector", "value"),
            Input(self.sub_panel_creators["perf-run1"].panel.format_specifier("accuracy"), "value"),
            Input(self.sub_panel_creators["perf-run1"].panel.format_specifier("data_loss"), "value"),
        )(self.update_run1_performance_panel)

        # TODO - fix output lists
        app.callback(
            Output(self.sub_panel_creators["m-res-run2"].panel.format_specifier("autoencoder_graph"), "figure"),
            Output(self.sub_panel_creators["m-res-run2"].panel.format_specifier("pca_graph"), "figure"),
            Output(self.sub_panel_creators["m-res-run2"].panel.format_specifier("merged_graph"), "figure"),
            # self.sub_panel_creators["m-res-run2"].graph_outputs,
            Input("run2_selector", "value"),
            Input(self.sub_panel_creators["m-res-run2"].panel.format_specifier("active_protocols"), "value")
        )(self.update_run2_method_results_panel)

        app.callback(
            Output(self.sub_panel_creators["perf-run2"].panel.format_specifier("autoencoder_graph"), "figure"),
            Output(self.sub_panel_creators["perf-run2"].panel.format_specifier("pca_graph"), "figure"),
            Output(self.sub_panel_creators["perf-run2"].panel.format_specifier("merged_graph"), "figure"),
            # self.sub_panel_creators["perf-run2"].graph_outputs,
            Input("run2_selector", "value"),
            Input(self.sub_panel_creators["perf-run2"].panel.format_specifier("accuracy"), "value"),
            Input(self.sub_panel_creators["perf-run2"].panel.format_specifier("data_loss"), "value"),
        )(self.update_run2_performance_panel)

    def generate_menu(self):
        cmp_menu = self.panel.get_menu()
        select_run = cmp_menu.add_menu_item("select-run", "Select Run").set_dropdown()
        select_run.set_content()
        select_run.style = {"display": "none"}

    def generate_content(self):
        content = self.panel.content

        for spc in self.sub_panel_creators.values():
            spc.generate_content()
        content.components = [spc.panel.layout for spc in self.sub_panel_creators.values()]

        self.run1_selector = dcc.RadioItems(id="run1_selector")
        self.run2_selector = dcc.RadioItems(id="run2_selector")

        run_select_list_content = self.panel.get_menu()["select-run"].dropdown.set_content()
        run_select_list_content.components = [
            html.Div(["Run 1:", self.run1_selector]),
            html.Div(["Run 2:", self.run2_selector])]

    # TODO - remove stub
    def update_run_select_list(self, btn):
        button_id = get_input_id()
        print("update_run_select_list")
        # view adapter stuff
        run_options = [{"label": "run placeholder1", "value": "run1"},
                       {"label": "run placeholder2", "value": "run2"},
                       {"label": "run placeholder3", "value": "run3"},]
        style_result = {"display": "none"}
        if button_id == self.panel.get_menu()["select-run"].btn.id:
            if btn % 2 == 1:
                style_result = {"display": "flex"}
        else:
            pass
        return run_options, run_options, style_result

    # TODO - remove stub
    def update_run1_method_results_panel(self, val, protocols):
        print("m-res-run1 panel updating... (STUB)")
        # view adapter stuff
        bruh_graph = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[4, 1, 2])])
        print("m-res-run1 panel updated... (STUB)")
        return bruh_graph, bruh_graph, bruh_graph

    # TODO - remove stub
    def update_run1_performance_panel(self, val, ae_val, pca_val):
        print("perf-run1 panel updating... (STUB)")
        # view adapter stuff
        bruh_graph = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[4, 1, 2])])
        print("perf-run1 panel updated... (STUB)")
        return bruh_graph, bruh_graph, bruh_graph

    # TODO - remove stub
    def update_run2_method_results_panel(self, val, protocols):
        print("m-res-run2 panel updating... (STUB)")
        # view adapter stuff
        bruh_graph = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[4, 1, 2])])
        print("m-res-run2 panel updated... (STUB)")
        return bruh_graph, bruh_graph, bruh_graph

    # TODO - remove stub
    def update_run2_performance_panel(self, val, ae_val, pca_val):
        print("perf-run2 panel updating... (STUB)")
        # view adapter stuff
        bruh_graph = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[4, 1, 2])])
        print("perf-run2 panel updated... (STUB)")
        return bruh_graph, bruh_graph, bruh_graph
