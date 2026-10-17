from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
)

from widgets.dashboard.stat_card import StatCard


class MeasurementStats(QFrame):

    def __init__(self):

        super().__init__()

        self.cards = {}

        self.build_ui()

    # ======================================================
    # UI
    # ======================================================

    def build_ui(self):

        self.setObjectName(
            "MeasurementStats"
        )


        layout = QGridLayout(self)

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout.setHorizontalSpacing(18)
        layout.setVerticalSpacing(18)

        cards = [

            (
                "measurements",
                "Measurements",
                "0",
                "fa5s.ruler",
                "#3B82F6",
                "Total",
            ),

            (
                "shirts",
                "Shirts",
                "0",
                "fa5s.tshirt",
                "#10B981",
                "Total",
            ),

            (
                "pants",
                "Pants",
                "0",
                "fa5s.user-tie",
                "#F59E0B",
                "Total",
            ),

            (
                "suits",
                "Suits",
                "0",
                "fa5s.user",
                "#8B5CF6",
                "Total",
            ),

            (
                "today",
                "Today's Added",
                "0",
                "fa5s.plus-circle",
                "#06B6D4",
                "Today",
            ),

            (
                "updated",
                "Updated Today",
                "0",
                "fa5s.sync-alt",
                "#EF4444",
                "Today",
            ),

            (
                "customers",
                "Customers",
                "0",
                "fa5s.users",
                "#22C55E",
                "Unique",
            ),

            (
                "pending",
                "Pending",
                "0",
                "fa5s.clock",
                "#F97316",
                "Review",
            ),
        ]

        for index, item in enumerate(cards):

            key = item[0]

            card = StatCard(
                item[1],
                item[2],
                item[3],
                item[4],
                trend=item[5],
            )

            row = index // 4
            column = index % 4

            layout.addWidget(
                card,
                row,
                column,
            )

            self.cards[key] = card

    # ======================================================
    # UPDATE
    # ======================================================

    def set_stats(self, stats):

        self._set_card(
            "measurements",
            stats.get("total", 0),
        )

        self._set_card(
            "shirts",
            stats.get("shirts", 0),
        )

        self._set_card(
            "pants",
            stats.get("pants", 0),
        )

        self._set_card(
            "suits",
            stats.get("suits", 0),
        )

        self._set_card(
            "today",
            stats.get("today", 0),
        )

        self._set_card(
            "updated",
            stats.get("updated_today", 0),
        )

        self._set_card(
            "customers",
            stats.get("customers", 0),
        )

        # Pending will become meaningful when
        # measurement review/status is introduced.
        self._set_card(
            "pending",
            0,
        )

    # ======================================================
    # CARD VALUE
    # ======================================================

    def _set_card(self, key, value):

        card = self.cards.get(key)

        if not card:
            return

        value = f"{value:,}"

        # StatCard implementation may use different
        # internal QLabel names. Support the common ones.

        if hasattr(card, "value_label"):

            card.value_label.setText(value)

        elif hasattr(card, "value"):

            if hasattr(card.value, "setText"):
                card.value.setText(value)

        else:

            # Find QLabel by object name if your StatCard
            # uses one.
            from PySide6.QtWidgets import QLabel

            labels = card.findChildren(
                QLabel
            )

            for label in labels:

                if label.objectName() in (
                    "Value",
                    "value",
                    "StatValue",
                ):
                    label.setText(value)
                    break