from PySide6.QtCharts import QChart, QChartView, QPieSeries
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QColor, QPainter, QFont
from PySide6.QtCore import Qt, QMargins
import qtawesome as qta

class OrderStatusChart(QFrame):
    def __init__(self):
        super().__init__()
        self.legend_widgets = []
        self.build_ui()

    def build_ui(self):
        self.setMinimumWidth(360)
        self.setMinimumHeight(380)
        self.setObjectName("Card")

        self.root = QVBoxLayout(self)
        self.root.setContentsMargins(20, 20, 20, 20)
        self.root.setSpacing(10)

        title = QLabel("Order Status")
        title.setObjectName("CardTitle")
        self.root.addWidget(title)

        self.series = QPieSeries()
        self.series.setHoleSize(0.55)

        self.chart = QChart()
        self.chart.addSeries(self.series)
        self.chart.legend().hide()
        self.chart.setBackgroundVisible(False)
        self.chart.setMargins(QMargins(0, 0, 0, 0))
        self.chart.setAnimationOptions(QChart.SeriesAnimations)

        view = QChartView(self.chart)
        view.setRenderHint(QPainter.Antialiasing)
        view.setMinimumHeight(220)
        self.root.addWidget(view)

        self.legend_layout = QVBoxLayout()
        self.legend_layout.setSpacing(5)
        self.root.addLayout(self.legend_layout)

    def update_data(self, status_list):
        self.series.clear()

        for w in self.legend_widgets:
            self.legend_layout.removeWidget(w)
            w.deleteLater()
        self.legend_widgets.clear()

        for label, val, color_hex in status_list:
            slice_item = self.series.append(label, val)
            slice_item.setColor(QColor(color_hex))
            slice_item.setLabelVisible(False)

            legend_item = self._create_legend_item(color_hex, label, val)
            self.legend_layout.addWidget(legend_item)
            self.legend_widgets.append(legend_item)

    def _create_legend_item(self, color, text, value):
        row = QHBoxLayout()
        row.setContentsMargins(0, 0, 0, 0)

        # Colour comes from the data, so draw the dot as an icon
        dot = QLabel()
        dot.setPixmap(qta.icon("fa5s.circle", color=color).pixmap(12, 12))

        lbl = QLabel(text)
        lbl.setObjectName("FieldLabel")

        number = QLabel(str(value))
        number.setObjectName("ValueText")

        row.addWidget(dot)
        row.addWidget(lbl)
        row.addStretch()
        row.addWidget(number)

        wrapper = QFrame()
        wrapper.setLayout(row)
        return wrapper