{
    "name": "Oil Workshop - Shift Management",
    "version": "1.0.0",
    "summary": "Shift closing, expenses and reports for oil workshop",
    "description": "Manage shifts, record sales & expenses and print thermal/formal closing reports.",
    "category": "Operations/Workshop",
    "author": "Generated for Muhammad Ali",
    "depends": ["base", "mail", "account", "sale"],
    "data": [
        "data/shift_sequence.xml",
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/shift_views.xml",
        "views/expense_views.xml",
        "views/sale_views.xml",
        "views/menus.xml",
        "reports/shift_report_thermal.xml",
        "reports/shift_report_formal.xml",
        "reports/shift_report_actions.xml"
    ],
    "installable": true,
    "application": false,
    "license": "LGPL-3"
}
