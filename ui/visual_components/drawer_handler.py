"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

import numpy as np

import pandas as pd

import pyqtgraph.functions as fn

from PyQt6.QtGui import QBrush, QColor

from pyqtgraph import AxisItem

from constants.general_constants import BLANK_LABEL_FONT_SIZE, RECTANGLE_NAME_PREFIX

from constants.pytrophysicsConstants import LINE_MARKER_CONSTANTS
from services.tools.number_service import min_with_nans, max_with_nans

from ui.style.BrushFill import get_brush_fill

from ui.style.LineColors import getColor, get_color_values

from ui.style.LineMarkers import LineMarkers

from ui.style.LineTypes import LineTypes

from ui.visual_components.RectangleComponent import RectangleComponent

from ui.visual_components.CustomAxis import CustomAxis

from ui.visual_components.constant_curves_handler import get_line

from ui.visual_components.track_handler import (create_track_plot_item, adjust_track_viewbox,
                                                create_track_scatter_plot_item)

import pyqtgraph as pg


def get_config_elements(config):
    x_axis = config["x_axis"]

    y_axis = config["y_axis"]

    line_width = config.get("line_width",
                            1)

    color_name = config.get("color",
                            "Negro")

    style = LineTypes().getLineType(config.get("line_style",
                                               "Solida"))

    line_marker = LineMarkers().getLineMarker(config.get("line_marker",
                                                         LINE_MARKER_CONSTANTS["NONE"]))

    add_axis = config.get('add_axis',
                          False)

    add_to_plot = config.get('add_to_plot',
                             True)

    invisible = config.get('invisible',
                           False)

    if invisible:
        line_width = 0.00001

    cummulative = config.get('cummulative',
                             False)

    scatter_curve = config.get('scatter_curve',
                               False)

    no_grid = config.get('no_grid',
                         False)

    curve_name = config.get('curve_name',
                            False)

    is_log = config.get("is_log",
                        False)

    is_reverse = config.get("is_reverse",
                            False)

    y_label = config.get("y_label",
                         "")

    is_y_log = config.get("is_y_log", False)

    y_min_viewbox = config.get("y_min_viewbox", 
                       None)

    y_max_viewbox = config.get("y_max_viewbox", 
                       None)

    return x_axis, y_axis, line_width, color_name, \
        style, line_marker, add_axis, add_to_plot, \
        invisible, cummulative, scatter_curve, no_grid, \
        curve_name, is_log, is_reverse, y_label, is_y_log, \
        y_min_viewbox, y_max_viewbox


def _add_curve(config,
               curve_track):
    x_axis, y_axis, line_width, color_name, \
        style, line_marker, add_axis, add_to_plot, \
        invisible, cummulative, scatter_curve, no_grid, \
        curve_name, is_log, is_reverse, y_label, is_y_log, \
        y_min_viewbox, y_max_viewbox = get_config_elements(config)

    if not curve_track.last_item():
        pg_plot_item = create_track_plot_item({
            'y_axis': y_axis,
            'x_axis': x_axis,
            'cummulative': cummulative,
            'no_grid': no_grid,
            'y_label': y_label,
            'is_log': is_log,
            "is_y_log": is_y_log,
            "scatter_curve": scatter_curve,
            "y_min_viewbox": y_min_viewbox,
            "y_max_viewbox": y_max_viewbox
        })

        curve_track.add_item(pg_plot_item)

        # Si en algún momento se quiere setear el nombre
        #
        # axis = pg_plot_item.getAxis("top")
        #
        # axis.setLabel(graphCurveName + ": " + dbCurveName + logLabel)

        curve_track.layout \
            .addItem(pg_plot_item,
                     row=curve_track.axis_number + 1,
                     col=1,
                     rowspan=1,
                     colspan=2)

    #else:
    #    pg_plot_item = curve_track.last_item()

    if not add_to_plot:
        return

    x_data = x_axis

    if is_log:
        x_data = np.log10(x_axis)

    y_data = y_axis

    if is_y_log:
        y_data = np.log10(y_axis)

    if scatter_curve:
        pen = pg.mkPen(color=getColor(color_name),
                       width=line_width)

        curve = pg.ScatterPlotItem(pen=pen,
                                   symbol=line_marker)

        curve.addPoints(x_data,
                        y_data)

    else:
        pen = pg.mkPen(color=getColor(color_name),
                       style=style,
                       width=line_width)

        curve = pg.PlotDataItem(x=x_data,
                                y=y_data,
                                pen=pen,
                                symbol=line_marker,
                                symbolPen=pen)

    curve_track.add_curve_data({
        "curve_name": curve_name,
        "color_name": color_name,
        "curve": curve,
        "add_axis": add_axis,
        "scatter_curve": scatter_curve,
        "is_log": is_log,
        "is_y_log": is_y_log,
        "is_reverse": is_reverse,
        "x_label": config.get("x_label", ""),
        "cummulative": cummulative,
        "x_axis": x_axis,
        "y_axis": y_axis,
        "style": config.get("line_style", ""),
        "line_marker": config.get("line_marker", "")
    })

    if not add_axis:
        curve_track.first_item() \
            .addItem(curve)


