from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QGraphicsDropShadowEffect
)

from PySide6.QtGui import QColor, QFont
from PySide6.QtCore import Qt

import qtawesome as qta
from utils.theme import is_dark


class StatCard(QFrame):

    def __init__(
        self,
        title,
        value,
        icon,
        color,
        trend=""
    ):
        super().__init__()

        self.color = color

        self.setMinimumHeight(170)
        self.setMinimumWidth(170)

        self.build_ui(
            title,
            value,
            icon,
            trend
        )

    # --------------------------------------------------

    def build_ui(
        self,
        title,
        value,
        icon,
        trend
    ):

        self.setObjectName("StatCard")

        shadow = QGraphicsDropShadowEffect()

        shadow.setBlurRadius(30)

        shadow.setOffset(0,8)

        shadow.setColor(
            # Softer shadow on light themes
            QColor(0, 0, 0, 160 if is_dark() else 45)
        )

        self.setGraphicsEffect(shadow)

        root = QVBoxLayout(self)

        root.setContentsMargins(
            22,
            20,
            22,
            20
        )

        root.setSpacing(4)

        # -----------------------------------
        # Header
        # -----------------------------------

        top = QHBoxLayout()

        icon_label = QLabel()

        icon_label.setPixmap(

            qta.icon(
                icon,
                color=self.color
            ).pixmap(32,32)

        )

        top.addWidget(icon_label)

        top.addStretch()

        # Accent colour is passed in per card, so draw the dot as an icon
        badge = QLabel()

        badge.setPixmap(
            qta.icon(
                "fa5s.circle",
                color=self.color
            ).pixmap(12,12)
        )

        top.addWidget(badge)

        root.addLayout(top)

        # -----------------------------------
        # Title
        # -----------------------------------

        title_lbl = QLabel(title)

        title_lbl.setObjectName("StatTitle")


        root.addWidget(title_lbl)

        # -----------------------------------
        # Value
        # -----------------------------------

        value_lbl = QLabel(value)

        value_lbl.setObjectName("StatValue")


        root.addWidget(value_lbl)

        root.addStretch()

        # -----------------------------------
        # Trend
        # -----------------------------------

        trend_layout = QHBoxLayout()

        arrow = QLabel()

        arrow.setPixmap(

            qta.icon(
                "fa5s.arrow-up",
                color="#22C55E"
            ).pixmap(14,14)

        )

        trend_layout.addWidget(arrow)

        trend_lbl = QLabel(trend)

        trend_lbl.setObjectName("TrendText")


        trend_layout.addWidget(trend_lbl)

        trend_layout.addStretch()

        root.addLayout(trend_layout)

    # --------------------------------------------------

    def enterEvent(self,event):

        self.move(
            self.x(),
            self.y()-2
        )

        super().enterEvent(event)

    def leaveEvent(self,event):

        self.move(
            self.x(),
            self.y()+2
        )

        super().leaveEvent(event)