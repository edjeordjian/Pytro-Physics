"""
Copyright 2023, Pytrophysics developers.

Licensed under GNU GPL 3.0 or later. 
See COPYING.txt for more information (you should have received a copy of the GNU General Public License 3 
along with this program. If not, see <https://www.gnu.org/licenses/gpl-3.0.txt>).
"""

from PyQt6.QtWidgets import QFrame, QGridLayout, QLabel


# You can't hide a layout, but you can hide a frame.
class LayoutWithFrame:
    def __init__(self):
        self.layout = QGridLayout()

        self.frame = QFrame()

        self.frame.setLayout(self.layout)

        self.lines = 0

    def getFrame(self):
        return self.frame

    def addWidget(self,
                  widget,
                  column=0,
                  next_line=True,
                  alignment=None):
        if alignment is not None:
            self.layout \
                .addWidget(widget,
                           self.lines,
                           column,
                           alignment=alignment)

        else:
            self.layout \
                .addWidget(widget,
                           self.lines,
                           column)

        if next_line:
            self.lines += 1

            self.addWidget(QLabel(""),
                           next_line=False)

    def addLayout(self,
                  layout,
                  column=0,
                  next_line=True,
                  alignment=None):
        if alignment is not None:
            self.layout \
                .addLayout(layout,
                           self.lines,
                           column,
                           alignment=alignment)

        else:
            self.layout \
                .addLayout(layout,
                           self.lines,
                           column)

        if next_line:
            self.add_blank_line()

    def add_blank_line(self):
        self.lines += 1

        self.addWidget(QLabel(""),
                       next_line=False)

    def hide(self):
        self.frame.hide()

    def show(self):
        self.frame.show()
