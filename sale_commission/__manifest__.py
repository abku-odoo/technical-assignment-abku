# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Sales Commission',
    'description': "Specification of module",
    'license': 'LGPL-3',
    
    'depends': ['base', 'sale_management'],
    'data': [
        "security/ir.model.access.csv",
        "views/sale_commission_period_views.xml",
        "views/commission_plan_method_views.xml",
        "views/commission_plan_views.xml",
        "views/sale_commission_plans_report_views.xml",
        "views/sale_commission_menus.xml",
        ],

    'installable': True,
    'application': True,
    'auto_install' : False,
}
