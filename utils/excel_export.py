"""Professional Excel (.xlsx) exports with a title, colours and totals.

Each sheet gets:
- shop name and report title at the top, the period and when it was made
- a coloured header row with filters, frozen so it stays visible
- alternating row shading, ₹ amounts, coloured status cells
- a totals row, sensible column widths, landscape page setup

Needs the XlsxWriter package:  pip install XlsxWriter
"""

from datetime import datetime

from services import settings_service

try:
    import xlsxwriter
except ImportError:  # handled by callers via is_available()
    xlsxwriter = None


class ExcelUnavailable(Exception):
    pass


def is_available() -> bool:
    return xlsxwriter is not None


# Column kinds: "text", "money", "int", "number", "status"
STATUS_COLOURS = {
    # status (lower case): (background, text)
    "pending": ("#FEF3C7", "#92400E"),
    "measurement": ("#E0E7FF", "#3730A3"),
    "cutting": ("#E0E7FF", "#3730A3"),
    "stitching": ("#E0E7FF", "#3730A3"),
    "ironing": ("#E0E7FF", "#3730A3"),
    "trial": ("#EDE9FE", "#5B21B6"),
    "ready": ("#D1FAE5", "#065F46"),
    "delivered": ("#DBEAFE", "#1E40AF"),
    "cancelled": ("#FEE2E2", "#991B1B"),
    "active": ("#D1FAE5", "#065F46"),
    "inactive": ("#F3F4F6", "#4B5563"),
    "in": ("#D1FAE5", "#065F46"),
    "out": ("#FEE2E2", "#991B1B"),
    "adjustment": ("#FEF3C7", "#92400E"),
}

NAVY = "#1E3A8A"
BORDER = "#D1D5DB"
STRIPE = "#F3F6FB"


class Column:
    def __init__(self, header, key, kind="text", width=None, total=False):
        self.header = header
        self.key = key
        self.kind = kind
        self.width = width
        self.total = total


class Sheet:
    def __init__(self, name, title, columns, rows, summary=None):
        """summary: optional list of (label, value, kind) shown above the table."""
        self.name = name[:31]
        self.title = title
        self.columns = columns
        self.rows = rows
        self.summary = summary or []


