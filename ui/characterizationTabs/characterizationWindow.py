"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from ui.characterizationTabs.porosity_tabs.EffectivePorosityTab import EffectivePorosityTab

from ui.characterizationTabs.QTabWidgetWithWell import QTabWidgetWithWell

from ui.characterizationTabs.SwirrTab import SwirrTab

from ui.characterizationTabs.permeability_tabs.PermeabilityTab import PermeabilityTab

from ui.characterizationTabs.crossplotTab import Crossplot

from ui.characterizationTabs.matrixPropertiesTab import MatrixPropertiesTab

from ui.characterizationTabs.TotalPorosityTab import TotalPorosityTab

from ui.characterizationTabs.swTab import SWTab

from ui.characterizationTabs.cutoffTab import CutoffTab

from ui.characterizationTabs.histogramsTab import HistogramsTab

from ui.characterizationTabs.iprTab import IPRTab

from ui.characterizationTabs.vShaleTab import VShaleTab


class CharacterizationWindow(QTabWidgetWithWell):
    def __init__(self):
        super().__init__("Characterization window")

        self.tabs = [VShaleTab(),
                     MatrixPropertiesTab(),
                     TotalPorosityTab(),
                     EffectivePorosityTab(),
                     SWTab(),
                     PermeabilityTab(),
                     SwirrTab(),
                     CutoffTab(),
                     Crossplot(),
                     HistogramsTab(),
                     IPRTab()]

        self.initUI()