def _append_curve(config,
                  curve_track):
    _add_curve(config,
               curve_track)


def _append_colored_rectangle(config,
                              curve_track):
    rectangle = RectangleComponent(config)

    curve_track.add_rectangle_data({
        "curve_name": f"{RECTANGLE_NAME_PREFIX}{config['curve_name']}",
        "color_name": config["color"],
        "curve": rectangle,
        "x_label": "",
        "cummulative": config["cummulative"]
    })

    if not config.get('add_axis', False):
        curve_track.first_item() \
            .addItem(rectangle)

# Never implemented
"""
def set_custom_ticks(ax, config):
    if config.get("x_axis", None) is None:
        return

    x_axis_values = config["x_axis"][~np.isnan(config["x_axis"])]

    if len(x_axis_values) == 0:
        return

    min_for_axis = get_rounded_float(min(x_axis_values))

    max_for_axis = get_rounded_float(max(x_axis_values))

    # tickLevels = ax.tickSpacing(minVal, maxVal, size)

    values = []

    for i in [25, 50, 75]:
        value = get_rounded_float(min_for_axis + i * 0.01 * (max_for_axis - min_for_axis))

        values.append((value, str(value)))

    ax.setTicks([
        [(min_for_axis, str(min_for_axis)), (max_for_axis, str(max_for_axis))],
        values
    ])
"""


