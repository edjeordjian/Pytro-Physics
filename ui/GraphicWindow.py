"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from os import remove

import pyautogui

import numpy as np

from PIL import Image

from PyQt6.QtGui import QAction, QIcon, QFontMetrics

from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QMenuBar, QMenu,
                             QFileDialog, QScrollArea, QVBoxLayout,
                             QHBoxLayout, QLabel, QCheckBox, QPushButton,
                             QComboBox, QGroupBox, QRadioButton, QLineEdit,
                             QWIDGETSIZE_MAX)

from PyQt6.QtCore import QTimer, Qt

from img2pdf import get_layout_fun, convert, px_to_pt

from constants.image_constants import (png_browser_options, pdf_browser_options, pdf_paper_size, ORIGINAL_SIZE,
                                       paper_width_in_cm, scales, IMAGE_WIDTH_LBL, DPIS,
                                       DPIS_LBL, NORMAL_DPI)

from constants.media_constants import VIEW_ICON_ROUTE

from constants.messages_constants import (TAB_ALREADY_EXISTS, TRACK_NAME_ALREADY_EXISTS, KEEP_SCALE_ERROR,
                                          TRACK_DOES_NOT_EXIST)

from constants.numerical_constants import MINIMUM_FLOAT

from constants.tab_constants import EVERY_TAB

from constants.views_constants import GRAPHIC_WINDOW_VIEW_ID

from model.CurveTrack import CurveTrack

from services.exporter_service import export_png_file

from services.tools.string_service import is_number

from model.EphimeralTrackRegister import EphimeralTrackRegister

from services.tools.list_service import get_sublist_and_complement, get_uniques, flat_map

from ui.ScrollableWidget import ScrollableWidget

from ui.popUps.loading_handler import loading_pop_up

from ui.visual_components.combo_handler import add_dictionary_to_combo

from ui.visual_components.crossplot_handler import _add_color_crossplot

from ui.visual_components.data_menu_handler import add_option_to_menu, load_view, save_view

from ui.visual_components.drawer_handler import (_add_legend, _add_new_curve, _add_curve, _add_axis,
                                                 _append_curve, _fill_between_curves, _add_scatterplot,
                                                 _append_colored_rectangle)

from ui.visual_components.histogram_handler import _add_histogram

from ui.visual_components.track_handler import (get_track_to_update, free_tracks_viewbox,
                                                set_tracks_viewbox, set_tracks_y_range)

from constants.general_constants import (ADD_CURVE_ACTION, APPEND_CURVE_ACTION, AXIS_ACTION, FILL_ACTION,
                                         LEGEND_ACTION, SCATTERPLOT_ACTION, TRACK_NAMES, COLOR_CROSSPLOT_ACTION,
                                         HISTOGRAM_ACTION, FEETS_LBL, METERS_LBL, number_of_decimals,
                                         LAYOUT_LEFT_PADDING,
                                         LAYOUT_BOTTOM_PADDING, X_PADDING_IMAGES, Y_PADDING_IMAGES, GENERIC_WINDOW_NAME,
                                         X_EXPORT_DELTA, X_EXPORT_DELTA_2, LOADING_LBL, APPEND_RECTANGLE)

from ui.style.LineColors import getColor

from ui.popUps.InfoWindow import InfoWindow

from ui.popUps.alertWindow import AlertWindow

from ui.visual_components.MultiComboBox import MultiComboBox

from ui.visual_components.track_handler import set_track_size

from services.image_service import pt_to_px, px_to_m, px_to_ft, get_scale_format

from functools import reduce

import config as app_config

import pyqtgraph as pg

VISUALIZATION = 'visualization'


