"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from ui.popUps.alertWindow import AlertWindow


class InfoWindow(AlertWindow):
    def __init__(self,
                 message,
                 title='Aviso',
                 kind='info'):
        super().__init__(message,
                         title=title,
                         kind=kind)
