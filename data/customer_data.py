from dataclasses import dataclass, field
from typing import List
import sqlite3

from database.database import DB_PATH
import math


@dataclass
class CustomerRowData:
    id: int
    name: str
    mobile: str
    orders_count: int
    pending_amount: float
    last_visit: str
    status: str
    has_measurements: bool


@dataclass
class CustomerStatsData:
    total_customers: int
    new_this_month: int
    active_customers: int
    active_percentage: float
    inactive_customers: int
    vip_customers: int


@dataclass
class CustomerQueryResult:
    customers: List[CustomerRowData] = field(default_factory=list)
    total_count: int = 0
    total_pages: int = 1
    current_page: int = 1


class CustomerDataService:
    @staticmethod
    def get_connection():
        # Same database file that init_db() creates
        return sqlite3.connect(DB_PATH)

    @classmethod
    def fetch_stats(cls) -> CustomerStatsData:
        conn = cls.get_connection()
        cursor = conn.cursor()

        # Total Registered Customers
        cursor.execute("SELECT COUNT(*) FROM customers")
        total_customers = cursor.fetchone()[0] or 0

        # New Customers added this month
        cursor.execute("""
            SELECT COUNT(*) FROM customers 
            WHERE strftime('%m', created_at) = strftime('%m', 'now')
              AND strftime('%Y', created_at) = strftime('%Y', 'now')
        """)
        new_this_month = cursor.fetchone()[0] or 0

        # Active Customers
        cursor.execute("SELECT COUNT(*) FROM customers WHERE is_active = 1")
        active_customers = cursor.fetchone()[0] or 0

        # Inactive Customers
        cursor.execute("SELECT COUNT(*) FROM customers WHERE is_active = 0")
        inactive_customers = cursor.fetchone()[0] or 0

        # VIP Customers
        cursor.execute("SELECT COUNT(*) FROM customers WHERE LOWER(customer_type) = 'vip'")
        vip_customers = cursor.fetchone()[0] or 0

        active_percentage = (active_customers / total_customers * 100) if total_customers > 0 else 0.0

        conn.close()

        return CustomerStatsData(
            total_customers=total_customers,
            new_this_month=new_this_month,
            active_customers=active_customers,
            active_percentage=round(active_percentage, 1),
            inactive_customers=inactive_customers,
            vip_customers=vip_customers
        )

    @classmethod
    def fetch_customers(
        cls, 
        name_query: str = "", 
        mobile_query: str = "", 
        status_filter: str = "All Status", 
        type_filter: str = "All Customers", 
        page: int = 1, 
        page_size: int = 10
    ) -> CustomerQueryResult:
        conn = cls.get_connection()
        cursor = conn.cursor()

        where_clauses = []
        params = []

        if name_query.strip():
            where_clauses.append("c.name LIKE ?")
            params.append(f"%{name_query.strip()}%")

        if mobile_query.strip():
            # Match the main or the alternate number
            where_clauses.append("(c.mobile LIKE ? OR c.alternate_mobile LIKE ?)")
            params.extend([f"%{mobile_query.strip()}%"] * 2)

        if status_filter == "Active":
            where_clauses.append("c.is_active = 1")
        elif status_filter == "Inactive":
            where_clauses.append("c.is_active = 0")

        if type_filter != "All Customers":
            where_clauses.append("LOWER(c.customer_type) = LOWER(?)")
            params.append(type_filter)

        where_sql = ("WHERE " + " AND ".join(where_clauses)) if where_clauses else ""

        # Total matching records count
        count_sql = f"SELECT COUNT(*) FROM customers c {where_sql}"
        cursor.execute(count_sql, params)
        total_count = cursor.fetchone()[0] or 0

        total_pages = max(1, math.ceil(total_count / page_size))
        page = min(max(1, page), total_pages)
        offset = (page - 1) * page_size

        # Aggregated query matching exact model fields
        query = f"""
            SELECT 
                c.id,
                c.name,
                c.mobile,
                c.is_active,
                COUNT(DISTINCT o.id) as total_orders,
                COALESCE(SUM(
                    CASE WHEN LOWER(o.status) = 'cancelled' THEN 0
                         ELSE o.remaining_amount END
                ), 0.0) as total_pending,
                MAX(o.order_date) as last_order_date,
                (SELECT COUNT(*) FROM customer_measurements cm WHERE cm.customer_id = c.id) as measurement_count
            FROM customers c
            LEFT JOIN orders o ON c.id = o.customer_id
            {where_sql}
            GROUP BY c.id
            ORDER BY c.id DESC
            LIMIT ? OFFSET ?
        """
        cursor.execute(query, params + [page_size, offset])
        rows = cursor.fetchall()

        customers = []
        for row in rows:
            cid, name, mobile, is_active, orders_cnt, pending_amt, last_visit, m_count = row
            status_str = "Active" if is_active else "Inactive"
            last_visit_str = str(last_visit).split(" ")[0] if last_visit else "Never"

            customers.append(
                CustomerRowData(
                    id=cid,
                    name=name or "N/A",
                    mobile=mobile or "N/A",
                    orders_count=orders_cnt or 0,
                    pending_amount=float(pending_amt or 0.0),
                    last_visit=last_visit_str,
                    status=status_str,
                    has_measurements=(m_count > 0)
                )
            )

        conn.close()

        return CustomerQueryResult(
            customers=customers,
            total_count=total_count,
            total_pages=total_pages,
            current_page=page
        )