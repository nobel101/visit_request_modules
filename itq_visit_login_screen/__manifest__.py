# -*- coding: utf-8 -*-
{
    'name': "Visit Login Screen",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

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
    'depends': ['itq_long_visit_request_concrete'],

    # always loaded
    'data': [
        'views/visit_permission_login_views.xml',
        'views/visit_permission_views.xml',

    ],

}