def _add_axis(config,
              curve_track):
    try:
        track_viewbox = curve_track.first_item() \
            .getViewBox()

    # Empty track
    except AttributeError:
        return

    if config.get("x_axis", None) is None and not config.get("blank", False):
        return

    # Custom values: too complex (and unfinished)
    #min_for_axis = get_rounded_float(min(x_axis_values))
    #max_for_axis = get_rounded_float(max(x_axis_values))
    #ax = MinMaxAxis(orientation="top", min_for_axis=min_for_axis, max_for_axis=max_for_axis)
    # x_axis_values = config["x_axis"][~np.isnan(config["x_axis"])]
    # if len(x_axis_values) == 0:
    #    return

    ax = AxisItem(orientation="top")

    # Custom values: too complex (and unfinished, other version)
    #set_custom_ticks(ax, config)

    bounds = {}

    viewbox = pg.ViewBox()

    if not config['blank']:
        if config.get('x_adjusted', False):
            bounds = {
                'x_axis': [config['x_adjusted_min'], config['x_adjusted_max']],
                'y_axis': config['y_axis'],
                'set_x_limits': True
            }

            ax.setRange(config['x_adjusted_min'], config['x_adjusted_max'])

        else:
            bounds = {
                'y_axis': config['y_axis'],
                'x_axis': config['x_axis'],
                'set_x_limits': False
            }
        bounds['y_min_viewbox'] = config.get('y_min_viewbox', None)
        bounds['y_max_viewbox'] = config.get('y_max_viewbox', None)

    # Se usa un viewbox aparte porque si se agrega la curva como siempre,
    # ambos ejes se van a ajustar a una escala que contenga todas las curvas.
    viewbox = adjust_track_viewbox(viewbox,
                                   bounds)

    bounds['set_x_limits'] = False

    viewbox_blank = adjust_track_viewbox(pg.ViewBox(),
                                         bounds)

    viewbox.invertX(config.get('is_reverse', False))

    cummulative = config.get('cummulative',
                             False)

    # If it is not the only axis, adjusting the range will not be compatible with
    # the range of the axis that is used as reference for the scale
    if cummulative:
        if curve_track.get_number_of_real_axies() == 1:
            if config['x_adjusted']:
                x_min = config["x_adjusted_min"]

                x_max = config['x_adjusted_max']

                viewbox.setLimits(xMin=x_min,
                                  xMax=x_max)

            else:
                x_min = min_with_nans(config["x_axis"])

                x_max = max_with_nans(config["x_axis"])

            config["cummulative"] = False

            cummulative = False

            viewbox.setRange(xRange=(x_min, x_max))

            ax.setRange(x_min, x_max)

        else:
            ax.setTicks([])

    # Es necesario además de esto hacer un agregado a la escena porque sino la curva
    # no se dibuja, Se hace más adelante
    curve_track.layout \
        .addItem(ax,
                 row=config['row'],
                 col=2)

    ax.linkToView(viewbox)

    # Comentar esto es parte de lo que se busca: que las curvas
    # que se agreguen den la ilusión de estar superpuestas (en vez de
    # que se ajusten todas a un mismo eje).
    #
    # viewbox.setXLink(track_viewbox)

    curve_track.add_axis(
        CustomAxis(ax, viewbox, config['curve_name'], cummulative, False,
                   config.get('x_adjusted', False), config.get('x_adjusted_min', None),
                   config.get('x_adjusted_max', None))
    )

    padding_label = pg.LabelItem(".", size=BLANK_LABEL_FONT_SIZE, color='w')

    curve_track.add_blank_label(padding_label)

    if config['blank']:
        ax.setPen('w')

        ax.setTextPen('w')

    else:
        # Si en algún momento se quiere setear el nombre
        # ax.setLabel(graphCurveName + ": " + dbCurveName + logLabel)

        ax.setPen(color=config['color'])

        ax.setTextPen(color=config['color'])

        # If there is only one, it must be a real axis (else, there are 0 axes)
        if len(curve_track.axis) == 1:
            # Para el primer eje, sincronizar las líneas griseadas
            track_viewbox.setXLink(viewbox)

        if not cummulative:
            viewbox.addItem(curve_track.get_curve(config['curve_name']))

    y_label = config.get("y_label", "")

    x_label = config.get("x_label", "")

    if len(x_label) != 0:
        ax.setLabel(x_label, **{'font-size': '8pt'})

        r, g, b = get_color_values(config['color_name'])

        ax.labelStyle['color'] = fn.mkPen(color=QColor(r, g, b)) \
                                             .color() \
                                             .name()

    curve_track.layout \
        .addItem(padding_label,
                 row=config['row'],
                 col=1)

    if config.get("is_log", False):
        ax.setLogMode("x")

        viewbox.setLogMode("x", True)

    if not cummulative:
        curve_track.add_track_viewbox(viewbox)


