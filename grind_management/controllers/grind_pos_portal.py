# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request



class GrindPortalPos(http.Controller):
    @http.route('/grind_shop', auth='user')
    def index(self, **kw):
        #get the current categories available
        grind_inventory_model= request.env['grind_inventory.model'].search([])
        grind_menu_ingredient= request.env['grind_menu_ingredient.model'].search([])

        return request.render('grind_management.grind_shop_template',{
            'category_inventory_no':len(grind_inventory_model),
            'category_ingredient_no':len(grind_menu_ingredient),
            'category_inventory_ids':grind_inventory_model,
            'category_ingredient_ids':grind_menu_ingredient,
        })

    @http.route('/temp_view', auth='user')
    def temp_view(self, **kw):
        # get the current categories available
        grind_inventory_model = request.env['grind_inventory.model'].search([])
        grind_menu_ingredient = request.env['grind_menu_ingredient.model'].search([])

        return request.render('grind_management.TempViewTemplate', {
            'category_inventory_no': len(grind_inventory_model),
            'category_ingredient_no': len(grind_menu_ingredient),
            'category_inventory_ids': grind_inventory_model,
            'category_ingredient_ids': grind_menu_ingredient,
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
