# -*- coding: utf-8 -*-
{
    'name': "Help Desk",

    'summary': """
        This module allows a customer to
        submit and review their ticket sstatus in a clear and concise manner""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Iatl-Intellisoft",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail','contacts','portal','website',],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'report/report_team_tickets_data.xml',
        'report/tickets_report.xml',
        'views/views.xml',
        'wizard/ticket_team_report_wizard.xml',
        'views/inherited_views.xml',
        'views/tickets_portal.xml',
    ],

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
