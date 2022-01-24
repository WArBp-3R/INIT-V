import dash_core_components as dcc
import dash_html_components as html

from .gui_creator.ComparePanelCreator import ComparePanelCreator
from .gui_creator.DashboardPanelCreator import DashboardPanelCreator


class GUIHandler:
    def __init__(self):
        dashboard_panel_creator = DashboardPanelCreator()
        compare_panel_creator = ComparePanelCreator()

        self.panel_creators = {
            dashboard_panel_creator.panel.desc_prefix: dashboard_panel_creator,
            compare_panel_creator.panel.desc_prefix: compare_panel_creator
        }

        for pc in self.panel_creators.values():
            sub_panel_creators = pc.sub_panel_creators
            for spc in sub_panel_creators:
                self.panel_creators[spc.panel.desc_prefix] = spc

        self.url = dcc.Location(id='url')
        self.window = dcc.Location(id="window")
        self.default_panel = self.panel_creators["dashboard"]

    def get_layout(self):
        html.Div(id="app", children=[
            self.url,
            html.Div(id="window", children=[self.default_panel.generate_content()])])

    # TODO - callback
    def display_page(self, path):
        pass
