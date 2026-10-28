

frappe.query_reports["Item In Out Summary"] = {
    filters: [
        {
            fieldname: "from_month",
            label: __("From Month"),
            fieldtype: "Select",
            options: [
                "January", "February", "March", "April",
                "May", "June", "July", "August",
                "September", "October", "November", "December"
            ],
            default: "January",
            reqd: 1
        },
        {
            fieldname: "to_month",
            label: __("To Month"),
            fieldtype: "Select",
            options: [
                "January", "February", "March", "April",
                "May", "June", "July", "August",
                "September", "October", "November", "December"
            ],
            default: "June",
            reqd: 1
        },
        {
            fieldname: "year",
            label: __("Year"),
            fieldtype: "Select",
            options: ["2023", "2024", "2025", "2026"],
            default: "2026",
            reqd: 1
        },
        {
            fieldname: "item_group",
            label: __("Item Group"),
            fieldtype: "Link",
            options: "Item Group"
        },
        {
            "fieldname": "company",
            "label": "Company",
            "fieldtype": "Link",
            "options": "Company",
            "default": frappe.defaults.get_user_default("Company"),
            "reqd": 1
        }
    ]
};