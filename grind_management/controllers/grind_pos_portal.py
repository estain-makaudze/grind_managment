# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json



class GrindPortalPos(http.Controller):
    @http.route('/grind_shop', auth='user')
    def grind_index(self, **kw):
        # get the current categories available
        grind_inventory_model = request.env['grind_inventory.model'].search([])
        grind_menu_ingredient = request.env['grind_menu.model'].search([])

        return request.render('grind_management.grind_shop_template', {
            'category_inventory_no': len(grind_inventory_model),
            'category_ingredient_no': len(grind_menu_ingredient),
        })

    @http.route('/grind_shop_products', type='http', auth='user', csrf=False, methods=['POST'])
    def grind_shop_products(self, **kw):
        grind_inventory_model = request.env['grind_inventory.model'].search([])
        grind_menu_model = request.env['grind_menu.model'].search([])

        inventory_products = [
            {
                'id': product.item_code,
                'name': product.name,
                'price': product.sale_price,
                'available_quantity': product.sale_price,
                'category': "Inventory",
            } for product in grind_inventory_model
        ]

        menu_ingredients = [
            {
                'id': menu.menu_code,
                'name': menu.name,
                'price': menu.sale_price,
                'category': "Menu",
            } for menu in grind_menu_model
        ]

        return request.make_response(
            json.dumps({
                'inventory_products': inventory_products,
                'menu_ingredients': menu_ingredients,
            }),
            headers={'Content-Type': 'application/json'}
        )
    
    @http.route('/checkout', type='json', auth='user', csrf=False, methods=['POST'])
    def checkout(self):
        #RECORD A TRANSACTION IN SALES
        #RECORD A TRANSACTION IN INVENTORY
        #RECORD A TRANSACTION IN EMPLOYEE EXPENSES

        # order = request.env['grind_order.model'].create({
        #     'order_date': fields.Date.today(),
        #     'order_status': 'draft',
        # })

        data = http.request.params
        print(data)

        return {
                'status': 'ok',
                'data1': 'Some random data'     
            }


    @http.route('/grind_shop/scan_qr', type='json', auth='user', csrf=False, methods=['POST', 'GET'])
    def grind_shop_scan_qr(self):
        cart = http.request.params

        return request.render('grind_management.grind_checkout_qr_code_scan', {
            'cart': cart,
        })

#     @http.route('/grind_management/grind_management/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('grind_management.listing', {
#             'root': '/grind_management/grind_management',
#             'objects': http.request.env['grind_management.grind_management'].search([]),
#         })

#     @http.route('/grind_management/grind_management/objects/<model("grind_management.grind_management"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('grind_management.object', {
#             'object': obj
#         })
