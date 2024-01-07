"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from ui.characterizationTabs.QTabWidgetWithWell import QTabWidgetWithWell

from constants.sw_constants import (RW_TAB_FULL_NAME, SW_TAB_NAME, SW_CALCULATION_TAB_NAME, RW_TAB_NAME)

from ui.characterizationTabs.swTabs.RwTab import RwTab

from ui.characterizationTabs.swTabs.SwCalculation import SwCalculation

from ui.characterizationTabs.swTabs.temperatureTab import TemperatureTab

from ui.characterizationTabs.swTabs.soSgTab import SoSgTab


class SWTab(QTabWidgetWithWell):
    def __init__(self):
        super().__init__(SW_TAB_NAME)

        self.tabs = [
            TemperatureTab(),
            RwTab(RW_TAB_NAME),
            SwCalculation(SW_CALCULATION_TAB_NAME),
            SoSgTab()
        ]

        self.initUI()
