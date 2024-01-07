"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

class EphimeralTrackRegister:
    def __init__(self,
                 track_name,
                 tab_name):
        self.track_name = track_name

        self.tab_name = tab_name

    def __eq__(self,
               to_compare):
        if not isinstance(to_compare, EphimeralTrackRegister):
            return False

        return self.track_name == to_compare.track_name and self.tab_name == to_compare.tab_name

    def __hash__(self):
        return hash((self.track_name, self.tab_name))

    def get_track_name(self):
        return self.track_name

    def get_tab_name(self):
        return self.tab_name
