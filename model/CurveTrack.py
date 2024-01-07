"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

import pyqtgraph as pg
from services.image_service import pt_to_px
from services.tools.json_service import get_list_of_items, remove_from_dictionary, get_list_of_values

from services.tools.list_service import last_element, replace_in_list, first_element, remove_list_from_list, \
    get_uniques, get_sublist_and_complement

from ui.visual_components.ColoredCurve import ColoredCurve
from ui.visual_components.ColoredRectangle import ColoredRectangle

from ui.visual_components.LithologiesItemSample import LithologiesItemSample

from ui.visual_components.track_handler import create_track, adjust_depth_in_config

import copy

from constants.general_constants import LAYOUT_LEFT_PADDING, LAYOUT_TOP_PADDING, LAYOUT_RIGHT_PADDING, \
    LAYOUT_BOTTOM_PADDING, TRACK_TITLE_LENGTH


class CurveTrack:
    real_track_axis = {}

    @staticmethod
    def get_max_axis():
        return max(
            list(CurveTrack.real_track_axis
                 .values()
                 ))

    def __init__(self, tab_name, track_name, layout,
                 title=True, stand_alone=False):
        self.configs = {}

        self.rectangle_configs = {}

        self.axis_configs = []

        self.fill_configs = []

        self.update = False

        self.scatter = False

        self.stand_alone = stand_alone

        self.tab_name = tab_name

        self.title = None

        if title:
            self.title = pg.LabelItem(track_name,
                                      size=f'{TRACK_TITLE_LENGTH}pt',
                                      color='#000000')

            self.original_title_text = track_name

        self.track_name = track_name

        self.axis_number = 0

        CurveTrack.real_track_axis[self.track_name] = self.axis_number

        self.legend = None

        self.init_restartable_attributes()

        self.mainLayout = layout

    def init_restartable_attributes(self):
        self.items = []

        self.curves = {}

        self.rectangles = {}

        self.scatter_lines = {}

        self.fill_items = {}

        self.axis = []

        self.blank_labels = []

    # Update should not be assigned here
    def initTrack(self,
                  track_position,
                  yRange=[]):
        self.layout = pg.GraphicsLayout()

        self.layout.setContentsMargins(LAYOUT_LEFT_PADDING,
                                       LAYOUT_TOP_PADDING, 
                                       LAYOUT_RIGHT_PADDING, 
                                       LAYOUT_BOTTOM_PADDING)

        if self.title is not None:
            self.layout \
                .addItem(self.title,
                         row=0,
                         col=1,
                         rowspan=1,
                         colspan=2)

        self.init_restartable_attributes()

        try:
            previous_track = self.track

        except AttributeError:
            previous_track = None

        # self.track tiene el GraphicsView, es decir el widget que represeta graficamente el track
        self.track = create_track(self.mainLayout,
                                  track_position,
                                  previous_track)

        self.track.setCentralWidget(self.layout)

        self.setYRange(yRange)

    def first_item(self):
        return first_element(self.items)

    def last_item(self):
        return last_element(self.items)

    def add_item(self,
                 item):
        self.items. \
            append(item)

    def add_cummulative_item(self, curve_name, curve):
        last_normal = None

        for i in range(
                        len(self.axis)
                      ):
            if not self.axis[i].is_cummulative():
                last_normal = self.axis[i]

            elif curve_name == self.axis[i].get_name():
                # No axis above the cummulative one
                if last_normal is None:
                    return

                x_limits = last_normal.get_limits()

                last_normal.set_x_range_viewbox(x_limits[0], x_limits[1])

                last_normal.add_item(curve)

    def can_be_cummulative(self, curve_name):
        last_normal = None

        for i in range(
                        len(self.axis_configs)
                      ):
            if curve_name == self.axis_configs[i]["curve_name"]:
                # No axis above the cummulative one
                if last_normal is None:
                    return False

                return True

            elif not self.axis_configs[i].get("cummulative", False):
                last_normal = self.axis_configs[i]

        return last_normal is not None

    def add_config(self,
                   config):
        self.configs[config['curve_name']] = config

        self.set_to_update()

    def add_rectangle_config(self,
                             config):
        self.rectangle_configs[config['curve_name']] = config

        self.set_to_update()

    def get_configs_list(self):
        return get_list_of_values(self.configs)

    def get_rectangle_config_list(self):
        return get_list_of_values(self.rectangle_configs)

    def delete_curve_if_existing(self, tab_name, curve_name):
        existing_curves = len(
            list(
                filter(lambda c: tab_name == c["tab_name"] and curve_name == c["curve_name"],
                       self.get_configs_list())))

        if existing_curves != 0:
            self.delete_curve_config(curve_name)

    def get_configs_with_labels(self):
        return list(
            map(lambda config: config['curve_name'],
                filter(lambda config: config.get('legend',
                                                 False),
                       self.get_configs_list())
                )
        )

    def add_legend(self,
                   config):
        self.legend = config

        self.set_to_update()

    def add_legend_item(self):
        self.legend_item = self.first_item() \
            .addLegend(offset=(self.legend['x_offset'],
                               self.legend['y_offset']),
                       labelTextSize=self.legend['legend_text_size'],
                       colCount=self.legend['columns'],
                       sampleType=LithologiesItemSample,
                       labelTextColor=self.legend['legend_text_color'])

        self.first_item() \
            .getAxis('top') \
            .setStyle(tickLength=0)

        for (name,
             colored_curve) in self.get_legend_curves():
            self.legend_item.addItem(colored_curve.curve,
                                     name)

    def get_legend_curves(self):
        configs_with_labels = self.get_configs_with_labels()

        return get_list_of_items(self.curves,
                                 configs_with_labels)

    def delete_curve_config(self,
                            curve_name):
        if self.configs \
                .get(curve_name,
                     None) is None:
            return

        self.delete_axis_with_curve_name(curve_name)

        self.configs \
            .pop(curve_name)

        self.delete_fill_with(curve_name)

        self.set_to_update()

    def clear_curves_config(self):
        for config in self.get_configs_list():
            self.delete_curve_config(config.get("curve_name"))

    def delete_fill_with(self,
                         curve_name):
        to_delete = []

        for config in self.fill_configs:
            if config['curve_name_1'] == curve_name or \
                    config['curve_name_2'] == curve_name:
                to_delete.append(config)

        for config in to_delete:
            self.fill_configs \
                .remove(config)

    def fill_already_exists(self,
                            new_config):
        curve_name_1 = new_config['curve_name_1']

        curve_name_2 = new_config['curve_name_2']

        for i in range(len(self.fill_configs)):
            config = self.fill_configs[i]

            if ((config['curve_name_1'] == curve_name_1 and
                 config['curve_name_2'] == curve_name_2) or
                    (config['curve_name_1'] == curve_name_2 and
                     config['curve_name_2'] == curve_name_1)):
                return i

        return -1

    def add_fill_config(self,
                        config):
        config_idx = self.fill_already_exists(config)

        if config_idx >= 0:
            self.fill_configs.pop(config_idx)

        idx_curve_1 = self.get_curve_axis_idx(config['curve_name_1'])

        idx_curve_2 = self.get_curve_axis_idx(config['curve_name_2'])

        # If idx_curve_1 an idx_curve_2 < 0, this is bypassed (ignored), because it
        # represents the case where no axis is being used.

        if idx_curve_1 < idx_curve_2:
            config['curve_name_1'], config['curve_name_2'] = config['curve_name_2'], config['curve_name_1']

        self.fill_configs \
            .append(config)

        return True

    def add_fill_item(self,
                      curve_name,
                      fill_item):
        axis_idx = self.get_curve_axis_idx(curve_name)

        self.axis[axis_idx] \
            .viewbox \
            .addItem(fill_item)

        self.fill_items[curve_name] = fill_item

    def remove_fill_config(self,
                           config):
        idx_to_pop = self.fill_already_exists(config)

        if idx_to_pop < 0:
            return False

        self.fill_configs \
            .pop(idx_to_pop)

    def add_axis_config(self,
                        config):
        self.axis_configs \
            .append(config)

        self.axis_number += 1

        if not config.get("blank", False):
            CurveTrack.real_track_axis[self.track_name] += 1

        self.set_to_update()

    def replace_axis_config(self,
                            new_config):
        old_config = next(filter(
            lambda axis_config: axis_config['curve_name'] == new_config['curve_name'],
            self.axis_configs),
            None)

        replace_in_list(self.axis_configs,
                        old_config,
                        new_config)

    def delete_axis_with_curve_name(self,
                                    curve_name):
        # Axis have the same name as their associated curve
        if not self.configs[curve_name].get("add_axis", False):
            return

        axies_configs_without_curve = list(
            filter(lambda config: config['curve_name'] != curve_name,
                   self.axis_configs))

        if self.axis_configs != axies_configs_without_curve:
            self.axis_configs = axies_configs_without_curve

            self.axis_number -= 1

            CurveTrack.real_track_axis[self.track_name] -= 1

        # Deletes blank axis configs if there is only one curve
        # if len(self.configs) == 1:
        #     self.axis_configs = []

    def remove_blank_axis(self):
        blank_axis = list(filter(lambda config: config["blank"],
                                  self.axis_configs))

        if len(blank_axis) == 0:
            raise Exception("No hay tracks blank")

        self.axis_number -= 1

        self.axis_configs.remove(blank_axis[0])

    def add_axis(self,
                 axis):
        self.axis.append(axis)

    def add_blank_label(self,
                         blank_label):
        self.blank_labels.append(blank_label)

    def get_curve_axis_idx(self,
                           curve_name):
        for i in range(len(self.axis)):
            if self.axis[i].name == curve_name:
                return i

        return -1

    def get_curve_axis(self,
                       curve_name):
        for i in range(len(self.axis)):
            if self.axis[i].name == curve_name:
                return self.axis[i]

        return None

    def get_axis_configs_and_blanks(self):
        return get_sublist_and_complement(self.axis_configs,
                                          lambda config: not config.get("blank", False))

    def update_axis(self):
        track_viewbox = self.first_item()\
            .getViewBox()

        for axis in self.axis:
            axis.set_geometry(track_viewbox.sceneBoundingRect())

        horizontal_spacing = self.layout.layout.horizontalSpacing()

        for blank_label in self.blank_labels:
            blank_label.setFixedWidth(self.first_item().getAxis("left").width() - horizontal_spacing)

    def is_blank_axis_compatible(self):
        return len(self.configs) > 0 and not self.stand_alone

    def first_axis(self):
        first_config = first_element(list(
            filter(lambda config: not config.get('blank', False),
                   self.axis_configs)
            )
        )

        if first_config is None:
            return None

        return self.axis[self.axis_configs.index(first_config)]

    def first_item_with_viewbox(self):
        if self.first_axis() is not None:
            return self.first_axis()

        if self.first_item() is not None:
            return self.first_item()

        return None

    def get_first_viewbox(self):
        if self.first_axis() is not None:
            return self.first_axis().viewbox

        if self.first_item() is not None:
            return self.first_item().getViewBox()

        return None

    def get_number_of_real_axies(self):
        return len(
                list(
                    filter(lambda config: not config.get("blank", False), self.axis_configs)))

    def add_curve_data(self,
                       config):
        curve_name = config["curve_name"]

        self.curves[curve_name] = ColoredCurve(config)

        self.set_to_update()

    def add_rectangle_data(self, config):
        curve_name = config["curve_name"]

        self.rectangles[curve_name] = ColoredRectangle(config)

        self.set_to_update()

    def first_curve(self):
        if len(self.curves) == 0:
            return None

        return list(self.curves
                        .values())[0].curve

    def get_curve(self, name):
        try:
            return self.curves[name].get_curve()

        except KeyError:
            try:
                return self.rectangles[name].get_curve()

            except KeyError:
                return None

    def get_curves_with_names(self):
        return self.curves\
            .items()

    def add_track_viewbox(self,
                          viewbox):
        self.layout \
            .scene() \
            .addItem(viewbox)

        try:
            self.update_axis()

            track_viewbox = self.first_item() \
                .getViewBox()

            track_viewbox.sigResized \
                .connect(self.update_axis)

        # No curves
        except AttributeError:
            return

    def get_tab_name(self):
        return self.tab_name

    def get_title_name(self):
        return self.title.text

    def set_to_update(self):
        self.update = True

    def _set_ephimeral_to_delete(self,
                                 config):
        config["ephimeral"] = False

        config["ephimeral_to_delete"] = True

    def remove_ehpimeral_to_delete(self):
        ephimeral_configs = []

        for key, value in self.configs.items():
            for key2, value2 in self.configs[key].items():
                if key2 == "ephimeral_to_delete" and value2 == True:
                    ephimeral_configs.append(key)

        for key in ephimeral_configs:
            self.delete_curve_config(key)

    def end_update(self):
        self.update = False

        for curve_name, curve_data in self.curves.items():
            if not curve_data.has_axis() or curve_data.get_is_cummulative():
                self.add_cummulative_item(curve_name, curve_data.get_curve())

    def set_ephimeral_to_delete(self):
        ephimeral_configs = []

        for key, value in self.configs.items():
            for key2, value2 in self.configs[key].items():
                if key2 == "ephimeral" and value2 == True:
                    ephimeral_configs.append(self.configs[key])

        list(map(lambda config: self._set_ephimeral_to_delete(config),
                 ephimeral_configs))

        ephimeral_fill_configs = list(filter(lambda config: config.get('ephimeral',
                                                                       False),
                                             self.fill_configs))

        list(map(lambda config: self._set_ephimeral_to_delete(config),
                 ephimeral_fill_configs))

    def set_scatter(self,
                    value):
        self.scatter = value

    def is_scatter(self):
        return self.scatter

    def get_name(self):
        return self.track_name

    def adjust_depth_in_configs(self, depth_curve, old_unit, new_unit):
        for key in self.configs.keys():
            adjust_depth_in_config(self.configs[key], depth_curve, old_unit, new_unit)

        for key in self.rectangle_configs.keys():
            adjust_depth_in_config(self.rectangle_configs[key], depth_curve, old_unit, new_unit)

        for config in self.axis_configs:
            adjust_depth_in_config(config, depth_curve, old_unit, new_unit)

        for config in self.fill_configs:
            adjust_depth_in_config(config, depth_curve, old_unit, new_unit)

    def get_serialized_state(self):
        return {
            "configs": self.configs,

            "axis_configs": self.axis_configs,

            "fill_configs": self.fill_configs,

            "rectangle_configs": self.rectangle_configs,

            "stand_alone": self.stand_alone,

            "axis_number": self.axis_number,

            "update": self.update,

            "scatter": self.scatter,

            "tab_name": self.tab_name,

            "track_name": self.track_name,

            "legend": self.legend,

            "title": self.get_title_name() if self.title is not None else None
        }

    def set_state(self, data):
        for config in data["configs"].keys():
            self.add_config(copy.deepcopy(data["configs"][config]))

        for axis_config in data["axis_configs"]:
            self.add_axis_config(copy.deepcopy(axis_config))

        for fill_config in data["fill_configs"]:
            self.add_fill_config(copy.deepcopy(fill_config))

        for rectangle_config in data["rectangle_configs"].keys():
            self.add_rectangle_config(copy.deepcopy(data["rectangle_configs"][rectangle_config]))

        self.stand_alone = data["stand_alone"]

        self.axis_number = data["axis_number"]

        self.update = data["update"]

        self.scatter = data["scatter"]

        self.legend = data["legend"]

    def get_tabs_in_use(self):
        config_tabs = list(
            map(lambda config: config["tab_name"],
                self.configs.values())
        )

        return get_uniques(config_tabs)

    def get_number_of_configs(self):
        return len(self.configs)

    def get_every_axis(self):
        return self.axis

    def set_lateral_label_content(self, label_content):
        return self.first_item().getAxis("left").setLabel(label_content)

    def get_lateral_label_content(self):
        return self.first_item().getAxis("left").labelText

    # TODO: refactor. Title could be a class with this behavior.
    def minimize_title(self, track_width, dpi):
        letter_size = pt_to_px(TRACK_TITLE_LENGTH, dpi)

        if letter_size * len(self.original_title_text) <= track_width:
            return

        number_of_letters = int(track_width / letter_size)

        self.original_title_text = self.title.text

        self.title.setText(self.title.text[0:number_of_letters + 1])

    def restore_title_text(self):
        self.title.setText(self.original_title_text)

    def setYRange(self, yRange):
        if len(yRange) == 0:
            return
        for config in self.configs.values():
            config["y_min_viewbox"] = min(yRange)
            config["y_max_viewbox"] = max(yRange)
        for config in self.rectangle_configs.values():
            config["y_min_viewbox"] = min(yRange)
            config["y_max_viewbox"] = max(yRange)
        for config in self.axis_configs:
            config["y_min_viewbox"] = min(yRange)
            config["y_max_viewbox"] = max(yRange)
        for config in self.fill_configs:
            config["y_min_viewbox"] = min(yRange)
            config["y_max_viewbox"] = max(yRange)
