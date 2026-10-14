from PySide6.QtCharts import QChart, QChartView, QPieSeries
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QColor, QPainter, QFont
from PySide6.QtCore import Qt, QMargins

class OrderStatusChart(QFrame):
    def __init__(self):
        super().__init__()
        self.legend_widgets = []
        self.build_ui()

    def build_ui(self):
        self.setMinimumWidth(360)
        self.setMinimumHeight(380)
        self.setStyleSheet("QFrame { background:#1B2333; border-radius:18px; } QLabel { color:white; }")
        self.setObjectName("OrderStatusChart")

        self.root = QVBoxLayout(self)
        self.root.setContentsMargins(20, 20, 20, 20)
        self.root.setSpacing(10)

        title = QLabel("Order Status")
        title.setFont(QFont("Segoe UI", 15, QFont.Bold))
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
        view.setStyleSheet("QChartView { background:transparent; border:none; }")
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

        dot = QLabel("●")
        dot.setStyleSheet(f"color:{color}; font-size:16px;")

        lbl = QLabel(text)
        lbl.setStyleSheet("color:#D1D5DB; font-size:13px;")

        number = QLabel(str(value))
        number.setStyleSheet("color:white; font-size:13px; font-weight:bold;")

        row.addWidget(dot)
        row.addWidget(lbl)
        row.addStretch()
        row.addWidget(number)

        wrapper = QFrame()
        wrapper.setLayout(row)
        wrapper.setStyleSheet("QFrame { background:transparent; border:none; }")
        return wrapper