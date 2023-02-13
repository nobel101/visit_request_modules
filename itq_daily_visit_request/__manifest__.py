# -*- coding: utf-8 -*-
{
    'name': "Daily Visit Request",

    'summary': """
        detailed implementation of Daily Visit Request module abstract model for visit requests""",

    'description': """
        Long description of module's purpose
    """,

    'author': "itqan",
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
        'views/daily_visit_request_views.xml',
        'views/visit_request_daily_line.xml',
    ],
    # only loaded in demonstration mode
}
