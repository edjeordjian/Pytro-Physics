"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

import numpy as np

from constants.pytrophysicsConstants import LINE_MARKER_CONSTANTS

import pyqtgraph as pg

from ui.style.LineColors import getColor

from ui.style.LineTypes import LineTypes

from numpy import log10


def get_base_config(config):
    color = config.get("color",
                       "Negro")

    line_style = config.get('line',
                            'Solida')

    line_marker = config.get('marker',
                             LINE_MARKER_CONSTANTS["NONE"])

    line_width = config.get("line_width",
                            3)

    return {
        'color': color,
        'line_style': line_style,
        'line_marker': line_marker,
        'line_width': line_width,
        'tab_name': config['tab_name'],
        'track_name': config['track_name'],
        'cummulative': True
    }


def add_rectangle_to(graph_window,
                     config,
                     name_id):
    if not config.get('y0', 0) or not config.get('y1', 0) \
            or not config.get('x0', 0) \
            or not config.get('x1', 0):
        return

    y0 = float(config['y0'])

    y1 = float(config['y1'])

    x0 = float(config['x0'])

    x1 = float(config['x1'])

    color = config.get("color",
                       "Negro")

    line_style = config.get('line',
                            'Solida')

    line_marker = config.get('marker',
                             LINE_MARKER_CONSTANTS["NONE"])

    line_width = config.get("line_width",
                            3)

    add_line_to(graph_window,
                {
                    'x_axis': [x0, x1],
                    'y_axis': [y1, y1],
                    'curve_name': 'Rect. techo' + name_id,
                    'add_axis': False,
                    'tab_name': config['tab_name'],
                    'track_name': config['track_name'],
                    'color': color,
                    'line': line_style,
                    'line_marker': line_marker,
                    'line_width': line_width,
                    "ephimeral": True
                })

    add_line_to(graph_window,
                {
                    'x_axis': [x0, x1],
                    'y_axis': [y0, y0],
                    'curve_name': 'Rect. piso' + name_id,
                    'add_axis': False,
                    'tab_name': config['tab_name'],
                    'track_name': config['track_name'],
                    'color': color,
                    'line': line_style,
                    'line_marker': line_marker,
                    'line_width': line_width,
                    "ephimeral": True
                })

    add_line_to(graph_window,
                {
                    'x_axis': [x0, x0],
                    'y_axis': [y0, y1],
                    'curve_name': 'Rect. izq.' + name_id,
                    'add_axis': False,
                    'tab_name': config['tab_name'],
                    'track_name': config['track_name'],
                    'color': color,
                    'line': line_style,
                    'line_marker': line_marker,
                    'line_width': line_width,
                    "ephimeral": True
                })

    add_line_to(graph_window,
                {
                    'x_axis': [x1, x1],
                    'y_axis': [y0, y1],
                    'curve_name': 'Rect. der.' + name_id,
                    'add_axis': False,
                    'tab_name': config['tab_name'],
                    'track_name': config['track_name'],
                    'color': color,
                    'line': line_style,
                    'line_marker': line_marker,
                    'line_width': line_width,
                    "ephimeral": True
                })


def add_line_to(graph_window,
                config):
    config.update(get_base_config(config))

    graph_window.append_curve(config)


def add_bottom_half_bucket_to(graph_window,
                              config):
    config.update(get_base_config(config))

    config['line_width'] = 1

    vertical_line = [config['x_min'], config['x_max']]

    x_axis = [*vertical_line]

    y_axis = [config['y_min']] * len(vertical_line)

    horizontal_line = [config['y_min'], config['y_max']]

    x_axis += [config['x_min']] * len(horizontal_line)

    y_axis += [*horizontal_line]

    x_axis += [*vertical_line]

    y_axis += [config['y_max']] * len(vertical_line)

    config['x_axis'] = x_axis

    config['y_axis'] = y_axis

    graph_window.append_curve(config)


def add_upper_half_bucket_to(graph_window,
                             config):
    config.update(get_base_config(config))

    config['line_width'] = 1

    vertical_line = [config['x_min'], config['x_max']]

    horizontal_line = [config['y_min'], config['y_max']]

    x_axis = [*vertical_line]

    x_axis += [config['x_max']] * len(horizontal_line)

    x_axis += [*vertical_line]

    y_axis = [config['y_min']] * len(vertical_line)

    y_axis += [*horizontal_line]

    y_axis += [config['y_max']] * len(vertical_line)

    config['x_axis'] = x_axis

    config['y_axis'] = y_axis

    graph_window.append_curve(config)


def get_line(config):
    color = getColor(config.get("line_color",
                                "Azul"))

    style = LineTypes().getLineType(config.get("line_style",
                                               "Solida"))

    pen = pg.mkPen(color=color,
                   style=style,
                   width=2)

    if config.get("x_values") is None:
        x_values = [config.get("x_min", -2000), config.get("x_max", 2000)]

    else:
        x_values = config.get("x_values")

    if config.get("y_values") is None:
        y_values = [config.get("y_min", -2000), config.get("y_max", 2000)]

    else:
        y_values = config.get("y_values")

    if config.get("is_log", False):
        x_values = log10(x_values)

        x_values[np.isnan(x_values)] = -2000

    if config.get("is_y_log", False):
        y_values = log10(y_values)

        y_values[np.isnan(y_values)] = -2000

    return pg.PlotCurveItem(x=x_values,
                            y=y_values,
                            pen=pen)
