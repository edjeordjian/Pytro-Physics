"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""


def add_dictionary_to_combo(cbo, dictionary):
    for key in dictionary.keys():
        cbo.addItem(key, dictionary[key])


def get_combo_text(cbo_element):
    return cbo_element.placeholderText() if \
        len(cbo_element.text()) == 0 else \
        cbo_element.text()


def update_curve_list(cbo,
                      well,
                      use_data=False):
    previous_index = cbo.currentIndex()

    cbo.clear()

    well_model = well.wellModel

    curve_names = well_model.get_curve_names()

    for curve_name in curve_names:
        if use_data:
            # WARNING: memory consuming!
            cbo.addItem(curve_name,
                        well_model.get_df_curve(curve_name))

        else:
            cbo.addItem(curve_name,
                        curve_name)

    if previous_index > 0:
        cbo.setCurrentIndex(previous_index)

    else:
        cbo.setCurrentIndex(0)


def update_curve_list_multi_cbo(multi_cbo,
                                well,
                                use_data=False):
    previous_indexes = multi_cbo.currentIndexes()

    multi_cbo.clear()

    well_model = well.wellModel

    curve_names = well_model.get_curve_names()

    for curve_name in curve_names:
        if use_data:
            # WARNING: memory consuming!
            multi_cbo.addItem(curve_name,
                              well_model.get_df_curve(curve_name))

        else:
            multi_cbo.addItem(curve_name,
                              curve_name)

    if len(previous_indexes) > 0:
        multi_cbo.setIndexes(previous_indexes)


def update_cbo(cbo,
               data,
               id_fn):
    previous_index = cbo.currentIndex()

    cbo.clear()

    if len(data) == 0:
        return

    for element in data:
        cbo.addItem(id_fn(element),
                    element)

    cbo.setCurrentIndex(previous_index)


def update_cbos(cbos,
                data,
                id_fn):
    for cbo in cbos:
        update_cbo(cbo,
                   data,
                   id_fn)


def add_none_option(cbos, keep_index=False, keep_last=True):
    for cbo in cbos:
        if keep_index:
            index = cbo.currentIndex()

            # None option was selected
            if index < 0:
                index = cbo.count()

            elif index == cbo.count() - 1:
                if keep_last:
                    index = cbo.count()

                else:
                    index = cbo.count() - 1

        else:
            index = cbo.count()

        cbo.insertItem(cbo.count(),
                       "N/A")

        cbo.setCurrentIndex(index)


def if_checked_enable_combo(cbo,
                            checkbox):
    if checkbox.isChecked():
        cbo.setEnabled(True)

    else:
        cbo.setEnabled(False)


def disable_elements_with_component(component,
                                    elements,
                                    inverse=False):
    condition = component.isChecked() if not inverse else not component.isChecked()

    for element in elements:
        element.setEnabled(condition)
