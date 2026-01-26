import sys
import os
import numpy as np
from shapely.geometry import Polygon, LineString
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt6.QtGui import QIcon
from interface import Ui_MainWindow
import pyqtgraph as pg

if getattr(sys, "frozen", False):  # If bundled as .exe
    base_path = sys._MEIPASS
else:  # Running as script
    base_path = os.path.dirname(os.path.abspath(__file__))

def read_points_from_file(filename):
    points = []
    with open(filename, 'r') as f:
        for line in f:
            if line.strip():
                x, y = map(float, line.strip().split())
                points.append((x, y))
    return points


def write_points_to_file(filename, points):
    with open(filename, 'w') as f:
        for x, y in points:
            f.write(f"{x:.4f} {y:.4f}\n")


def interpolate_linestring(line, r):
    length = line.length
    num_points = int(np.floor(length / r))
    distances = np.linspace(0, length, num_points)
    return [line.interpolate(d).coords[0] for d in distances]


def interpolate_path_with_offset(points, r, offset=0):
    poly = Polygon(points)
    poly_offset = poly.buffer(offset)
    offset_line = LineString(poly_offset.exterior.coords)
    offset_points = interpolate_linestring(offset_line, r)
    return offset_points

def load_qss(file_path):
    """Load and return the QSS stylesheet."""
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return file.read()
    return ""

class InterpolationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        icon_path = os.path.join(base_path, 'Assets/icon1.ico')
        self.setWindowIcon(QIcon(icon_path))

        # Setup Plot
        self.ui.plot_widget.getPlotItem().setAspectLocked(True)

        # Connect Signals
        self.ui.browse_button.clicked.connect(self.browse_file)
        self.ui.generate_button.clicked.connect(self.generate_points)
        self.ui.quit_button.clicked.connect(self.close)

        # Enable drag & drop
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if os.path.isfile(file_path):
                self.ui.input_file_edit.setText(file_path)
                self.ui.statusbar.showMessage(f"Loaded input file: {file_path}")

    def browse_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Input File", "", "Text Files (*.txt *.tpl *.dat);;All Files (*)")
        if file_name:
            self.ui.input_file_edit.setText(file_name)
            self.ui.statusbar.showMessage(f"Loaded input file: {file_name}")

    def generate_points(self):
        input_file = self.ui.input_file_edit.toPlainText().strip()
        if not os.path.isfile(input_file):
            self.ui.statusbar.showMessage("Invalid input file!")
            return

        try:
            r = float(self.ui.r_edit.text())
            offset = float(self.ui.offset_edit.text())
        except ValueError:
            self.ui.statusbar.showMessage("Invalid numeric values for r or offset")
            return

        suffix = self.ui.output_suffix_edit.text().strip()
        base, ext = os.path.splitext(input_file)
        output_file = base + "_interpolated" + str(suffix) + ext

        try:
            original_points = read_points_from_file(input_file)
            offset_points = interpolate_path_with_offset(original_points, r, offset)
            write_points_to_file(output_file, offset_points)

            # Plot
            self.ui.plot_widget.clear()
            x, y = zip(*original_points)
            ox, oy = zip(*offset_points)

            # Original path -> line + points
            self.ui.plot_widget.plot(x, y, pen='r', symbol='o', symbolBrush='r', symbolSize=6, name="Original Path")

            # Interpolated points -> only points
            self.ui.plot_widget.plot(ox, oy, pen=None, symbol='o', symbolBrush='b', symbolSize=5, name="Interpolated Points")

            self.ui.statusbar.showMessage(f"Generated {len(offset_points)} points. Saved to {output_file}")

        except Exception as e:
            self.ui.statusbar.showMessage(f"Error: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    qss_path = os.path.join(base_path, "Assets/Adaptic.qss")
    app.setStyleSheet(load_qss(qss_path))
    
    window = InterpolationApp()
    window.show()
    sys.exit(app.exec())
