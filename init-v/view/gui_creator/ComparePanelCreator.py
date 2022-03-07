import dash_core_components as dcc
import dash_html_components as html

from .PanelCreator import PanelCreator
from .RunResultPanelCreator import RunResultPanelCreator


class ComparePanelCreator(PanelCreator):
    TITLE = "Compare"
    IS_MAIN_PANEL = True

    def __init__(self, handler, desc_prefix="cmp"):
        self.run1_selector = None
        self.run2_selector = None

        spc = [x[0](handler, desc_prefix=x[1]) for x in
               [(RunResultPanelCreator, "run_1"), (RunResultPanelCreator, "run_2")]]

        super().__init__(handler, desc_prefix, sub_panel_creators=spc)

    def generate_menu(self):
        cmp_menu = self.panel.get_menu()
        # select_run = cmp_menu.add_menu_item("select-run", "Select Run").set_dropdown()
        # select_run.set_content()
        # select_run.style = {"display": "none"}

    def generate_content(self):
        content = self.panel.content
        content.components = [spc.panel.layout for spc in self.sub_panel_creators.values()]

        # self.run1_selector = dcc.RadioItems(id=self.panel.format_specifier("run1_selector"))
        # self.run2_selector = dcc.RadioItems(id=self.panel.format_specifier("run2_selector"))

        # run_select_list_content = self.panel.get_menu()["select-run"].dropdown.set_content()
        # run_select_list_content.components = [
        #     html.Div(["Run 1:", self.run1_selector]),
        #     html.Div(["Run 2:", self.run2_selector])]

    # def define_callbacks(self):
    #     self.handler.app.callback(
    #         Output(self.panel.format_specifier("run1_selector"), "options"),
    #         Output(self.panel.format_specifier("run2_selector"), "options"),
    #         Output(self.panel.get_menu()["select-run"].dropdown.id, "style"),
    #         Input(self.panel.get_menu()["select-run"].btn.id, "n_clicks"),
    #     )(self.update_run_select_list)

    # # TODO - replace stub
    # def update_run_select_list(self, btn):
    #     button_id = get_input_id()
    #     print("update_run_select_list")
    #     # view adapter stuff
    #     run_options = [{"label": "run placeholder1", "value": "run1"},
    #                    {"label": "run placeholder2", "value": "run2"},
    #                    {"label": "run placeholder3", "value": "run3"},]
    #     style_result = {"display": "none"}
    #     if button_id == self.panel.get_menu()["select-run"].btn.id:
    #         if btn % 2 == 1:
    #             style_result = {"display": "flex"}
    #     else:
    #         pass
    #     return run_options, run_options, style_result
