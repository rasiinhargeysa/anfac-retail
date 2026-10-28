import frappe
from datetime import date, timedelta


MONTHS = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12
}

MONTH_NAMES = {v: k for k, v in MONTHS.items()}


def execute(filters=None):
    filters = filters or {}

    month_range = get_month_range(filters)
    columns = get_columns(filters, month_range)
    data = get_data(filters, month_range)

    return columns, data


def get_month_range(filters):
    """
    Returns list of month numbers between
    from_month and to_month.
    """

    from_num = MONTHS.get(filters.get("from_month"), 1)
    to_num = MONTHS.get(filters.get("to_month"), 12)

    if from_num > to_num:
        frappe.throw(
            "From Month must be before or equal to To Month."
        )

    return list(range(from_num, to_num + 1))


def get_columns(filters, month_range):

    columns = [
        {
            "label": "Sn",
            "fieldname": "sn",
            "fieldtype": "Int",
            "width": 50
        },
        {
            "label": "Brand Name",
            "fieldname": "item_code",
            "fieldtype": "Link",
            "options": "Item",
            "width": 150
        },
        {
            "label": "Description",
            "fieldname": "item_name",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "label": "Original QTY",
            "fieldname": "original_qty",
            "fieldtype": "Float",
            "width": 130
        },
        {
            "label": "In QTY",
            "fieldname": "in_qty",
            "fieldtype": "Float",
            "width": 110
        },
    ]

    for m in month_range:

        mname = MONTH_NAMES[m]

        columns += [
            {
                "label": f"Sold ({mname})",
                "fieldname": f"sold_{m}",
                "fieldtype": "Float",
                "width": 120
            },
            {
                "label": f"Balance ({mname})",
                "fieldname": f"balance_{m}",
                "fieldtype": "Float",
                "width": 120
            },
            {
                "label": f"Sold % ({mname})",
                "fieldname": f"pct_{m}",
                "fieldtype": "Percent",
                "width": 110
            },
        ]

    columns += [
        {
            "label": "Total Sold",
            "fieldname": "total_sold",
            "fieldtype": "Float",
            "width": 120
        },
        {
            "label": "Total Sold %",
            "fieldname": "total_sold_pct",
            "fieldtype": "Percent",
            "width": 120
        },
    ]

    return columns


