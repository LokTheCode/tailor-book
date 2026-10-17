from dataclasses import dataclass, field
from typing import List, Tuple
from pathlib import Path
import sqlite3

from database.database import DB_PATH as APP_DB_PATH


# ==========================================================
# DATABASE PATH
# ==========================================================

# Use the same database file that init_db() creates
# (%LOCALAPPDATA%\TailorManagement\tailor.db on Windows)
DB_PATH = Path(APP_DB_PATH)


# ==========================================================
# DATA CLASSES
# ==========================================================

@dataclass
class DeliveryItemData:

    time: str

    customer: str

    dress: str

    color: str


@dataclass
class DashboardData:

    stats: List[
        Tuple[str, str, str, str, str]
    ] = field(default_factory=list)

    recent_orders: List[
        List[str]
    ] = field(default_factory=list)

    deliveries: List[
        DeliveryItemData
    ] = field(default_factory=list)

    revenue_series: List[
        float
    ] = field(default_factory=list)

    order_status: List[
        Tuple[str, int, str]
    ] = field(default_factory=list)


# ==========================================================
# DASHBOARD DATA SERVICE
# ==========================================================

class DashboardDataService:

    # ------------------------------------------------------
    # DATABASE CONNECTION
    # ------------------------------------------------------

    @staticmethod
    def get_connection():

        # Make sure database directory exists
        DB_PATH.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        connection = sqlite3.connect(
            str(DB_PATH)
        )

        return connection

    # ------------------------------------------------------
    # FETCH DASHBOARD DATA
    # ------------------------------------------------------

    @classmethod
    def fetch_latest(
        cls
    ) -> DashboardData:

        conn = None

        try:

            conn = cls.get_connection()

            cursor = conn.cursor()

            # ==================================================
            # STATUS COLORS
            # ==================================================

            status_colors = {

                "Ready":
                    "#22C55E",

                "ready":
                    "#22C55E",

                "Stitching":
                    "#3B82F6",

                "stitching":
                    "#3B82F6",

                "Cutting":
                    "#F59E0B",

                "cutting":
                    "#F59E0B",

                "Pending":
                    "#EF4444",

                "pending":
                    "#EF4444",

                "Delivered":
                    "#8B5CF6",

                "delivered":
                    "#8B5CF6",

                "Cancelled":
                    "#6B7280",

                "cancelled":
                    "#6B7280"
            }

            # ==================================================
            # 1. TOTAL REGISTERED CUSTOMERS
            # ==================================================

            cursor.execute("""
                SELECT COUNT(*)
                FROM customers
                WHERE is_active = 1
            """)

            total_customers = (
                cursor.fetchone()[0]
                or 0
            )

            # ==================================================
            # 2. TODAY'S ORDERS
            # ==================================================

            cursor.execute("""
                SELECT COUNT(*)
                FROM orders
                WHERE DATE(order_date)
                    = DATE('now', 'localtime')
            """)

            today_orders = (
                cursor.fetchone()[0]
                or 0
            )

            # ==================================================
            # 3. MONTHLY REVENUE
            # ==================================================

            cursor.execute("""
                SELECT COALESCE(
                    SUM(amount),
                    0
                )

                FROM order_payments

                WHERE strftime(
                    '%m',
                    payment_date
                ) = strftime(
                    '%m',
                    'now',
                    'localtime'
                )

                AND strftime(
                    '%Y',
                    payment_date
                ) = strftime(
                    '%Y',
                    'now',
                    'localtime'
                )
            """)

            monthly_revenue = (
                cursor.fetchone()[0]
                or 0
            )

            # ==================================================
            # 4. TOTAL MEASUREMENT PROFILES
            # ==================================================

            cursor.execute("""
                SELECT COUNT(*)
                FROM customer_measurements
            """)

            total_measurements = (
                cursor.fetchone()[0]
                or 0
            )

            # ==================================================
            # 5. LOW STOCK ITEMS
            # ==================================================

            cursor.execute("""
                SELECT COUNT(*)

                FROM inventory_items

                WHERE quantity <= minimum_quantity

                AND is_active = 1
            """)

            low_stock_items = (
                cursor.fetchone()[0]
                or 0
            )

            # ==================================================
            # STATS
            # ==================================================

            stats = [

                (
                    "Customers",
                    f"{total_customers:,}",
                    "fa5s.users",
                    "#10B981",
                    "Total Registered"
                ),

                (
                    "Today's Orders",
                    str(today_orders),
                    "fa5s.clipboard-list",
                    "#3B82F6",
                    "New Today"
                ),

                (
                    "Revenue",
                    f"₹{monthly_revenue:,.2f}",
                    "fa5s.rupee-sign",
                    "#F59E0B",
                    "This Month"
                ),

                (
                    "Measurements",
                    str(total_measurements),
                    "fa5s.ruler",
                    "#06B6D4",
                    "Saved Profiles"
                ),

                (
                    "Low Stock Items",
                    str(low_stock_items),
                    "fa5s.exclamation-triangle",
                    "#EF4444",
                    "Inventory Alert"
                ),

            ]

            # ==================================================
            # 6. RECENT 5 ORDERS
            # ==================================================

            cursor.execute("""
                SELECT

                    o.order_number,

                    c.name,

                    COALESCE(
                        (
                            SELECT garment_type
                            FROM order_items
                            WHERE order_id = o.id
                            LIMIT 1
                        ),
                        'N/A'
                    ) AS garment,

                    COALESCE(
                        o.delivery_date,
                        'N/A'
                    ),

                    COALESCE(
                        o.status,
                        'pending'
                    ),

                    COALESCE(
                        o.total_amount,
                        0
                    )

                FROM orders o

                LEFT JOIN customers c
                    ON o.customer_id = c.id

                ORDER BY o.id DESC

                LIMIT 5
            """)

            recent_orders = [

                [

                    row[0],

                    row[1] or "Walk-in",

                    row[2],

                    str(row[3]),

                    row[4].capitalize(),

                    f"₹{row[5]:,.2f}"

                ]

                for row in cursor.fetchall()

            ]

            # ==================================================
            # 7. TODAY'S SCHEDULED DELIVERIES
            # ==================================================

            cursor.execute("""
                SELECT

                    c.name,

                    COALESCE(
                        (
                            SELECT garment_type
                            FROM order_items
                            WHERE order_id = o.id
                            LIMIT 1
                        ),
                        'Garment'
                    ) AS garment,

                    COALESCE(
                        o.status,
                        'pending'
                    )

                FROM orders o

                LEFT JOIN customers c
                    ON o.customer_id = c.id

                WHERE DATE(o.delivery_date)
                    = DATE(
                        'now',
                        'localtime'
                    )
            """)

            deliveries = [

                DeliveryItemData(

                    time="Today",

                    customer=(
                        row[0]
                        or "Customer"
                    ),

                    dress=row[1],

                    color=status_colors.get(
                        row[2].lower(),
                        "#3B82F6"
                    )

                )

                for row in cursor.fetchall()

            ]

            # ==================================================
            # 8. MONTHLY REVENUE BREAKDOWN
            #    CURRENT YEAR
            # ==================================================

            cursor.execute("""
                SELECT

                    strftime(
                        '%m',
                        payment_date
                    ) AS m,

                    SUM(amount)

                FROM order_payments

                WHERE strftime(
                    '%Y',
                    payment_date
                ) = strftime(
                    '%Y',
                    'now',
                    'localtime'
                )

                GROUP BY m

                ORDER BY m ASC
            """)

            rev_dict = {

                int(row[0]): (
                    row[1] or 0
                )

                for row in cursor.fetchall()

                if row[0] is not None

            }

            revenue_series = [

                float(
                    rev_dict.get(
                        month,
                        0.0
                    )
                )

                for month in range(
                    1,
                    13
                )

            ]

            # ==================================================
            # 9. ORDER STATUS BREAKDOWN
            # ==================================================

            cursor.execute("""
                SELECT

                    status,

                    COUNT(*)

                FROM orders

                GROUP BY status
            """)

            order_status = [

                (

                    (
                        row[0].capitalize()
                        if row[0]
                        else "Unknown"
                    ),

                    row[1],

                    status_colors.get(

                        (
                            row[0].lower()
                            if row[0]
                            else ""
                        ),

                        "#3B82F6"

                    )

                )

                for row in cursor.fetchall()

            ]

            # ==================================================
            # RETURN
            # ==================================================

            return DashboardData(

                stats=stats,

                recent_orders=recent_orders,

                deliveries=deliveries,

                revenue_series=revenue_series,

                order_status=order_status

            )

        finally:

            if conn is not None:

                conn.close()