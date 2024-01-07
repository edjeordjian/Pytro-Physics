"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

import pyqtgraph as pg

import numpy as np

from constants.pytrophysicsConstants import LINE_MARKER_CONSTANTS, COLORMAP_CONSTANTS

from ui.visual_components.track_handler import create_track_plot_item

from ui.style.LineColors import getColor
from ui.style.LineMarkers import LineMarkers
from ui.style.LineTypes import LineTypes
from ui.style.Colormaps import Colormaps

def add_color_crossplot(config,
                        window):
    '''
    config = {
            'title': 'Título de crossplot',
            'x_axis_title': self.selectedPefCurve,
            'y_axis_title': self.selectedRhoCurve,
            'flex_size': 6,
            'invert_x': False,
            'invert_y': True,
            'log_x': False,
            'log_y': False,
            'scatter_groups': [{                
                'x_axis': self.well.get_df_curve(self.selectedPefCurve),
                'y_axis': self.well.get_df_curve(self.selectedRhoCurve),
                'scatter_name': self.scattername,
                'marker': self.markerCbo.currentText(),
                'fixed_color': self.colorCbo.currentText(),
                'has_z_axis': True,
                'z_axis': self.well.wellModel.get_depth_curve(),
                'z_axis_colormap': "viridis",
                'z_axis_title': self.selectedZAxisCurve,
            } , ...],
            'line_groups': [{
                'x_axis': self.well.get_df_curve(self.selectedPefCurve),
                'y_axis': self.well.get_df_curve(self.selectedRhoCurve),
                'line_name': self.curveName,
                'line_color': self.colorCbo.currentText(),
                'line_style': self.lineType.currentText()
            }, ...],
            'words':[{
                'x': 3,
                'y': 5,
                'name': 'word'
            }]
        }
    '''

    curve_track = window.create_curve_track()

    curve_track.set_scatter(True)

    bounds = {
        'free_axis': True,
        'cummulative': False
    }

    # config['title']
    pg_plot_item = create_track_plot_item(bounds)

    legend = pg_plot_item.addLegend(offset=(10, 10))
    pg_plot_item.hideAxis('top')
    pg_plot_item.showAxis('bottom', True)
    pg_plot_item.showLabel('left', True)
    pg_plot_item.showLabel('bottom', True)
    pg_plot_item.setTitle(config['title'])
    pg_plot_item.getAxis('bottom').setLabel(config['x_axis_title'])
    pg_plot_item.getAxis('left').setLabel(config['y_axis_title'])
    pg_plot_item.getViewBox().setMouseEnabled(x=True,
                                              y=True)
    pg_plot_item.getViewBox().invertX(config.get('invert_x', False))
    pg_plot_item.getViewBox().invertY(config.get('invert_y', True))
    pg_plot_item.setLogMode(config.get('log_x', False), config.get('log_y', False))
    
    # Stub ImageItem, se usa para generar la colorbar pero no se agrega al plotitem
    data = np.fromfunction(lambda i, j: (1+0.3*np.sin(i)) * (i)**2 + (j)**2, (100, 100))
    i1 = pg.ImageItem(image=data)

    colorbars = []

    for scatter_config in config.get('scatter_groups', []):
        marker = scatter_config.get("marker", LINE_MARKER_CONSTANTS["DOT"])
        if marker == LINE_MARKER_CONSTANTS["NONE"]:
            continue
        
        symbol = LineMarkers().getLineMarker(marker)

        if scatter_config.get('has_z_axis', False):
            colormap = Colormaps().getColormap(scatter_config.get("z_axis_colormap",
                                                                  COLORMAP_CONSTANTS["INFERNO"]))
            cm = pg.colormap.get(colormap)
            #cm.reverse()
            n = len(scatter_config["x_axis"])
            colors = map(lambda x: cm.getByIndex(int(x / 256)), range(n+1))
            colors = cm.getStops()
            colorList = cm.getStops()[1]
            z_min = np.min(scatter_config["z_axis"][~np.isnan(scatter_config["z_axis"])])
            z_max = np.max(scatter_config["z_axis"][~np.isnan(scatter_config["z_axis"])])
            colors = list(map(lambda x: 0 if np.isnan(x) else pg.mkColor(colorList[int(((x-z_min)*255)/ (z_max - z_min) ) - 1]), scatter_config["z_axis"]))

            z_axis_title = scatter_config.get("z_axis_title", "Eje Z")

            colorbars.append(pg_plot_item.addColorBar(i1,
                                                      colorMap=colormap,
                                                      values=(z_min, z_max),
                                                      limits=(z_min, z_max),
                                                      interactive=False,
                                                      label = z_axis_title))
            
            # Se crea el scatter y se define inicialmente un brush unico, para que la legenda lo detecte correctamente
            scatter = pg.ScatterPlotItem(brush=cm.getBrush(orientation="horizontal"), pen='k', symbol=symbol, size=10)

        else:
            color = getColor(scatter_config.get("fixed_color", "Negro"))
            colors = list(map(lambda x: color, scatter_config["x_axis"]))
            scatter = pg.ScatterPlotItem(brush=color, pen='k', symbol=symbol, size=10)
        
        # Se agregan los puntos pasando en brush un arreglo con el color que debe tener cada punto segun el colormap (o el color fijo)
        scatter.addPoints(scatter_config["x_axis"], scatter_config["y_axis"], brush=colors)
        #scatter.setSymbol(symbol)
        
        if scatter_config.get("scatter_name", "") != "":
            legend.addItem(scatter, scatter_config["scatter_name"])

        pg_plot_item.getViewBox() \
            .addItem(scatter)

    for line_config in config.get("line_groups", []):
        color = getColor(line_config.get("line_color",
                                         "Negro"))

        style = LineTypes().getLineType(line_config.get("line_style",
                                                        "Solida"))
        
        pen = pg.mkPen(color=color,
                       style=style,
                       width=2)

        line_plotcurveitem = pg.PlotCurveItem(x=line_config["x_axis"],    
                                              y=line_config["y_axis"],
                                              pen = pen)
        if line_config.get('line_name', "") != "":
            legend.addItem(line_plotcurveitem, line_config['line_name'])

        pg_plot_item.getViewBox() \
            .addItem(line_plotcurveitem)

    for word in config.get('words', []):
        word_item = pg.TextItem(word['name'], (50, 50, 50), anchor=(0, 0))
        word_item.setPos(word['x'], word['y'])
        pg_plot_item.getViewBox() \
            .addItem(word_item)

    curve_track.add_item(pg_plot_item)

    curve_track.layout \
        .addItem(pg_plot_item,
                 row=1,
                 col=10,
                 rowspan=1,
                 colspan=1)

    for i in range(len(colorbars)):
        curve_track.layout \
            .addItem(colorbars[i],
                     row=1,
                     col=11 + i,
                     rowspan=1,
                     colspan=1)