def _add_fill_between_curves_to_track(curve_track, x_data_1, y_data_1, x_data_2, y_data_2, brush, line_name_to_add_fill):
    # Como cada curva tiene su eje x y aparece "superpuesta" en el plot item, para lograr el rellenado
    # entre 2 curvas, una de ellas debe ajustarse a las dimensiones de la otra.
    # La curva 1 se ajusta a las dimensiones de la 2.

    # Algoritmo:
    # Obtener xData1 de line1 y xData2 de line2
    # obtener xData1 normalizado al max y min de xData2
    # crear nuevos plotCurveItem provisorios con xData1 y xData2 (no se agregan al grafico)
    # crear un nuevo FillBetweenItem con las curvas provisorias
    # borrar las curvas provisorias
    # agregar el FillBetweenItem al grafico de line1

    adHocCurve1 = pg.PlotCurveItem(x=x_data_1,
                                   y=y_data_1,
                                   name="adHoc1")

    adHocCurve2 = pg.PlotCurveItem(x=x_data_2,
                                   y=y_data_2,
                                   name="adHoc2")

    fill_item = pg.FillBetweenItem(adHocCurve1,
                                   adHocCurve2,
                                   brush)

    curve_track.add_fill_item(line_name_to_add_fill,
                              fill_item)


def _fill_between_curves(config,
                         curve_track):
    lineName1 = config['curve_name_1']

    lineName2 = config['curve_name_2']

    r, g, b = get_color_values(config['color'])

    brush = QBrush(QColor(r, g, b),
                   get_brush_fill(config.get('fill', "Sólido")))

    curve1 = curve_track.curves[lineName1] \
        .curve

    curve2 = curve_track.curves[lineName2] \
        .curve

    x_data_1, y_data_1 = curve1.getData()

    x_data_2, y_data_2 = curve2.getData()
    
    cummulative = config.get('cummulative',
                             False) 
                  

    #print("Rellena el area entre la curva ", lineName1, " y ", lineName2)

    semi_fill = config.get('semi_fill',
                            False)

    # Curves are not overlapped: they belong to the same viewbox, and are
    # in the same scale.
    if cummulative:
        fill_item = pg.FillBetweenItem(curve1,
                                       curve2,
                                       brush)

        curve_track.first_item() \
            .addItem(fill_item)

    elif semi_fill:
        y_min = max([min(y_data_1), min(y_data_2)])
        y_max = min([max(y_data_1), max(y_data_2)])

        data_1_x = x_data_1.tolist()
        data_1_y = y_data_1.tolist()
        data_2_x = x_data_2.tolist()
        data_2_y = y_data_2.tolist()

        df1 = pd.DataFrame(data = {"x": data_1_x, "y": data_1_y})
        df2 = pd.DataFrame(data = {"x": data_2_x, "y": data_2_y})

        df1 = df1.loc[(df1["y"] >= y_min) & (df1["y"] <= y_max)]
        data_1_x = df1["x"].to_numpy()
        data_1_y = df1["y"].to_numpy()
        df2 = df2.loc[(df2["y"] >= y_min) & (df2["y"] <= y_max)]
        data_2_x = df2["x"].to_numpy()
        data_2_y = df2["y"].to_numpy()
        adHocCurve1 = pg.PlotCurveItem(x=data_1_x,
                                       y=data_1_y,
                                       name="adHoc1")

        adHocCurve2 = pg.PlotCurveItem(x=data_2_x,
                                       y=data_2_y,
                                       name="adHoc2")

        fill_item = pg.FillBetweenItem(adHocCurve1,
                                       adHocCurve2,
                                       brush)

        curve_track.first_item() \
            .addItem(fill_item)

    else:
        x_axis_1 = curve_track.get_curve_axis(lineName1)
        x_axis_2 = curve_track.get_curve_axis(lineName2)

        if (x_axis_1 is None) or (x_axis_2 is None):
            return None

        if x_axis_1.is_x_adjusted() and not x_axis_2.is_x_adjusted():
            x_range_1 = x_axis_1.get_limits()
            x_range_2 = x_axis_2.get_limits()
            xData2 = np.interp(x_data_2,
                           (min(x_range_2), max(x_range_2)),
                           (min(x_range_1), max(x_range_1)))
            _add_fill_between_curves_to_track(curve_track,
                                          xData2, y_data_2,
                                          x_data_1, y_data_1,
                                          brush,
                                          config['curve_name_1'])

        elif x_axis_2.is_x_adjusted():
            x_range_1 = x_axis_1.get_limits()
            x_range_2 = x_axis_2.get_limits()
            xData1 = np.interp(x_data_1,
                           (min(x_range_1), max(x_range_1)),
                           (min(x_range_2), max(x_range_2)))
            _add_fill_between_curves_to_track(curve_track,
                                          xData1, y_data_1,
                                          x_data_2, y_data_2,
                                          brush,
                                          config['curve_name_2'])

        else:
            xData1 = np.interp(x_data_1,
                           (min(x_data_1), max(x_data_1)),
                           (min(x_data_2), max(x_data_2)))
            _add_fill_between_curves_to_track(curve_track,
                                          xData1, y_data_1,
                                          x_data_2, y_data_2,
                                          brush,
                                          config['curve_name_2'])