def export(path, report_title, sheets, period_text=""):
    """Write the sheets to an .xlsx file."""
    if not is_available():
        raise ExcelUnavailable(
            "Excel export needs the XlsxWriter package.\n\n"
            "Open a terminal in the project folder and run:\n    pip install XlsxWriter"
        )

    shop = settings_service.get_many(["shop_name", "shop_phone", "shop_address", "currency_symbol"])
    symbol = shop["currency_symbol"] or "₹"

    workbook = xlsxwriter.Workbook(path)
    workbook.set_properties({"title": report_title, "author": shop["shop_name"], "company": shop["shop_name"]})

    base = {"font_name": "Calibri", "font_size": 10, "valign": "vcenter"}

    def fmt(**extra):
        return workbook.add_format({**base, **extra})

    f = {
        "shop": fmt(bold=True, font_size=16, font_color=NAVY),
        "title": fmt(bold=True, font_size=13, font_color="#111827"),
        "meta": fmt(font_color="#6B7280", italic=True),
        "header": fmt(bold=True, font_color="#FFFFFF", bg_color=NAVY, border=1, border_color=NAVY,
                      align="center", text_wrap=True),
        "sum_label": fmt(bold=True, font_color="#374151", bg_color="#EEF2FF", border=1, border_color=BORDER),
        "sum_value": fmt(bold=True, font_color=NAVY, bg_color="#EEF2FF", border=1, border_color=BORDER,
                         align="right"),
        "sum_money": fmt(bold=True, font_color=NAVY, bg_color="#EEF2FF", border=1, border_color=BORDER,
                         num_format=f'"{symbol}"#,##0.00'),
        "empty": fmt(italic=True, font_color="#9CA3AF", align="center"),
    }

    def cell_format(kind, striped):
        key = (kind, striped)
        if key not in f:
            options = {"border": 1, "border_color": BORDER}
            if striped:
                options["bg_color"] = STRIPE
            if kind == "money":
                options["num_format"] = f'"{symbol}"#,##0.00'
            elif kind == "int":
                options.update(num_format="0", align="center")
            elif kind == "number":
                options["num_format"] = "#,##0.##"
            f[key] = fmt(**options)
        return f[key]

    def status_format(value):
        colours = STATUS_COLOURS.get(str(value).strip().lower())
        key = ("status", colours)
        if key not in f:
            options = {"border": 1, "border_color": BORDER, "align": "center", "bold": True}
            if colours:
                options.update(bg_color=colours[0], font_color=colours[1])
            f[key] = fmt(**options)
        return f[key]

    total_formats = {
        kind: fmt(bold=True, top=2, top_color=NAVY, bottom=1, bottom_color=BORDER, bg_color="#E5E7EB",
                  **({"num_format": f'"{symbol}"#,##0.00'} if kind == "money" else
                     {"num_format": "0", "align": "center"} if kind == "int" else
                     {"num_format": "#,##0.##"} if kind == "number" else {}))
        for kind in ("text", "money", "int", "number", "status")
    }

    generated = datetime.now().strftime("%d %b %Y, %I:%M %p")

    for sheet in sheets:
        ws = workbook.add_worksheet(sheet.name)
        last_col = max(0, len(sheet.columns) - 1)

        # ---------------- Heading block ----------------
        ws.set_row(0, 26)
        ws.merge_range(0, 0, 0, last_col, shop["shop_name"] or "Tailor Shop", f["shop"])
        contact = "  •  ".join(x for x in (shop["shop_phone"], shop["shop_address"].replace("\n", ", ")) if x)
        ws.merge_range(1, 0, 1, last_col, contact, f["meta"])
        ws.set_row(2, 22)
        ws.merge_range(2, 0, 2, last_col, sheet.title, f["title"])
        meta = f"Period: {period_text}   |   Generated: {generated}" if period_text else f"Generated: {generated}"
        ws.merge_range(3, 0, 3, last_col, meta, f["meta"])

        row = 5

        # ---------------- Summary (key figures) ----------------
        if sheet.summary:
            # Label across the first two columns so column A keeps its width
            value_col = 2 if len(sheet.columns) > 2 else 1
            for label, value, kind in sheet.summary:
                if value_col == 2:
                    ws.merge_range(row, 0, row, 1, label, f["sum_label"])
                else:
                    ws.write(row, 0, label, f["sum_label"])
                if kind == "money":
                    ws.write_number(row, value_col, float(value or 0), f["sum_money"])
                else:
                    ws.write(row, value_col, value, f["sum_value"])
                row += 1
            row += 1

        # ---------------- Table ----------------
        header_row = row
        ws.set_row(header_row, 24)
        for col, column in enumerate(sheet.columns):
            ws.write(header_row, col, column.header, f["header"])

        if not sheet.rows:
            ws.merge_range(header_row + 1, 0, header_row + 1, last_col, "No records for this period", f["empty"])

        widths = [max(len(c.header) + 4, 10) for c in sheet.columns]

        for index, item in enumerate(sheet.rows):
            r = header_row + 1 + index
            striped = index % 2 == 1
            for col, column in enumerate(sheet.columns):
                value = item.get(column.key, "") if isinstance(item, dict) else item[col]
                if value is None:
                    value = ""
                if column.kind in ("money", "number", "int"):
                    try:
                        number = float(value or 0)
                        ws.write_number(r, col, int(number) if column.kind == "int" else number,
                                        cell_format(column.kind, striped))
                    except (TypeError, ValueError):
                        ws.write(r, col, value, cell_format("text", striped))
                    shown = f"{symbol}{float(value or 0):,.2f}" if column.kind == "money" else str(value)
                elif column.kind == "status":
                    text = str(value).title()
                    ws.write(r, col, text, status_format(value))
                    shown = text
                else:
                    ws.write(r, col, str(value), cell_format("text", striped))
                    shown = str(value)
                widths[col] = max(widths[col], min(len(shown) + 3, 50))

        # ---------------- Totals ----------------
        if sheet.rows and any(c.total for c in sheet.columns):
            total_row = header_row + 1 + len(sheet.rows)
            for col, column in enumerate(sheet.columns):
                fmt_total = total_formats.get(column.kind, total_formats["text"])
                if col == 0:
                    ws.write(total_row, col, f"TOTAL ({len(sheet.rows)})", total_formats["text"])
                elif column.total:
                    first = xlsxwriter.utility.xl_rowcol_to_cell(header_row + 1, col)
                    last = xlsxwriter.utility.xl_rowcol_to_cell(total_row - 1, col)
                    values = [item.get(column.key) or 0 for item in sheet.rows]
                    try:
                        cached = sum(float(v) for v in values)
                    except (TypeError, ValueError):
                        cached = 0
                    ws.write_formula(total_row, col, f"=SUM({first}:{last})", fmt_total, cached)
                else:
                    ws.write_blank(total_row, col, None, fmt_total)

        # ---------------- Layout ----------------
        for col, column in enumerate(sheet.columns):
            ws.set_column(col, col, column.width or widths[col])

        ws.freeze_panes(header_row + 1, 0)
        if sheet.rows:
            ws.autofilter(header_row, 0, header_row + len(sheet.rows), last_col)

        ws.set_landscape()
        ws.set_paper(9)  # A4
        ws.fit_to_pages(1, 0)
        ws.repeat_rows(header_row)
        ws.set_margins(left=0.4, right=0.4, top=0.6, bottom=0.6)
        ws.set_header(f"&L&8{shop['shop_name']}&R&8{sheet.title}")
        ws.set_footer("&L&8Generated " + generated + "&RPage &P of &N")
        ws.hide_gridlines(2)

    workbook.close()