def get_data(filters, month_range):

    year = int(filters.get("year", 2026))

    # ---------------------------------------------------------
    # ORIGINAL QTY CUTOFF
    # ---------------------------------------------------------
    #
    # Original QTY represents stock balance at the end of
    # the month BEFORE the selected From Month.
    #
    # Example:
    #
    # From Month = June 2026
    #
    # Original QTY = stock balance as of:
    # 31-May-2026
    #
    # If From Month = January 2026:
    # cutoff becomes 31-Dec-2025.
    #

    from_month_num = MONTHS.get(
        filters.get("from_month"),
        1
    )

    first_day_of_from_month = date(
        year,
        from_month_num,
        1
    )

    cutoff_date = (
        first_day_of_from_month
        - timedelta(days=1)
    )

    # ---------------------------------------------------------
    # IN QTY DATE RANGE
    # ---------------------------------------------------------
    #
    # In QTY is calculated inside selected:
    #
    # From Month -> To Month
    #
    # Example:
    #
    # From Month = June
    # To Month = August
    #
    # 01-Jun-2026 -> 31-Aug-2026
    #

    to_month_num = MONTHS.get(
        filters.get("to_month"),
        12
    )

    range_start_date = first_day_of_from_month

    if to_month_num == 12:

        range_end_date = date(
            year,
            12,
            31
        )

    else:

        range_end_date = (
            date(
                year,
                to_month_num + 1,
                1
            )
            - timedelta(days=1)
        )

    # ---------------------------------------------------------
    # ITEM GROUP FILTER
    # ---------------------------------------------------------

    item_group_condition = ""

    if filters.get("item_group"):

        item_group_condition = """
            AND item.item_group = %(item_group)s
        """

    # ---------------------------------------------------------
    # COMPANY FILTER
    # ---------------------------------------------------------

    company = filters.get("company")

    sle_company_condition = ""
    sle_in_company_condition = ""
    si_company_condition = ""

    if company:

        # Original QTY company condition
        sle_company_condition = """
            AND sle.warehouse IN (
                SELECT name
                FROM `tabWarehouse`
                WHERE company = %(company)s
            )
        """

        # In QTY company condition
        sle_in_company_condition = """
            AND sle_in.warehouse IN (
                SELECT name
                FROM `tabWarehouse`
                WHERE company = %(company)s
            )
        """

        # Sales Invoice company condition
        si_company_condition = """
            AND si.company = %(company)s
        """

    # ---------------------------------------------------------
    # MONTHLY SOLD SUBQUERIES
    # ---------------------------------------------------------

    sold_subqueries = ""

    for m in month_range:

        sold_subqueries += f"""
            ,
            COALESCE(
                (
                    SELECT SUM(sii.qty)

                    FROM `tabSales Invoice Item` sii

                    INNER JOIN `tabSales Invoice` si
                        ON si.name = sii.parent

                    WHERE sii.item_code = item.item_code

                      AND si.docstatus = 1

                      AND MONTH(si.posting_date) = {m}

                      AND YEAR(si.posting_date) = %(year)s

                      {si_company_condition}

                ),
                0
            ) AS sold_{m}
        """

    # ---------------------------------------------------------
    # MAIN SQL
    # ---------------------------------------------------------

    sql = """
        SELECT

            item.item_code,

            item.item_name,

            /*
            ---------------------------------------------------
            ORIGINAL QTY
            ---------------------------------------------------

            For every warehouse:

            Find the LAST Stock Ledger Entry on or before
            cutoff_date.

            Take qty_after_transaction from that entry.

            Then sum balances from all applicable warehouses.
            */

            COALESCE(
                (
                    SELECT SUM(
                        sle.qty_after_transaction
                    )

                    FROM `tabStock Ledger Entry` sle

                    WHERE sle.item_code = item.item_code

                      AND sle.is_cancelled = 0

                      AND sle.posting_date
                          <= %(cutoff_date)s

                      {sle_company_condition}

                      AND NOT EXISTS (

                          SELECT 1

                          FROM `tabStock Ledger Entry` sle2

                          WHERE sle2.item_code
                                = sle.item_code

                            AND sle2.warehouse
                                = sle.warehouse

                            AND sle2.is_cancelled = 0

                            AND sle2.posting_date
                                <= %(cutoff_date)s

                            AND (

                                sle2.posting_date
                                    > sle.posting_date

                                OR (

                                    sle2.posting_date
                                        = sle.posting_date

                                    AND sle2.posting_time
                                        > sle.posting_time
                                )

                                OR (

                                    sle2.posting_date
                                        = sle.posting_date

                                    AND sle2.posting_time
                                        = sle.posting_time

                                    AND sle2.creation
                                        > sle.creation
                                )
                            )
                      )
                ),
                0
            ) AS original_qty,


            /*
            ---------------------------------------------------
            IN QTY
            ---------------------------------------------------

            Sum positive Stock Ledger Entry actual_qty
            movements during selected date range.

            Example:

            June -> August

            01-Jun -> 31-Aug
            */

            COALESCE(
                (
                    SELECT SUM(

                        CASE

                            WHEN sle_in.actual_qty > 0
                            THEN sle_in.actual_qty

                            ELSE 0

                        END
                    )

                    FROM `tabStock Ledger Entry` sle_in

                    WHERE sle_in.item_code
                          = item.item_code

                      AND sle_in.is_cancelled = 0
                      AND sle_in.voucher_type != 'Stock Entry'

                      AND sle_in.posting_date
                          >= %(range_start_date)s

                      AND sle_in.posting_date
                          <= %(range_end_date)s

                      {sle_in_company_condition}

                ),
                0
            ) AS in_qty


            {sold_subqueries}


        FROM `tabItem` item


        WHERE item.disabled = 0

          AND item.is_stock_item = 1

          {item_group_condition}


        ORDER BY item.item_name ASC

    """.format(

        sold_subqueries=sold_subqueries,

        item_group_condition=item_group_condition,

        sle_company_condition=sle_company_condition,

        sle_in_company_condition=sle_in_company_condition
    )

    # ---------------------------------------------------------
    # EXECUTE SQL
    # ---------------------------------------------------------

    rows = frappe.db.sql(
        sql,
        {
            "year": year,

            "cutoff_date": cutoff_date,

            "range_start_date": range_start_date,

            "range_end_date": range_end_date,

            "item_group": filters.get("item_group"),

            "company": company
        },
        as_dict=1
    )

    # ---------------------------------------------------------
    # BUILD REPORT RESULT
    # ---------------------------------------------------------

    result = []

    for i, row in enumerate(
        rows,
        start=1
    ):

        original = row.original_qty or 0

        in_qty = row.in_qty or 0

        total_sold = 0

        entry = {

            "sn": i,

            "item_code": row.item_code,

            "item_name": row.item_name,

            "original_qty": original,

            "in_qty": in_qty,
        }

        # -----------------------------------------------------
        # BALANCE
        # -----------------------------------------------------
        #
        # Balance starts with:
        #
        # Original QTY + In QTY
        #
        # Then each month's sold quantity is deducted.
        #
        # Formula:
        #
        # Balance =
        # Original QTY + In QTY - Cumulative Sold QTY
        #

        running_balance = original + in_qty

        for m in month_range:

            sold = (
                row.get(f"sold_{m}")
                or 0
            )

            # ---------------------------------------------
            # NEW BALANCE FORMULA
            # ---------------------------------------------

            running_balance -= sold

            pct = (
                round(
                    sold / original * 100,
                    2
                )
                if original
                else 0
            )

            total_sold += sold

            entry[f"sold_{m}"] = sold

            entry[f"balance_{m}"] = (
                running_balance
            )

            entry[f"pct_{m}"] = pct

        # -----------------------------------------------------
        # TOTAL SOLD
        # -----------------------------------------------------

        entry["total_sold"] = total_sold

        entry["total_sold_pct"] = (
            round(
                total_sold / original * 100,
                2
            )
            if original
            else 0
        )

        # -----------------------------------------------------
        # SKIP ITEMS WITH NO ACTIVITY
        # -----------------------------------------------------

        if (
            total_sold == 0
            and original == 0
        ):
            continue

        result.append(entry)

    return result