def _add_scatterplot(config,
                     curve_track):
    plot_item = pg.PlotItem(labels={
        'left': config["left_label"],

        'bottom': config["bottom_label"]
    })

    plot_item.showGrid(x=True,
                       y=True,
                       alpha=0.7)

    plot_item.updateGrid()

    plot_item.setMenuEnabled(False)

    x_axis = config["x_axis"]
    y_axis = config["y_axis"]

    is_log = config.get("is_log", False)

    if is_log:
        plot_item.getAxis("bottom").setLogMode("x")
        plot_item.getViewBox().setLogMode("x", True)
        x_axis = np.log10(x_axis)

    is_y_log = config.get("is_y_log", False)

    if is_y_log:
        plot_item.getAxis("left").setLogMode("y")
        plot_item.getViewBox().setLogMode("y", True)
        y_axis = np.log10(y_axis)

    config.update({
        "x_axis": x_axis,
        "y_axis": y_axis
    })

    scatter = create_track_scatter_plot_item(config)

    try:
        x_min, x_max = min(x_axis[~np.isnan(x_axis)]), max(x_axis[~np.isnan(x_axis)])

        y_min, y_max = min(y_axis[~np.isnan(y_axis)]), max(y_axis[~np.isnan(y_axis)])

    except TypeError:
        x_axis = np.array(x_axis)

        y_axis = np.array(y_axis)

        x_min, x_max = min(x_axis[~np.isnan(x_axis)]), max(x_axis[~np.isnan(x_axis)])

        y_min, y_max = min(y_axis[~np.isnan(y_axis)]), max(y_axis[~np.isnan(y_axis)])

    min_value = min(x_min, y_min) - 0.2 * min(x_min, y_min)

    max_value = max(x_max, y_max) + 0.2 * max(x_max, y_max)

    plot_item.getViewBox() \
        .setLimits(yMin=min_value,
                   yMax=max_value,
                   xMin=min_value,
                   xMax=max_value)

    plot_item.getViewBox() \
        .addItem(scatter)

    if config.get("custom_curve", False):
        plot_item.getViewBox() \
            .addItem(get_line({
                "x_values": config["x_values"],
                "y_values": config["y_values"],
                "is_log": is_log,
                "is_y_log": is_y_log
        }))

    elif config.get("custom_line", False):
        plot_item.getViewBox() \
            .addItem(get_line({
                "is_log": is_log,
                "is_y_log": is_y_log
        }))

    curve_track.add_item(scatter)

    curve_track.layout \
        .addItem(plot_item,
                 row=curve_track.axis_number + 1,
                 col=1)


def _add_legend(curve_track):
    curve_track.add_legend_item()


def _add_new_curve(curve_track,
                   axis_config,
                   config):
    curve_track.add_config(config)

    curve_track.add_axis_config(axis_config)
