"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from ui.GraphicWindow import GraphicWindow
from ui.characterizationTabs.QWidgetWithWell import QWidgetWithWell
from ui.visual_components.data_menu_handler import deserialize_qt_attributes


class QWidgetStandAlone(QWidgetWithWell):
    def __init__(self, tab_name):
        super().__init__(tab_name)

        self.init_window()

    def init_window(self):
        self.window = GraphicWindow(self.get_tabs_serialization,
                                    self.set_tabs,
                                    self.get_vertical_unit,
                                    view_id=self.tab_name,
                                    stand_alone=True)

    def get_tabs_serialization(self):
        return self.get_view_serialization()

    def get_tabs_in_use(self):
        return [self]

    def set_tabs(self, tab_state):
        deserialize_qt_attributes(self, list(tab_state.values())[0])

    def get_vertical_unit(self):
        pass

    def preview(self):
        if not super().preview():
            return False

        self.replace_commas_in_numeric_inputs()

        return True
