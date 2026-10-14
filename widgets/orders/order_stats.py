from PySide6.QtWidgets import (
    QFrame,
    QGridLayout
)

from widgets.dashboard.stat_card import StatCard


class OrderStats(QFrame):

    def __init__(self):

        super().__init__()

        self.cards = {}

        self.build_ui()

    # ==========================================================

    def build_ui(self):

        self.setObjectName(
            "OrderStats"
        )

        self.setStyleSheet("""
            QFrame#OrderStats {
                background: transparent;
                border: none;
            }
        """)

        layout = QGridLayout(self)

        layout.setContentsMargins(
            0, 0, 0, 0
        )

        layout.setHorizontalSpacing(
            18
        )

        layout.setVerticalSpacing(
            18
        )

        definitions = [

            (
                "total",
                "Total Orders",
                "fa5s.shopping-bag",
                "#3B82F6"
            ),

            (
                "cutting",
                "Cutting",
                "fa5s.cut",
                "#F59E0B"
            ),

            (
                "stitching",
                "Stitching",
                "fa5s.tshirt",
                "#8B5CF6"
            ),

            (
                "trial",
                "Trial",
                "fa5s.user-check",
                "#06B6D4"
            ),

            (
                "ready",
                "Ready",
                "fa5s.box-open",
                "#22C55E"
            ),

            (
                "delivered",
                "Delivered",
                "fa5s.truck",
                "#10B981"
            ),

            (
                "pending_payment",
                "Pending Payment",
                "fa5s.wallet",
                "#EF4444"
            ),

            (
                "overdue",
                "Overdue",
                "fa5s.exclamation-triangle",
                "#DC2626"
            ),
        ]

        positions = [
            (0, 0),
            (0, 1),
            (0, 2),
            (0, 3),
            (1, 0),
            (1, 1),
            (1, 2),
            (1, 3),
        ]

        for (
            (key, title, icon, icon_color),
            (row, column)
        ) in zip(
            definitions,
            positions
        ):

            card = StatCard(
                title,
                "0",
                icon,
                icon_color,
                trend=""
            )

            self.cards[key] = card

            layout.addWidget(
                card,
                row,
                column
            )

    # ==========================================================

    def set_stats(self, stats):

        self.set_card(
            "total",
            stats.get("total", 0),
            "All orders"
        )

        self.set_card(
            "cutting",
            stats.get("cutting", 0),
            "In progress"
        )

        self.set_card(
            "stitching",
            stats.get("stitching", 0),
            "In progress"
        )

        self.set_card(
            "trial",
            stats.get("trial", 0),
            "Pending trial"
        )

        self.set_card(
            "ready",
            stats.get("ready", 0),
            "Ready for pickup"
        )

        self.set_card(
            "delivered",
            stats.get("delivered", 0),
            "Completed"
        )

        self.set_card(
            "pending_payment",
            f"₹{stats.get('pending_payment', 0):,.0f}",
            "Outstanding"
        )

        self.set_card(
            "overdue",
            stats.get("overdue", 0),
            "Delivery overdue"
        )

    # ==========================================================

    def set_card(
        self,
        key,
        value,
        trend
    ):

        card = self.cards.get(key)

        if not card:
            return

        # StatCard implementation dependent.
        # Most versions expose value/trend labels.
        if hasattr(card, "value_label"):

            card.value_label.setText(
                str(value)
            )

        if hasattr(card, "trend_label"):

            card.trend_label.setText(
                str(trend)
            )