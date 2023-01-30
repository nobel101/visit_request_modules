# -*- coding: utf-8 -*-
{
    'name': "Request For Visit Concrete",

    'summary': """
        detailed implementation of Request For Visit module abstract model for long and trainee visit requests""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.itqansystems.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['itq_visit_request_abstract','web'],

    # always loaded
    'data': [
        'data/ir_sequence.xml',
        'views/visit_request_long_views.xml',
        'views/action_visit_permission_views.xml',
        # report
        'reports/visit_request_long_report.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
