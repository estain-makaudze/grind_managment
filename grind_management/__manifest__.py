# -*- coding: utf-8 -*-
{
    'name': "Grind management",
    'summary': """
        This is a Grind Management Module for managment of the grind shop at Zimworx
    """,
    'description': """
        This module server as purpose of managing inventory, meals, shop products for the grind shop
        It then further produce a basic POS Shop which allow Zimworx employess buy products on qrcode scanning
    """,
    'author': "Estain Makaudze",
    'website': "https://www.zimworx.com",
    'category': 'Inventory',
    'version': '16.24.0.1',
    'depends': ['base','mail', 'hr'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'wizards/grind_inventory_movement_wizard.xml',
        'views/main_menus.xml',
        'views/grind_inventory_model.xml',
        'views/grind_menu_model.xml',
        'views/hr_employee_inheritance.xml',
        'views/grind_sales_model.xml',
        'views/grind_inventory_category.xml',
        'views/grind_inventory_uom.xml',
        'views/grind_inventory_supplier.xml',
        'views/grind_shop_template.xml',
        'views/grind_checkout_qr_code_scan.xml',
    ],
    # 'assets': {
    #     'web.assets_backend': [
    #         'grind_management/static/src/js/category_products_template.js',
    #     ],
    # },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
    'auto_install': False,
}
