"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from ui.visual_components.constant_curves_handler import add_rectangle_to


class SingleCurveVShalePreviewer:
    def __init__(self,
                 graph_window,
                 config_curve,
                 config_vshale,
                 groups,
                 tab_name):
        config_curve["add_axis"] = True

        config_vshale["add_axis"] = True

        graph_window.add_curve(config_curve)

        graph_window.add_curve(config_vshale)

        for i in range(len(groups)):
            if groups[i]["Min Depth QLE"].isEnabled():
                config = {
                    "y0": groups[i]["Min Depth QLE"].text(),
                    "y1": groups[i]["Max Depth QLE"].text(),
                    "x0": groups[i]["Min Curve QLE"].text(),
                    "x1": groups[i]["Max Curve QLE"].text(),

                    "color": groups[i]["Color"].currentText(),
                    "line": groups[i]["Line"].currentText(),

                    'tab_name': config_curve['tab_name'],
                    'track_name': config_curve['track_name']
                }

                add_rectangle_to(graph_window,
                                 config,
                                 f'{str(i)}')

        graph_window.draw_tracks(tab_name)
