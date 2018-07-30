import sys
from itertools import cycle
from PyQt5.QtGui import QIcon, QPixmap, QColor, QBrush, QPen
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton,
         QHBoxLayout, QVBoxLayout, QGraphicsScene, QGraphicsView)

qt_app = QApplication(sys.argv)

class GitviewGui(QGraphicsScene):
    COLORS = cycle([
            QColor(255,   0,   0), # red
            QColor(255,   0, 255), # red
            QColor(  0,   0, 255), # red
            QColor(  0, 255, 255), # red
            QColor(  0, 255,   0), # red
            QColor(255, 255,   0), # red
            ])
    #COLORS = cycle([QColor(colorname) for colorname in QColor.colorNames()])
    _commit_size = (30, 30)
    _hspace = 15
    _vspace = 15
    _branch_position = [0, 0]
    _pen = QPen()

    def __init__(self):
        QWidget.__init__(self)
        #self.setWindowTitle("Gitview")
        #self.setMinimumWidth(400)

        self.view = QGraphicsView(self)

    def draw_branch(self, branch):
        self._branch_position[0] = 0
        color = next(self.COLORS)
        self._brush = QBrush(color)
        self._parent_location = None
        width = 3
        for commit in branch:
            self.draw_commit(commit)
            self._pen.setWidth(width)
            #width += 1
        self._branch_position[1] += self._vspace + self._commit_size[1]

    def draw_commit(self, commit):
        loc = self._branch_position
        self.addEllipse(*loc,
                        *self._commit_size,
                        brush=self._brush)
        if self._parent_location is not None:
            line_loc = [*self._parent_location, *loc]
            line_loc[0] += self._commit_size[0]
            line_loc[1] += self._commit_size[1] / 2
            line_loc[3] += self._commit_size[1] / 2
            self.addLine(*line_loc, self._pen)
            if False:
                print("Parent: {0}, {1}; loc: {2}, {3}".format(
                    *self._parent_location, *loc))
                print("  Line: {0}".format(line_loc))
        self._parent_location = list(loc)
        self._branch_position[0] += self._commit_size[0] + self._hspace

    def run(self):
        self.view.show()
        qt_app.exec()

if __name__ == "__main__":
    gui = GitviewGui()
    gui.draw_branch([x for x in range(5)])
    gui.draw_branch([x for x in range(2)])
    gui.draw_branch([x for x in range(3)])
    gui.draw_branch([x for x in range(8)])
    gui.run()