class GraphicWindow(ScrollableWidget):
    def __init__(self, tab_serialization_function, tab_set_function, get_depth_unit,
                 tab_update_fn=None, view_id=GRAPHIC_WINDOW_VIEW_ID, 
                 stand_alone=False, title=GENERIC_WINDOW_NAME, get_depth_range=(lambda : [])):
        super().__init__(QHBoxLayout())

        self.view_id = view_id

        self.timer = QTimer()

        self.timer.setInterval(1000)

        self.timer.timeout.connect(self.refresh)

        self.menuBar = QMenuBar()

        self.exportAction = QAction("Exportar",
                                    self)

        self.exportAction.triggered \
            .connect(self.export)

        self.menuBar \
            .addAction(self.exportAction)

        self.view_menu = QMenu('Vista')

        add_option_to_menu(self,
                           self.view_menu,
                           'media/up_arrow.png',
                           'Cargar',
                           lambda: load_view(self, tab_update_fn=tab_update_fn))

        add_option_to_menu(self,
                           self.view_menu,
                           'media/down_arrow.png',
                           'Guardar',
                           lambda x: save_view(self))

        self.menuBar.addMenu(self.view_menu)

        self.layout.setMenuBar(self.menuBar)

        self._handleConfig = {
            ADD_CURVE_ACTION: lambda config,
                                     track: _add_curve(config,
                                                       track),

            AXIS_ACTION: lambda config,
                                track: _add_axis(config,
                                                 track),

            APPEND_CURVE_ACTION: lambda config,
                                        track: _append_curve(config,
                                                             track),

            APPEND_RECTANGLE: lambda config,
                                     track: _append_colored_rectangle(config,
                                                                      track),

            FILL_ACTION: lambda config,
                                track: _fill_between_curves(config,
                                                            track),

            SCATTERPLOT_ACTION: lambda config,
                                       track: _add_scatterplot(config,
                                                               track),

            COLOR_CROSSPLOT_ACTION: lambda config, track: _add_color_crossplot(config, track),

            HISTOGRAM_ACTION: lambda config, track: _add_histogram(config, track)
        }

        self.get_depth_unit = get_depth_unit

        self.layout.setMenuBar(self.menuBar)

        self.curve_tracks = []

        self.stand_alone = stand_alone

        self.ephimeral_tracks = set()

        self.ephimeral_to_delete = set()

        self.get_tab_serialization = tab_serialization_function

        self.set_tabs = lambda tabs: tab_set_function(tabs)

        self._init_scroll_area(int(app_config.screen_width / 2 + 9),
                               31,
                               app_config.window_width,
                               app_config.window_height,
                               title)

        if tab_update_fn is not None:
            self.tab_update_fn = tab_update_fn

        self.get_depth_range = get_depth_range

    def get_first_track_with_curves(self,
                                    tracks=None):
        if tracks is None:
            tracks = self.curve_tracks

        for track in tracks:
            if track.first_item_with_viewbox() is not None:
                return track

        return None

    def get_axis_config(self,
                        config):
        color_name = config.get("color",
                                "Negro")

        color = getColor(color_name)

        x_label = config.get("x_label",
                             "")

        y_label = config.get("y_label",
                             "")

        cummulative = config.get('cummulative',
                                 False)

        config["is_reverse"] = config.get("is_reverse",
                                          False)

        # An error ocurrs if this is not a new object
        return {
            'curve_name': config['curve_name'],

            'color': color,

            'color_name': color_name,

            'action': AXIS_ACTION,

            'blank': False,

            "is_reverse": config.get("is_reverse", False),

            'x_axis': config['x_axis'],

            'y_axis': config['y_axis'],

            'x_label': x_label,

            'y_label': y_label,

            'cummulative': cummulative,

            "is_log": config.get("is_log", False),

            'x_adjusted': config.get('x_adjusted', False),

            'x_adjusted_min': config.get("x_adjusted_min", ""),

            'x_adjusted_max': config.get("x_adjusted_max", "")
        }

    # Not idempotent
    # Affects a single track
    # Preconditions: track has been already created
    def add_legend(self,
                   config):
        self.get_curve_track(config['track_name']) \
            .add_legend(config)

    # Idempotent
    # Affects a single track
    def add_scatterplot(self,
                        config):
        existing_tracks = list(
            filter(lambda track: track.tab_name == config["tab_name"],
                   self.curve_tracks)
        )

        result = list(
            filter(lambda track: track.track_name == config["track_name"],
                   existing_tracks)
        )

        # This is different from _add_curve because it has
        # NO SUPPORT for adding scatterplots from the main menu, or
        # adding padding axes (there nothing to sync vertically!)
        if len(result) != 0:
            curve_track = result[0]

            curve_track.add_config(config)

            self.layout.removeWidget(curve_track.track)

        else:
            curve_track = self.create_curve_track(config["tab_name"],
                                                  config["track_name"],
                                                  self.get_last_idx(existing_tracks))

            if curve_track is None:
                return

            curve_track.set_scatter(True)

        config["action"] = SCATTERPLOT_ACTION

        curve_track.add_config(config)

    # Imported from legacy code
    def add_histogram(self, config):
        self.remove_ephimeral_tracks(config['tab_name'])

        config["curve_name"] = config["title"]

        config["action"] = HISTOGRAM_ACTION

        self.set_ephimeral_track(config['title'],
                                 config['tab_name'])

        curve_track = self.create_curve_track(config['tab_name'],
                                              config['title'],
                                              self.get_last_idx(self.curve_tracks),
                                              True)

        curve_track.add_config(config)

    # Imported from legacy code
    def add_color_crossplot(self, config):
        track_name = config["title"]

        config["curve_name"] = config["title"]

        config["action"] = COLOR_CROSSPLOT_ACTION

        result = list(
            filter(lambda track: track.track_name == track_name,
                   self.curve_tracks)
        )

        if len(result) == 0:
            curve_track = self.create_curve_track(config['title'],
                                                  config['title'],
                                                  self.get_last_idx(self.curve_tracks),
                                                  False)

            if curve_track is None:
                return

            curve_track.add_config(config)

        else:
            curve_track = result[0]

            self.layout.removeWidget(curve_track.track)

            curve_track.add_config(config)

    # For calculations    # Idempotent
    # May affect any track because of the blanc axis (For vertical sync)
    def add_curve(self,
                  config):
        tab_name = config.get('tab_name',
                              VISUALIZATION)

        track_name = config['track_name']

        config["action"] = ADD_CURVE_ACTION

        axis_config = self.get_axis_config(config)

        existing_tracks = list(
            filter(lambda track: track.tab_name == tab_name,
                   self.curve_tracks)
        )

        result = list(
            filter(lambda track: track.track_name == track_name,
                   existing_tracks)
        )

        # New curve with no track
        if len(result) == 0:
            if config.get("cummulative", False):
                return KEEP_SCALE_ERROR

            curve_track = self.create_curve_track(tab_name,
                                                  track_name,
                                                  self.get_last_idx(existing_tracks))

            if curve_track is None:
                return TRACK_DOES_NOT_EXIST

            _add_new_curve(curve_track,
                           axis_config,
                           config)
        
        else:
            curve_track = result[0]

            if config.get("cummulative", False) and \
                    not curve_track.can_be_cummulative(config["curve_name"]):
                    return KEEP_SCALE_ERROR

            # Existing curve
            if curve_track.get_curve(config["curve_name"]) is not None:
                self.layout.removeWidget(curve_track.track)

                curve_track.add_config(config)

                # if not cummulative:
                curve_track.replace_axis_config(axis_config)

            # Empty track or new curve with existing track
            else:
                _add_new_curve(curve_track,
                            axis_config,
                            config)
                
        return ""

    # ** For free drawing ***
    # Not idempotent
    # May affect any track because of the blanc axis (For vertical sync)
    # Pre-condition: track has been created
    def append_curve(self,
                     config):
        curve_track = get_track_to_update(config,
                                          self.curve_tracks)

        curve_track.delete_curve_if_existing(config["tab_name"],
                                             config["curve_name"])

        config["action"] = APPEND_CURVE_ACTION

        config['add_to_plot'] = True

        curve_track.add_config(config)

        add_axis = config.get('add_axis',
                              False)

        if add_axis:
            axis_config = self.get_axis_config(config)

            curve_track.add_axis_config(axis_config)

    def get_last_idx(self,
                     existing_tracks):
        if len(existing_tracks) != 0:
            return self.curve_tracks.index(existing_tracks[len(existing_tracks) - 1]) + 1

        return len(self.curve_tracks)

    # Para la pantalla de edición libre (puede tocar cualquier track)
    # Es idempotente
    # Solo debería afectar a un track
    # Precondición: el track ya está creado
    def add_fill_between_curves(self,
                                config):
        if config['curve_name_1'] == '' or config['curve_name_2'] == '':
            return

        curve_track = get_track_to_update(config,
                                          self.curve_tracks)

        config["action"] = FILL_ACTION

        curve_track.add_fill_config(config)

    # It is not idempotent if there is a fill to delete.
    # It should affect only one track.
    # Precondition: the track has already been created.
    def remove_fill_between_curves(self,
                                   config):
        get_track_to_update(config,
                            self.curve_tracks) \
            .remove_fill_config(config)

    def add_colored_rectangle(self,
                              config):
        curve_track = get_track_to_update(config,
                                          self.curve_tracks)

        config["action"] = APPEND_RECTANGLE

        config['add_to_plot'] = True

        curve_track.add_rectangle_config(config)

        add_axis = config.get('add_axis',
                              False)

        if add_axis:
            axis_config = self.get_axis_config(config)

            curve_track.add_axis_config(axis_config)

    # These have sepparated method because deleting ephimerals
    # when drawing on EVERY track (at draw_tracks) may delete ephimerals
    # from other tabs (which should not be deleted)
    def set_ephimeral_to_delete(self, tab_name):
        tracks = list(
            filter(lambda t: t.tab_name == tab_name,
                   self.curve_tracks)
        )

        for track in tracks:
            track.set_ephimeral_to_delete()

    def remove_ehphimerals(self, tab_name):
        tracks = list(
            filter(lambda t: t.tab_name == tab_name,
                   self.curve_tracks)
        )

        for track in tracks:
            track.remove_ehpimeral_to_delete()

    def draw_tracks(self,
                    tab_name):
        self._add_blank_axis_configs()

        depth_range = self.get_depth_range()

        update_every_tab = tab_name == EVERY_TAB

        if update_every_tab:
            tracks_to_update = self.curve_tracks

        else:
            # The tab is used to avoid rebuilding everything
            # Could it be necessary to update anything beyond the ones in the tab? (update or tab_name??)
            tracks_to_update = list(
                filter(lambda t: t.update and t.tab_name == tab_name,
                       self.curve_tracks)
            )

            # Ephimeral curves
            for track in tracks_to_update:
                track.remove_ehpimeral_to_delete()

            # For fixing edge case in thickness tab
            # Ephimeral tracks
            # self.remove_ephimeral_tracks(tab_name)

        for track in tracks_to_update:
            track_index = self.curve_tracks \
                .index(track)

            track.initTrack(track_index, depth_range)

            for config in track.get_configs_list() + track.get_rectangle_config_list():
                self._handleConfig[config['action']](config,
                                                     track)

            axis_configs, blank_axis_configs = track.get_axis_configs_and_blanks()

            total_axis_configs = axis_configs + blank_axis_configs

            for i in range(
                        len(total_axis_configs)
                    ):
                action = total_axis_configs[i]['action']

                total_axis_configs[i]['row'] = i + 1

                self._handleConfig[action](total_axis_configs[i],
                                           track)

            for config in track.fill_configs:
                self._handleConfig[config['action']](config,
                                                     track)

            if track.legend is not None:
                _add_legend(track)

            track.end_update()

        if self._remove_blank_axis_configs():
            self.draw_tracks(EVERY_TAB)

        if not update_every_tab:
            for track in tracks_to_update:
                track.set_ephimeral_to_delete()

            self.set_tracks_to_delete(tracks_to_update)

        # Vertical sync must remain no matter which tracks are modified
        self.sync_tracks()

        if not self.isVisible():
            self.show()

    def sync_tracks(self):
        scatters, normal_curves = get_sublist_and_complement(self.curve_tracks,
                                                             lambda track: track.is_scatter())

        self._update_vertical_sync(normal_curves)

        self._update_sync_scatters(scatters)

    def _update_sync_scatters(self,
                              scatters):
        if len(scatters) == 0:
            return

        base_viewbox = scatters[0].items[0].getViewBox()

        for i in range(1, len(scatters)):
            viewbox_to_sync = list(map(lambda item: item.getViewBox(),
                                       scatters[i].items))

            for viewbox in viewbox_to_sync:
                viewbox.linkView(viewbox.XAxis, base_viewbox)

                viewbox.linkView(viewbox.YAxis, base_viewbox)

    def _update_vertical_sync(self,
                              tracks):
        first_track = self.get_first_track_with_curves(tracks)

        if first_track is None:
            return

        #tracks_to_sync = list(filter(lambda t: t != first_track,
        #                             tracks))

        for track in tracks:
            viewbox_to_sync = list(map(lambda axis: axis.viewbox,
                                       track.axis))

            viewbox_to_sync += list(map(lambda item: item.getViewBox(),
                                        track.items))

            for viewbox in viewbox_to_sync:
                viewbox.setYLink(first_track.get_first_viewbox())

    def _remove_blank_axis_configs(self):
        number_of_axis = set(
                map(lambda track: track.axis_number,
                    self.curve_tracks)
            )

        # New axies do not count!
        if 0 in number_of_axis:
            number_of_axis.remove(0)

        run_again = False

        for track in self.curve_tracks:
            while track.axis_number > CurveTrack.get_max_axis():
                track.remove_blank_axis()

                run_again = True

        return run_again

    def _add_blank_axis_configs(self):
        tracks_to_add_blank = list(
            filter(lambda t: t.is_blank_axis_compatible(),
                   self.curve_tracks)
        )

        for track in tracks_to_add_blank:
            while track.axis_number < CurveTrack.get_max_axis():
                axis_config = {
                    'action': AXIS_ACTION,
                    'blank': True,
                    'curve_name': 'blank'
                }

                track.add_axis_config(axis_config)

    def get_tab_names(self):
        return list(map(lambda t: t.get_tab_name(),
                        self.curve_tracks))

    def get_track_titles(self):
        return list(map(lambda t: t.get_title_name(),
                        self.curve_tracks))

    def get_view_id(self):
        return self.view_id

    def create_blank_track(self,
                           tab_name,
                           track_name):
        existing_tracks = list(
            filter(lambda track: track.tab_name == tab_name,
                   self.curve_tracks)
        )

        self.create_curve_track(tab_name,
                                track_name,
                                self.get_last_idx(existing_tracks))

    def create_curve_track(self, tab_name, track_name, insert_idx=-1,
                           title=True):
        if insert_idx < 0:
            if tab_name in self.get_tab_names() or tab_name in TRACK_NAMES:
                AlertWindow(TAB_ALREADY_EXISTS)

                return None

            insert_idx = len(self.curve_tracks)

            if track_name in self.get_track_titles():
                AlertWindow(f"{track_name} {TRACK_NAME_ALREADY_EXISTS}")

                return None

        curve_track = CurveTrack(tab_name, track_name, self.layout, title,
                                 self.stand_alone)

        self.curve_tracks \
            .insert(insert_idx,
                    curve_track)

        return curve_track

    def remove_curve_track(self,
                           track_name):
        tracks_to_remove = list(
            filter(lambda track: track.track_name == track_name,
                   self.curve_tracks)
        )

        if len(tracks_to_remove) == 0:
            return

        if len(tracks_to_remove) > 1:
            print("Error: no debería haber más de un track con el mismo nombre")

        self.remove_track_item(tracks_to_remove[0])

    def remove_track_if_exists(self, track_names):
        current_track_names = list(map(lambda track: track.track_name, self.curve_tracks))
        for track_name in track_names:
            if track_name in current_track_names:
                self.remove_curve_track(track_name)

    def remove_every_track(self):
        for track in list(self.curve_tracks):
            self.remove_track_item(track)

    def remove_tracks(self, tab):
        for track in self.get_curve_tracks(tab):
            self.remove_track_item(track)

    def remove_track_item(self, track_to_remove):
        for config in track_to_remove.get_configs_list():
            track_to_remove.delete_curve_config(config["curve_name"])

        self.layout \
            .removeWidget(track_to_remove.track)

        track_to_remove.track.close()

        track_to_remove.track = None

        self.curve_tracks.remove(track_to_remove)

        self.sync_tracks()

    def get_curve_tracks(self, tab=None):
        if tab is None:
            return self.curve_tracks

        return list(
            filter(lambda t: t.tab_name == tab,
                   self.curve_tracks)
        )

    def get_curve_track(self, track_name):
        return next(filter(lambda t: t.track_name == track_name,
                           self.curve_tracks))

    def refresh(self):
        print("Generic graph refresh")

        if self.isMaximized():
            self.showNormal()
            self.showMaximized()
        else:
            self.resize(self.width() + 1, self.height() + 1)
            self.resize(self.width() - 1, self.height() - 1)

    def export(self):
        self.exportWindow = QWidget()
        self.exportWindowLayout = QVBoxLayout()
        self.exportWindowLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.exportDepthGrpBox = QGroupBox("Rango del eje vertical")
        self.exportDepthLayout = QVBoxLayout()

        self.exportCurrentDepthRb = QRadioButton("Tomar el rango visible actual")
        self.exportFullDepthRb = QRadioButton("Tomar el rango maximo total")
        self.exportCustomDepthRb = QRadioButton("Tomar rango personalizado")

        self.exportCurrentDepthRb.toggled.connect(self.exportDepthSelection)
        self.exportFullDepthRb.toggled.connect(self.exportDepthSelection)
        self.exportCustomDepthRb.toggled.connect(self.exportDepthSelection)

        self.exportCustomDepthMinLE = QLineEdit()
        self.exportCustomDepthMinLE.setPlaceholderText("Valor mínimo del eje vertical")
        self.exportCustomDepthMinLE.setEnabled(False)
        self.exportCustomDepthMaxLE = QLineEdit()
        self.exportCustomDepthMaxLE.setPlaceholderText("Valor máximo del eje vertical")
        self.exportCustomDepthMaxLE.setEnabled(False)

        self.exportCurrentDepthRb.setChecked(True)

        self.exportDepthLayout.addWidget(self.exportCurrentDepthRb)
        self.exportDepthLayout.addWidget(self.exportFullDepthRb)
        self.exportDepthLayout.addWidget(self.exportCustomDepthRb)
        self.exportDepthLayout.addWidget(self.exportCustomDepthMinLE)
        self.exportDepthLayout.addWidget(self.exportCustomDepthMaxLE)

        self.exportDepthGrpBox.setLayout(self.exportDepthLayout)

        self.exportScaleLabel = QLabel("Seleccion Escala")
        self.exportScaleDefaultCb = QCheckBox("Usar escala por defecto")
        self.exportScaleCbo = QComboBox()
        self.exportScaleCbo.addItems(scales)

        self.dpi_lbl = QLabel(DPIS_LBL)
        self.dpi_cbo = QComboBox()
        add_dictionary_to_combo(self.dpi_cbo, DPIS)

        self.exportScaleCbo.setEnabled(False)
        self.exportScaleDefaultCb.stateChanged.connect(self.updateScaleSelection)
        self.exportScaleDefaultCb.setChecked(True)

        if not self.stand_alone:
            self.exportWindowLayout.addWidget(self.exportDepthGrpBox)
            self.exportWindowLayout.addWidget(self.exportScaleLabel)
            self.exportWindowLayout.addWidget(self.exportScaleDefaultCb)
            self.exportWindowLayout.addWidget(self.exportScaleCbo)
            self.exportWindowLayout.addWidget(self.dpi_lbl)
            self.exportWindowLayout.addWidget(self.dpi_cbo)

        else:
            self.exportWindowLayout.addWidget(QLabel(""))
            self.exportWindowLayout.addWidget(QLabel(""))
            self.exportWindowLayout.addWidget(QLabel(""))

        self.exportTracksLabel = QLabel("Seleccion Tracks")
        self.exportTracksCbo = MultiComboBox()
        track_names = [track.track_name for track in self.curve_tracks]
        self.exportTracksCbo.addItems(track_names)
        self.exportAllTracksCb = QCheckBox("Exportar todos los Tracks")
        self.exportAllTracksCb.stateChanged.connect(self.updateExportAllTracks)

        self.exportWindowLayout.addWidget(self.exportTracksLabel)
        self.exportWindowLayout.addWidget(self.exportTracksCbo)
        self.exportWindowLayout.addWidget(self.exportAllTracksCb)

        self.exportTypeGrpBox = QGroupBox("Tipo de Archivo")
        self.exportTypeLayout = QVBoxLayout()
        self.exportPNGRb = QRadioButton("Exportar como PNG")
        self.exportPDFRb = QRadioButton("Exportar como PDF")
        self.exportPDFPaperSizeCbo = QComboBox()

        for paperSize in pdf_paper_size.keys():
            self.exportPDFPaperSizeCbo.addItem(paper_width_in_cm[paperSize], paperSize)

        self.exportPDFPaperSizeCbo.setCurrentIndex(0)
        self.exportButton = QPushButton("Exportar")

        self.exportPNGRb.setChecked(True)
        self.exportPDFPaperSizeCbo.setEnabled(False)
        self.exportPNGRb.toggled.connect(self.exportTypeSelection)
        self.exportPDFRb.toggled.connect(self.exportTypeSelection)
        self.exportButton.clicked.connect(
            lambda checked: self.exportToSelectedFile()
        )

        self.exportTypeLayout.addWidget(self.exportPNGRb)
        self.exportTypeLayout.addWidget(self.exportPDFRb)
        self.exportTypeLayout.addWidget(QLabel(IMAGE_WIDTH_LBL))
        self.exportTypeLayout.addWidget(self.exportPDFPaperSizeCbo)
        self.exportTypeLayout.addWidget(self.exportButton)
        self.exportTypeGrpBox.setLayout(self.exportTypeLayout)
        self.exportWindowLayout.addWidget(self.exportTypeGrpBox)

        self.exportWindow.setLayout(self.exportWindowLayout)

        self.exportWindow.setWindowTitle("Exportar")

        width, height = pyautogui.size()

        export_window_width = int(width / 6)

        export_window_height = int(height - height * 0.6)

        self.exportWindow.setGeometry(int(width / 2 - export_window_width + 100),
                                      int(height / 2 - export_window_height + 100),
                                      export_window_width,
                                      export_window_height)

        self.exportWindow.setWindowIcon(QIcon(VIEW_ICON_ROUTE))

        self.exportWindow.show()

    def exportDepthSelection(self):
        self.exportCustomDepthMinLE.setEnabled(self.exportCustomDepthRb.isChecked())
        self.exportCustomDepthMaxLE.setEnabled(self.exportCustomDepthRb.isChecked())

    def exportTypeSelection(self):
        self.exportPDFPaperSizeCbo.setEnabled(self.exportPDFRb.isChecked())

    def exportToSelectedFile(self):
        if not self.exportAllTracksCb.isChecked():
            selected_tracks = list(filter(lambda track: track.track_name in self.exportTracksCbo.currentOptions(),
                                          self.curve_tracks))

            if len(selected_tracks) == 0:
                AlertWindow("No hay tracks seleccionados para exportar")
                return None

        if self.exportPDFRb.isChecked():
            file_name, _ = QFileDialog.getSaveFileName(self,
                                                       pdf_browser_options['header'],
                                                       pdf_browser_options['default_name'],
                                                       pdf_browser_options['extension'])

            loading_pop_up(LOADING_LBL,
                           lambda: self.export_to_pdf(file_name))

        else:
            file_name, _ = QFileDialog.getSaveFileName(self,
                                                       png_browser_options['header'],
                                                       png_browser_options['default_name'],
                                                       png_browser_options['extension'])

            loading_pop_up(LOADING_LBL,
                           lambda: self.export_to_pngs(file_name))

    def updateScaleSelection(self):
        self.exportScaleCbo.setEnabled(not self.exportScaleDefaultCb.isChecked())

    def updateExportAllTracks(self):
        self.exportTracksCbo.setEnabled(not self.exportAllTracksCb.isChecked())

    def export_header_png(self,
                          file_path,
                          strings,
                          min_width):

        if len(strings) == 0:
            return None

        self.header_item = pg.GraphicsView()
        self.header_item.setBackground('w')
        self.header_item_layout = pg.GraphicsLayout()
        self.header_item.setCentralWidget(self.header_item_layout)
        self.label_items = []
        header_font = pg.LabelItem("DUMMY",size='12pt',color='#000000').font()
        header_font_metrics = QFontMetrics(header_font)
        header_height = header_font_metrics.height()
        widths = [min_width]
        for i in range(len(strings)):
            self.label_items.append(pg.LabelItem(strings[i],
                                                         size='12pt',
                                                         color='#000000'))
            self.header_item_layout.addItem(self.label_items[i],
                                            row=i,
                                            col=1)
            widths.append(header_font_metrics.horizontalAdvance(strings[i]))

        total_header_height = int((header_height + 2) * len(strings))
        header_width = max(widths)
        set_track_size(self.header_item, int(header_width), total_header_height)
        self.header_item.show()
        new_png_file_name = export_png_file(self.header_item_layout,
                                                file_path,
                                                0)

        self.header_item.close()

        return new_png_file_name

    def export_tracks_to_pngs(self, file_name, selected_tracks, min_y_axis, max_y_axis, header = True, minimum_width = None, max_depth = None, print_scale = True):
        pngs = []

        #scatters, selected_tracks = get_sublist_and_complement(selected_tracks,
        #                                                     lambda track: track.is_scatter())

        items = [track.layout for track in selected_tracks]

        track_items = reduce(list.__add__, [track.items for track in selected_tracks])

        for i in range(len(selected_tracks)):
            if self.exportPDFRb.isChecked() and self.exportPDFPaperSizeCbo.currentData() != ORIGINAL_SIZE:
                selected_tracks[i].track.setMinimumSize(1, 1)

                img_width = pt_to_px(pdf_paper_size[self.exportPDFPaperSizeCbo.currentData()][0], self.dpi_cbo.currentData())

                track_width = int(img_width / len(selected_tracks))

                selected_tracks[i].minimize_title(track_width, self.dpi_cbo.currentData())

                selected_tracks[i].track.setMaximumWidth(track_width)

            item = track_items[i]

            if header:
                item = selected_tracks[i].layout

            else:
                selected_tracks[i].set_lateral_label_content(" ")

            depth_height = selected_tracks[i].items[0].getAxis("left").boundingRect().height()

            depth_range_max = selected_tracks[i].items[0].getAxis("left").range[0]

            depth_range_min = selected_tracks[i].items[0].getAxis("left").range[1]

            selected_tracks[i].items[0].setYRange(float(min_y_axis), float(max_y_axis), padding=0.0)
            original_depth_range_max = depth_range_max
            original_depth_range_min = depth_range_min
            depth_range_max = max(selected_tracks[i].items[0].getAxis("left").range)
            depth_range_min = min(selected_tracks[i].items[0].getAxis("left").range)

            depth_unit = self.get_depth_unit()

            scale = None

            adjusted_depth_height = 0

            if print_scale:

                if depth_unit == METERS_LBL:
                    adjusted_depth_height = px_to_m(depth_height, self.dpi_cbo.currentData())

                elif depth_unit == FEETS_LBL:
                    adjusted_depth_height = px_to_ft(depth_height, self.dpi_cbo.currentData())

                depth_range_size = depth_range_max - depth_range_min

                scale = get_scale_format(adjusted_depth_height / depth_range_size)

            new_png_file_name = export_png_file(item,
                                                file_name,
                                                i)

            selected_tracks[i].items[0].setYRange(original_depth_range_min, original_depth_range_max, padding=0.0)

            #item.getViewBox().setDefaultPadding(original_padding)

            pngs.append(new_png_file_name)

            #TODO: crop
            #if max_depth is not None and float(max_depth) < float(max_y_axis):
            #    proportion_to_crop = (float(max_y_axis) - float(max_depth)) / (float(max_y_axis) - float(min_y_axis))
            #    depth_height_to_crop = depth_height * proportion_to_crop
            #    track_image = Image.open(pngs[i])
            #    cropped_image = track_image.crop((0, 0, track_image.width, track_image.height - depth_height_to_crop))
            #    track_image.close()
            #    cropped_image.save(pngs[i])
            #    cropped_image.close()

            if self.exportPDFRb.isChecked() and self.exportPDFPaperSizeCbo.currentData() != ORIGINAL_SIZE:
                selected_tracks[i].track.setMaximumWidth(QWIDGETSIZE_MAX)
                width, height = pyautogui.size()

                selected_tracks[i].track.setMinimumSize(int(width * 0.2),
                                                        int(height * 0.7))

                selected_tracks[i].restore_title_text()

            if len(new_png_file_name) == 0:
                AlertWindow("No se pudo exportar el archivo.")

                return None, None, None, None

        image = Image.open(pngs[0])
        image_width = image.width
        image.close()

        path_png_only_tracks = self.combine_pngs(pngs,
                                 file_name[0:-4] + "_horizontal.png",
                                 False,
                                 header,
                                 minimum_width)

        return path_png_only_tracks, adjusted_depth_height, scale, image_width


    def export_to_pngs(self,
                       file_name,
                       show_popup=True):
        if len(file_name) == 0:
            return None, None, None

        # exporters.PrintExporter
        if '.png' not in file_name:
            file_name += '.png'

        selected_tracks = self.curve_tracks

        if not self.exportAllTracksCb.isChecked():
            selected_tracks = list(filter(lambda track: track.track_name in self.exportTracksCbo.currentOptions(), self.curve_tracks))

        vertical_padding=0

        #if (self.exportCustomDepthMinLE.isEnabled() and
        #        is_number(self.exportCustomDepthMinLE.text()) and
        #        self.exportCustomDepthMaxLE.isEnabled() and
        #        is_number(self.exportCustomDepthMaxLE.text())):
        #        selected_tracks[i].items[0].setYRange(float(self.exportCustomDepthMinLE.text()), float(self.exportCustomDepthMaxLE.text()), padding=0.0)
        #        aux_viewbox = pg.ViewBox()
        #        padding = aux_viewbox.suggestPadding(selected_tracks[0].items[0].getAxis("left"))


        there_are_scatters_to_print = reduce(lambda x, y: x or y, list(map(lambda track: track.is_scatter(), selected_tracks)))
        print_scale = True
        if there_are_scatters_to_print:
            print_scale = False
        #scatters, selected_tracks = get_sublist_and_complement(selected_tracks,
        #                                                     lambda track: track.is_scatter())

        depth_range_max = max(selected_tracks[0].items[0].getAxis("left").range)
        depth_range_min = min(selected_tracks[0].items[0].getAxis("left").range)

        original_depth_range_max = depth_range_max
        original_depth_range_min = depth_range_min
        viewbox = selected_tracks[0].first_item().getViewBox()
        y_min, y_max = viewbox.state['limits']["yLimits"][0], viewbox.state['limits']["yLimits"][1]
        if self.exportFullDepthRb.isChecked():
            depth_range_min = y_min
            depth_range_max = y_max

        elif self.exportCustomDepthRb.isChecked():
            if is_number(self.exportCustomDepthMinLE.text()) and \
               is_number(self.exportCustomDepthMaxLE.text()) and \
               float(self.exportCustomDepthMinLE.text()) < float(self.exportCustomDepthMaxLE.text()) and \
               float(self.exportCustomDepthMaxLE.text()) < y_max and \
               float(self.exportCustomDepthMinLE.text()) > y_min:
                depth_range_min = float(self.exportCustomDepthMinLE.text())
                depth_range_max = float(self.exportCustomDepthMaxLE.text())
                if selected_tracks[0].items[0].getAxis("left").logMode:
                    depth_range_min = np.log10(max(depth_range_min, MINIMUM_FLOAT))
                    depth_range_max = np.log10(max(depth_range_max, MINIMUM_FLOAT * 2))
            else:
                AlertWindow("El rango custom ingresado es invalido, deben ser numeros dentro del rango de profundidad del pozo")
                return None, None, None

        depth_height = selected_tracks[0].items[0].getAxis("left").boundingRect().height()

        depth_range_size = depth_range_max - depth_range_min

        depth_unit = self.get_depth_unit()

        adjusted_depth_height = 0

        if print_scale:
            if depth_unit == METERS_LBL:
                adjusted_depth_height = px_to_m(depth_height, self.dpi_cbo.currentData())

            elif depth_unit == FEETS_LBL:
                adjusted_depth_height = px_to_ft(depth_height, self.dpi_cbo.currentData())

            scale = get_scale_format(adjusted_depth_height / depth_range_size)
            original_scale = scale
        else:
            scale = None

        #Get range original
        #setYRange valores custom, padding =0
        #obtener padding sugerido
        #setYRange original
        #continuar

        #Rango total a exportar = rango custo + padding obtenido * 2
        #factor_cambio = escala destino / escala origen
        #incremento = Rango total a exportar / factor_cambio

        pngs = []

        track_width_w_header = None

        if print_scale \
                and (not self.exportScaleDefaultCb.isChecked()) \
                and (float(original_scale[2:]) > float(self.exportScaleCbo.currentText()[2:])):
            scaling_factor = float(self.exportScaleCbo.currentText()[2:]) / float(original_scale[2:])
            increase = depth_range_size * scaling_factor
            i = 0

            previous_limits = free_tracks_viewbox(selected_tracks)

            label_title = None

            if len(selected_tracks) > 1:
                label_title = selected_tracks[0].get_lateral_label_content()

            # This dummy while fixes (somehow) an error when exporting images with fixed width that have
            # many tracks.
            while depth_range_min + i*increase < depth_range_max:
                png_name, adh, scale, width = self.export_tracks_to_pngs(f"{file_name[0:-4]}_{str(i)}_horizontal.png",
                                                            selected_tracks,
                                                            str(float(depth_range_min) + i*increase),
                                                            str(float(depth_range_min) + (1+i)*increase),
                                                            i==0,
                                                            track_width_w_header,
                                                            depth_range_max,
                                                            print_scale)
                if png_name is None:
                    return None, None, None

                track_width_w_header = width if i == 0 else track_width_w_header

                i = i + 1

            for j in range(len(selected_tracks)):
                selected_tracks[j].set_lateral_label_content(label_title)

            i = 0

            while depth_range_min + i*increase < depth_range_max:
                png_name, adh, scale, width = self.export_tracks_to_pngs(f"{file_name[0:-4]}_{str(i)}_horizontal.png",
                                                            selected_tracks,
                                                            str(float(depth_range_min) + i*increase),
                                                            str(float(depth_range_min) + (1+i)*increase),
                                                            i==0,
                                                            track_width_w_header,
                                                            depth_range_max,
                                                            print_scale)
                if png_name is None:
                    return None, None, None

                pngs.append(str(png_name))

                track_width_w_header = width if i == 0 else track_width_w_header

                i = i + 1

            path_png_only_tracks = self.combine_vertical_pngs(pngs,
                                                              file_name[0:-4] + "_horizontal.png",
                                                              False,
                                                              vertical_padding,
                                                              self.dpi_cbo.currentData())

            set_tracks_y_range(selected_tracks, original_depth_range_min, original_depth_range_max)

            set_tracks_viewbox(selected_tracks, previous_limits)

            for j in range(len(selected_tracks)):
                selected_tracks[j].set_lateral_label_content(label_title)

        else:
            path_png_only_tracks, adjusted_depth_height, scale, _ = self.export_tracks_to_pngs(file_name,
                                                                                        selected_tracks,
                                                                                        depth_range_min,
                                                                                        depth_range_max,
                                                                                        header=True,
                                                                                        print_scale=print_scale)

        image = Image.open(path_png_only_tracks)
        image_width = image.width
        image_height = image.height
        image.close()

        if print_scale and (not self.exportScaleDefaultCb.isChecked()) and (float(original_scale[2:]) <= float(self.exportScaleCbo.currentText()[2:])):
            scaling_factor = float(original_scale[2:]) / float(self.exportScaleCbo.currentText()[2:])
            self.scale_image(path_png_only_tracks, path_png_only_tracks, scaling_factor)

            adjusted_depth_height = adjusted_depth_height * scaling_factor
            #scale = get_scale_format(adjusted_depth_height / depth_range_size)
            scale = self.exportScaleCbo.currentText()

            image = Image.open(path_png_only_tracks)
            image_width = image.width
            image_height = image.height
            image.close()

        header_text_3 = ""
        if selected_tracks[0].items[0].getAxis("left").logMode:
            depth_range_max = 10 ** depth_range_max
            depth_range_min = 10 ** depth_range_min
            header_text_3 = "Eje vertical en escala logarítmica"

        header_text_1 = str(f"Pozo: {app_config.current_well}")
        header_text_2 = "Rango eje vertical: " + \
                            str(round(depth_range_min, number_of_decimals)) + " a " \
                            + str(round(depth_range_max, number_of_decimals))
        if print_scale:
            header_text_2 = "Profundidad (" +  str(self.get_depth_unit()).upper() +"): " + \
                            str(round(depth_range_min, number_of_decimals)) + " a " \
                            + str(round(depth_range_max, number_of_decimals))
            header_text_3 = f"Escala: {scale}" if print_scale else f"Escala: --- (No Aplica a Crossplots/Histogramas)"


        header_png = self.export_header_png(file_name[0:-4] + "_header",
                                            [header_text_1, header_text_2, header_text_3],
                                            image_width)

        if print_scale and self.exportPDFRb.isChecked() and self.exportPDFPaperSizeCbo.currentData() != ORIGINAL_SIZE:
            header_image = Image.open(header_png)
            image_height = header_image.height + vertical_padding + image_height
            image_width = max(header_image.width, image_width)
            header_image.close()

            pdf_layout = get_layout_fun(pagesize=(pdf_paper_size[self.exportPDFPaperSizeCbo.currentData()][0],
                                                  px_to_pt(image_height, self.dpi_cbo.currentData())),
                                        fit=None)

            _, _, pdf_img_width, pdf_img_height = pdf_layout(image_width,
                                                             image_height,
                                                             (self.dpi_cbo.currentData(), self.dpi_cbo.currentData()))

            scaled_axis_height = depth_height * pt_to_px(pdf_img_height, self.dpi_cbo.currentData()) / image_height

            depth_unit = self.get_depth_unit()

            if depth_unit == METERS_LBL:
                scaled_axis_height = px_to_m(scaled_axis_height, self.dpi_cbo.currentData())

            elif depth_unit == FEETS_LBL:
                scaled_axis_height = px_to_ft(scaled_axis_height, self.dpi_cbo.currentData())

            if not self.exportScaleDefaultCb.isChecked():
                scale = self.exportScaleCbo.currentText()

            else:
                scale = get_scale_format(scaled_axis_height / depth_range_size)

            header_text_3 = f"Escala: {scale}."

            header_png = self.export_header_png(file_name[0:-4] + "_header",
                                            [header_text_1, header_text_2, header_text_3],
                                            image_width)

        self.combine_vertical_pngs([header_png, path_png_only_tracks],
                                 file_name,
                                 show_popup,
                                 vertical_padding,
                                 self.dpi_cbo.currentData())

        self.exportWindow.close()

        return file_name, depth_height, depth_range_size

    def combine_pngs(self,
                     pngs,
                     file_name,
                     show_popup,
                     header=False,
                     minimum_width=None):
        if len(pngs) == 0:
            AlertWindow("No hay tracks seleccionados para exportar")
            return None

        images = [Image.open(png) for png in pngs]

        widths = []
        heights = []

        for i in images:
            widths.append(i.size[0])
            heights.append(i.size[1])
        #widths, heights = zip(*(i.size for i in images))

        if minimum_width:
            for i in range(len(widths)):
                widths[i] = max(widths[i], minimum_width)

        x_padding = X_PADDING_IMAGES

        x_offset = 0 if header else LAYOUT_LEFT_PADDING

        new_png = Image.new('RGB',
                            (sum(widths) + x_padding * (len(pngs) - 1) + x_offset,
                             max(heights) - LAYOUT_BOTTOM_PADDING if header else max(heights) - 1),
                            (255, 255, 255))

        for i in range(len(images)):
            if header:
                im = images[i].crop((0, 0, images[i].width, images[i].height - LAYOUT_BOTTOM_PADDING))
            else:
                im = images[i].crop((0, 1, images[i].width, images[i].height))
            delta_x = x_offset

            if i > 1:
                delta_x += x_padding

            new_png.paste(im,
                          (delta_x,
                           0))

            images[i].close()

            x_offset = delta_x + widths[i]

        new_png.save(file_name)

        new_png.close()

        for png in pngs:
            remove(png)

        if show_popup:
            InfoWindow('Imagen exportada')

        return file_name

    def combine_vertical_pngs(self,
                              pngs,
                              file_name,
                              show_popup,
                              vertical_padding=Y_PADDING_IMAGES,
                              dpi_value=NORMAL_DPI):
        if len(pngs) == 0:
            AlertWindow("No hay imagenes para combinar verticalmente")
            return None

        images = [Image.open(png) for png in pngs]

        widths, heights = zip(*(i.size for i in images))

        new_png = Image.new('RGB',
                            (max(widths),
                             sum(heights) + vertical_padding * (len(pngs) - 1)),
                            (255, 255, 255))

        y_offset = 0

        for i in range(len(images)):
            delta_y = y_offset

            if i > 1:
                delta_y += vertical_padding

            delta_x = 0

            new_png.paste(images[i],
                          (delta_x,
                           delta_y))

            y_offset = delta_y + images[i].size[1]

            images[i].close()

        new_png.save(file_name, dpi=(dpi_value, dpi_value))

        new_png.close()

        for png in pngs:
            remove(png)

        if show_popup:
            InfoWindow('Imagen exportada')

        return file_name

    def scale_image(self, image_path, destination_path, scale_factor):
        image = Image.open(image_path)
        width = int(image.width*scale_factor)
        height = int(image.height*scale_factor)
        resized = image.resize((width, height))
        image.close()
        resized.save(destination_path)
        resized.close()
        return destination_path

    def export_to_pdf(self, file_name, show_popup=True):
        png_path, axis_height, depth_range_size = self.export_to_pngs(file_name,
                                                                      False)

        if png_path is None:
            return

        image = Image.open(png_path)

        if self.exportPDFPaperSizeCbo.currentData() != ORIGINAL_SIZE:
            pdf_layout = get_layout_fun(pagesize=(pdf_paper_size[self.exportPDFPaperSizeCbo.currentData()][0],
                                                  px_to_pt(image.height, self.dpi_cbo.currentData())),
                                        fit=None)

            pdf_bytes = convert(image.filename, layout_fun=pdf_layout)

        else:
            pdf_bytes = convert(image.filename)

        pdf_path = png_path.replace(".png",
                                    ".pdf")

        file = open(pdf_path, "wb")

        file.write(pdf_bytes)

        image.close()

        file.close()

        remove(png_path)

        if show_popup:
            InfoWindow('PDF exportado')

        self.exportWindow.close()

    def set_ephimeral_track(self,
                            track_name,
                            tab_name):
        self.ephimeral_tracks.add(EphimeralTrackRegister(track_name,tab_name))

    def set_track_to_delete(self,
                            to_delete):
        for track in to_delete:
            self.ephimeral_to_delete.add(track)

            self.ephimeral_tracks.remove(track)

    def remove_ephimeral_tracks(self,
                                tab_name):
        ephimeral_track_names_to_delete = list(
            map(lambda track: track.get_track_name(), self.ephimeral_to_delete)
        )

        curve_tracks_to_remove = list(
            filter(lambda x: x.get_name() in ephimeral_track_names_to_delete,
                   self.curve_tracks)
        )

        for track in curve_tracks_to_remove:
            self.remove_curve_track(track.get_name())

    def set_tracks_to_delete(self,
                             tracks_to_update):
        ephimeral_track_names = list(
            map(lambda track: track.get_track_name(), self.ephimeral_tracks)
        )

        # Preconditions:
        # - every curve in a ephimeral track is ephimeral.
        to_delete_names = list(
            map(lambda x: x.get_name(),
                filter(lambda x: x.get_name() in ephimeral_track_names,
                       tracks_to_update)
                )
        )

        tracks_to_delete = list(
            filter(lambda x: x.get_track_name() in to_delete_names, self.ephimeral_tracks)
        )

        self.set_track_to_delete(tracks_to_delete)

    def draw_tracks_with_new_unit(self, depth_curve, old_unit, new_unit):
        for track in self.curve_tracks:
            track.adjust_depth_in_configs(depth_curve, old_unit, new_unit)

        self.draw_tracks(EVERY_TAB)

    def get_serialized_curve_tracks(self):
        serializations = []

        for curve_track in self.curve_tracks:
            serializations.append(curve_track.get_serialized_state())

        return serializations

    def set_view(self, state):
        for track_data in state:
            curve_track = self.create_curve_track(track_data["tab_name"],
                                                  track_data["track_name"],
                                                  len(self.curve_tracks),
                                                  track_data.get("title", "") is not None)

            if curve_track is None:
                continue

            curve_track.set_state(track_data)

    def get_tabs_in_use(self):
        return get_uniques(
            list(
                flat_map(lambda track: track.get_tabs_in_use(),
                         self.curve_tracks)
            )
        )

    def get_track(self, tab_name, track_name):
        existing_tracks = list(
            filter(lambda track: track.tab_name == tab_name,
                   self.curve_tracks)
        )

        result = list(
            filter(lambda track: track.track_name == track_name,
                   existing_tracks)
        )

        if len(result) == 0:
            return None

        return result[0]

    def clear_track_curves(self, tab_name, track_name):
        track = self.get_track(tab_name, track_name)

        if track is None:
            return

        track.clear_curves_config()
