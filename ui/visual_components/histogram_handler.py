"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

import pyqtgraph as pg

import numpy as np

from services.tools.list_service import list_to_numpy

from ui.visual_components.track_handler import create_track_plot_item

from ui.style.LineColors import getColor

from services.tools.string_service import is_number


def _add_histogram(config, curve_track):
    '''
    config = {
            'title': 'Título de Histograma',
            'x_axis_title': self.selectedCurve,
            'y_axis_title': self.distributionName,
            'flex_size': 6,
            'invert_x': False,
            'invert_y': False,
            'log_x': False,
            'buckets': 40,
            'histogram_groups': [{                
                'values': self.well.get_df_curve(self.selectedCurve),
                'histogram_name': self.histName,
                'color': self.colorCbo.currentText(),
                'alpha': 255,
                'show_accum': True,
                'alpha_accum': 255
            } , ...]
        }
    '''

    curve_track.set_scatter(True)

    bounds = {
        'free_axis': True
    }

    # config['title']
    pg_plot_item = create_track_plot_item(bounds)

    legend = pg_plot_item.addLegend(offset=(10, 10))
    pg_plot_item.hideAxis('top')
    pg_plot_item.showAxis('bottom', True)
    pg_plot_item.showLabel('left', True)
    pg_plot_item.showLabel('bottom', True)
    pg_plot_item.getAxis('bottom').setLabel(config['x_axis_title'])
    pg_plot_item.getAxis('left').setLabel(config['y_axis_title'])
    pg_plot_item.getViewBox().setMouseEnabled(x=True,
                                              y=True)
    pg_plot_item.getViewBox().invertX(config.get('invert_x', False))
    pg_plot_item.getViewBox().invertY(config.get('invert_y', False))
    pg_plot_item.setLogMode(config.get('log_x', False), False)

    for group in config['histogram_groups']:
        group["values"] = list_to_numpy(group["values"])

    vals = config['histogram_groups'][0]['values'][~np.isnan(config['histogram_groups'][0]['values'])]
    min_val = min(vals)
    max_val = max(vals)

    buckets = 40
    buckets_input = config.get('buckets', "40")

    if is_number(buckets_input) and int(buckets_input) > 0:
        buckets = int(buckets_input) + 1

    for histogram_config in config['histogram_groups'][1::]:
        vals = histogram_config['values'][~np.isnan(histogram_config['values'])]
        min_val = min(min(vals), min_val)
        max_val = max(max(vals), max_val)

    for histogram_config in config['histogram_groups']:

        vals = histogram_config['values'][~np.isnan(histogram_config['values'])]

        y,x = np.histogram(vals, bins=np.linspace(min_val, max_val, buckets))

        y = y/len(vals)

        color = getColor(histogram_config.get("color", "Azul"))

        alpha = histogram_config.get('alpha', 150)

        brush = pg.mkBrush(color=np.append(np.array(color), int(alpha)))

        ## Using stepMode="center" causes the plot to draw two lines for each sample.
        ## notice that len(x) == len(y)+1
        hist = pg_plot_item.plot(x, y, stepMode="center", fillLevel=0, fillOutline=True, brush=brush)

        if histogram_config.get("show_accum", False):
            alpha = histogram_config.get('alpha_accum', 200)
            y = np.cumsum(y)
            x = [min_val] + list(x) + [max_val]
            y = [0, 0] + list(y) + [1]
            pen = pg.mkPen(color=np.append(np.array(color), int(alpha)))
            pg_plot_item.plot(x, y, pen=pen)

        if histogram_config.get("histogram_name", "") != "":
            legend.addItem(hist, histogram_config["histogram_name"])

    curve_track.add_item(pg_plot_item)

    curve_track.layout \
        .addItem(pg_plot_item,
                 row=1,
                 col=1,
                 rowspan=1,
                 colspan=1)
