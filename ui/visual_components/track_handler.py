"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

import pyqtgraph as pg

import pyautogui

from constants.pytrophysicsConstants import COLORMAP_CONSTANTS

from constants.numerical_constants import APP_MIN, APP_MAX

from services.tools.logger_service import log_error
from services.tools.number_service import change_ft_mts_list, change_ft_mts

from ui.style.Colormaps import Colormaps

from ui.visual_components.PlotItemWithoutLine import PlotItemWithoutLine


def set_track_size(track, width, height):
    track.setFixedSize(width, height)
    return track


def create_track(layout,
                 track_position,
                 to_replace=None):
    track = pg.GraphicsView()

    # We had a problem using this:
    # track.setCacheMode(pg.GraphicsView.CacheModeFlag.CacheNone)

    track.setBackground('w')

    width, height = pyautogui.size()

    track.setMinimumSize(int(width * 0.2),
                         int(height * 0.7))

    if to_replace:
        # Replace widget no anda bien, seguro es el caché del background
        # Según QtWidgets.pyi, se puede poner CacheNone, pero no sé si
        # es algo bueno
        layout.removeWidget(to_replace)

    layout.insertWidget(track_position,
                        track)
    return track


def adjust_track_viewbox(viewbox,
                         bounds,
                         padding=0.08):
    viewbox.invertY(True)

    # Avoids last numbers on axis from being hid
    #viewbox.enableAutoRange(axis='x')

    viewbox.setMenuEnabled(False)

    viewbox.setDefaultPadding(padding)

    y_axis = bounds.get('y_axis',
                        None)

    x_axis = bounds.get('x_axis',
                        None)
    
    free_axis = bounds.get('free_axis',
                           False)

    y_min_viewbox = bounds.get('y_min_viewbox',
                       None)
    
    y_max_viewbox = bounds.get('y_max_viewbox',
                       None)

    if bounds.get('set_x_limits', False) and not bounds.get('cummulative', False):
        viewbox.setXRange(min(x_axis), max(x_axis))

    if x_axis is not None and y_axis is not None and y_min_viewbox is not None and y_max_viewbox is not None:
        # No se habilita el movimiento sobre el eje x
        # (a pesar de que se está acotando su máximo) debido
        # a la forma en que se logra el rellenado entre curvas.
        viewbox.setMouseEnabled(x=False,
                                y=True)

        viewbox.setLimits(yMin=y_min_viewbox,
                          yMax=y_max_viewbox)

    elif not free_axis:
        # Usado para deshabilitar interaccion con el eje blanc en
        # ambas direcciones (vertical y horizontal) en tracks 
        # con varios ejes
        viewbox.setMouseEnabled(x=False,
                                y=False)

    return viewbox


def create_track_scatter_plot_item(config):
    colormap = Colormaps().getColormap(COLORMAP_CONSTANTS["INFERNO"])

    cm = pg.colormap.get(colormap)

    scatter = pg.ScatterPlotItem(brush=cm.getBrush(orientation="horizontal"), pen='k', size=10)

    scatter.addPoints(config["x_axis"], config["y_axis"])

    return scatter


def create_track_plot_item(config,
                           padding=0.04):
    plot_item = PlotItemWithoutLine()
    
    adjust_track_viewbox(plot_item.getViewBox(),
                         config,
                         padding)

    plot_item.hideAxis('bottom')

    plot_item.setMenuEnabled(False)

    plot_item.showAxis('top')

    add_axis = config.get("add_axis",
                          False)

    # TEST rápido: si esto se muestra, tienen que coincidir
    # los valores con el eje primer eje (aunque no estén completamente alineados).
    # No se utiliza .style['showValues'] = False porque esto interfiere con
    # la alineación vertical cuando se crean ejes blank
    if not add_axis:
        plot_item.getAxis('top') \
            .style['showValues'] = False

    plot_item.getAxis('left') \
        .style['showValues'] = True

    y_label = config.get('y_label', "")

    if len(y_label) != 0:
        plot_item.getAxis("left") \
                 .setLabel(y_label)

    if not config.get('no_grid',
                      False):
        plot_item.showGrid(x=True,
                           y=True,
                           alpha=0.7)

        plot_item.updateGrid()

    if config.get("is_log", False):
        plot_item.getAxis("top").setLogMode("x")
    
    if config.get("is_y_log", False):
        plot_item.getAxis("left").setLogMode("y")

    return plot_item


def get_track_to_update(config,
                        tracks):
    track_name = config['track_name']

    result = list(
        filter(lambda track: track.track_name == track_name,
               tracks)
    )

    if len(result) == 0:
        log_error("No hay un track con nombre: " + track_name)

        return None

    curve_track = result[0]

    curve_track.update = True

    return curve_track


def adjust_depth_in_config(config, depth_curve, old_unit, new_unit):
    if config.get("is_scatter", False):
        return

    if config.get("ephimeral", False) or config.get("ephimeral_to_delete", False):
        if config.get("y_max", -1) > 0:
            config["y_max"] = change_ft_mts(config["y_max"], new_unit)

        if config.get("y_min", -1) > 0:
            config["y_min"] = change_ft_mts(config["y_min"], new_unit)

        if config.get("y_axis", None) is not None:
            config["y_axis"] = change_ft_mts_list(config["y_axis"], new_unit)

    else:
        config["y_axis"] = depth_curve

    if config.get("y_min_viewbox", -1) > 0:
        config["y_min_viewbox"] = change_ft_mts(config["y_min_viewbox"], new_unit)

    if config.get("y_max_viewbox", -1) > 0:
        config["y_max_viewbox"] = change_ft_mts(config["y_max_viewbox"], new_unit)

    y_label = config.get('y_label', "")

    if len(y_label) != 0:
        config["y_label"] = config["y_label"].replace(old_unit.lower(), new_unit.lower())


def free_tracks_viewbox(tracks):
    previous_limits = []

    for track in tracks:
        viewbox = track.first_item().getViewBox()

        y_min, y_max = viewbox.state['limits']["yLimits"][0], viewbox.state['limits']["yLimits"][1]

        linked_views = []

        axies = track.get_every_axis()

        for axis in axies:
            limits = axis.get_axis().linkedView().state["limits"]

            linked_views.append((limits["yLimits"][0],
                                 limits["yLimits"][1]))

        previous_limits.append((y_min, y_max, linked_views))

        for axis in axies:
            axis.get_axis().linkedView().setLimits(yMin=APP_MIN, yMax=APP_MAX)

        viewbox.setLimits(yMin=APP_MIN, yMax=APP_MAX)

    return previous_limits


def set_tracks_viewbox(tracks, previous_limits):
    for i in range(len(tracks)):
        y_min, y_max, axis_limits = previous_limits[i]

        tracks[i].first_item().getViewBox().setLimits(yMin=y_min, yMax=y_max)

        axies = tracks[i].get_every_axis()

        for j in range(len(axies)):
            y_min_ax, y_max_ax = axis_limits[j]

            axies[j].get_axis().linkedView().setLimits(yMin=y_min_ax, yMax=y_max_ax)


def set_tracks_y_range(tracks, y_min, y_max):
    for i in range(len(tracks)):
        tracks[i].first_item().setYRange(y_min, y_max, padding=0.0)
