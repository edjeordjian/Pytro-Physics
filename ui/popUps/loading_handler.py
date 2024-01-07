"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from PyQt6.QtCore import QTimer

from constants.general_constants import loading_pop_up_timeout_ms

from ui.popUps.LoadingWindow import LoadingWindow


def loading_pop_up(message,
                   fn):
    pop_up = LoadingWindow(message)

    QTimer.singleShot(loading_pop_up_timeout_ms, lambda: (
        fn(),

        pop_up.close()))
