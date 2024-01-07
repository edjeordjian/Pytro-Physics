"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from constants.porosity_constants import TOTAL_POROSITY_TAB_NAME

from ui.characterizationTabs.QTabWidgetWithWell import QTabWidgetWithWell

from ui.characterizationTabs.porosity_tabs.PorosityAsquithGibson import PorosityAsquithGibson

from ui.characterizationTabs.porosity_tabs.PorosityByGardnerHuntRaymer import PorosityByGardnerHuntRaymer

from ui.characterizationTabs.porosity_tabs.PorosityByWyllie import PorosityByWyllie

from ui.characterizationTabs.porosity_tabs.PorosityWithDensity import PorosityWithDensity


class TotalPorosityTab(QTabWidgetWithWell):
    def __init__(self):
        super().__init__(TOTAL_POROSITY_TAB_NAME)

        self.tabs = [
            PorosityWithDensity(),
            PorosityAsquithGibson(),
            PorosityByWyllie(),
            PorosityByGardnerHuntRaymer()
        ]

        self.initUI(tab_width=24)
