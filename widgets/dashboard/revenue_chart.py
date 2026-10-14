from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout
from PySide6.QtGui import QColor, QPainter, QPen, QFont
from PySide6.QtCore import Qt, QMargins

class RevenueChart(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("RevenueChart")
        self.build_ui()

    def build_ui(self):
        self.setMinimumHeight(340)
        self.setStyleSheet("""
        QFrame { background:#1B2333; border-radius:18px; }
        QLabel { color:white; }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title = QLabel("Monthly Revenue")
        title.setFont(QFont("Segoe UI", 15, QFont.Bold))
        layout.addWidget(title)

        self.total = QLabel("₹ 0")
        self.total.setStyleSheet("font-size:26px; font-weight:bold; color:#22C55E;")
        layout.addWidget(self.total)

        self.series = QLineSeries()
        pen = QPen(QColor("#6D8DFF"))
        pen.setWidth(4)
        self.series.setPen(pen)

        self.chart = QChart()
        self.chart.addSeries(self.series)
        self.chart.legend().hide()
        self.chart.setBackgroundVisible(False)
        self.chart.setPlotAreaBackgroundVisible(False)
        self.chart.setMargins(QMargins(0, 0, 0, 0))

        self.axisX = QValueAxis()
        self.axisX.setRange(0, 11)
        self.axisX.setTickCount(12)
        self.axisX.setLabelsColor(QColor("white"))
        self.axisX.setGridLineVisible(False)

        self.axisY = QValueAxis()
        self.axisY.setRange(0, 150)
        self.axisY.setTickCount(7)
        self.axisY.setLabelsColor(QColor("white"))
        self.axisY.setGridLineColor(QColor("#374151"))

        self.chart.addAxis(self.axisX, Qt.AlignBottom)
        self.chart.addAxis(self.axisY, Qt.AlignLeft)
        self.series.attachAxis(self.axisX)
        self.series.attachAxis(self.axisY)

        view = QChartView(self.chart)
        view.setRenderHint(QPainter.Antialiasing)
        view.setStyleSheet("background:transparent; border:none;")
        layout.addWidget(view)

    def update_data(self, values: list, total_text: str = None):
        self.series.clear()
        for i, val in enumerate(values):
            self.series.append(i, val)

        if values:
            max_val = max(values)
            self.axisY.setRange(0, max_val * 1.2)
            self.axisX.setRange(0, max(11, len(values) - 1))

        if total_text:
            self.total.setText(total_text)