"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from constants import permeability_constants

from ui.characterizationTabs.QTabWidgetWithWell import QTabWidgetWithWell

from ui.characterizationTabs.permeability_tabs.PemeabilityAda import PermeabilityAda

from ui.characterizationTabs.permeability_tabs.PermeabilityCoates import PermeabilityCoates

from ui.characterizationTabs.permeability_tabs.PermeabilityCoatesAndDumanoir import PermeabilityCoatesAndDumanoir

from ui.characterizationTabs.permeability_tabs.PermeabilityKPHI import PermeabilityKPhi

from ui.characterizationTabs.permeability_tabs.PermeabilityRandomForest import PermeabilityRandomForest

from ui.characterizationTabs.permeability_tabs.PermeabilityTimur import PermeabilityTimur

from ui.characterizationTabs.permeability_tabs.PermeabilityXGBoost import PermeabilityXGBoost

from ui.characterizationTabs.permeability_tabs.PermiabilityTixier import PermeabilityTixier


class PermeabilityTab(QTabWidgetWithWell):
    def __init__(self):
        super().__init__(permeability_constants.PERMEABILITY_TAB_NAME)

        self.tabs = [
            PermeabilityRandomForest(), PermeabilityXGBoost(), PermeabilityAda(), PermeabilityKPhi(),
            PermeabilityTixier(), PermeabilityTimur(), PermeabilityCoates(), PermeabilityCoatesAndDumanoir()
        ]

        self.initUI()
