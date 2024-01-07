"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from constants.general_constants import GRAPHIC_WINDOW_NAME

from model.WellModel import WellModel

from ui.GraphicWindow import GraphicWindow


class Well:
    def __init__(self, well_name, well_url, well_action,
                 well_is_new, tab_serialization_function, tab_set_function, tab_update_fn):
        self.wellModel = WellModel(well_name, well_url, well_action, well_is_new)

        self.graphicWindow = GraphicWindow(tab_serialization_function,
                                           tab_set_function,
                                           self.wellModel.get_depth_unit,
                                           tab_update_fn=tab_update_fn,
                                           title=GRAPHIC_WINDOW_NAME,
                                           get_depth_range=self.wellModel.get_depth_range)
