"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later.
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from pyqtgraph import PlotItem, AxisItem

from ui.visual_components.AxisItemWithoutLine import AxisItemWithoutLine


class PlotItemWithoutLine(PlotItem):
    def setAxisItems(self, axisItems=None):
        """
        Place axis items as given by `axisItems`. Initializes non-existing axis items.

        ==============  ==========================================================================================
        **Arguments:**
        *axisItems*     Optional dictionary instructing the PlotItem to use pre-constructed items
                        for its axes. The dict keys must be axis names ('left', 'bottom', 'right', 'top')
                        and the values must be instances of AxisItem (or at least compatible with AxisItem).
        ==============  ==========================================================================================
        """

        if axisItems is None:
            axisItems = {}

        # Array containing visible axis items
        # Also containing potentially hidden axes, but they are not touched so it does not matter
        visibleAxes = ['left', 'bottom']
        visibleAxes.extend(axisItems.keys())  # Note that it does not matter that this adds
        # some values to visibleAxes a second time

        for k, pos in (('top', (1, 1)), ('bottom', (3, 1)), ('left', (2, 0)), ('right', (2, 2))):
            if k in self.axes:
                if k not in axisItems:
                    continue  # Nothing to do here

                # Remove old axis
                oldAxis = self.axes[k]['item']
                self.layout.removeItem(oldAxis)
                oldAxis.scene().removeItem(oldAxis)
                oldAxis.unlinkFromView()

            # Create new axis
            if k in axisItems:
                axis = axisItems[k]
                if axis.scene() is not None:
                    if k not in self.axes or axis != self.axes[k]["item"]:
                        raise RuntimeError(
                            "Can't add an axis to multiple plots. Shared axes"
                            " can be achieved with multiple AxisItem instances"
                            " and set[X/Y]Link.")
            else:
                if k == "top":
                    axis = AxisItemWithoutLine(orientation=k, parent=self)

                else:
                    axis = AxisItem(orientation=k, parent=self)

            # Set up new axis
            axis.linkToView(self.vb)
            self.axes[k] = {'item': axis, 'pos': pos}
            self.layout.addItem(axis, *pos)
            # place axis above images at z=0, items that want to draw over the axes should be placed at z>=1:
            axis.setZValue(0.5)
            axis.setFlag(axis.GraphicsItemFlag.ItemNegativeZStacksBehindParent)
            axisVisible = k in visibleAxes
            self.showAxis(k, axisVisible)
