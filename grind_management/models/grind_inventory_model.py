# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import date, datetime

from pkg_resources import require


class GrindInventory(models.Model):
    _name = 'grind_inventory.model'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'Grind Inventory'

    name = fields.Char(string="Item Name", required=True)
    item_code = fields.Char(string="Item Code", required=True, help="Unique identifier for each item")
    category_id = fields.Many2one('grind_inventory.category', string="Category", help="Category the item belongs to")
    supplier_id = fields.Many2one('grind_inventory.supplier', string="Supplier", help="Supplier of the item")
    currency_id = fields.Many2one('res.currency', string="Currency")
    grind_inventory_movement_ids = fields.One2many('grind_inventory.movement', 'grind_inventory_id', string="Grind Movement")
    description = fields.Text(string="Description", help="Description of the item")
    cost_price = fields.Monetary(string="Cost Price", required=True, help="Purchase price of the item")
    sale_price = fields.Monetary(string="Sale Price", required=True, help="Selling price of the item")
    quantity_available = fields.Float(string="Available Quantity", compute='_compute_quantity_available',help="Quantity available in stock", readonly=1)
    reorder_quantity = fields.Float(string="Reorder Quantity", help="Quantity to reorder when stock is low")
    grind_inventory_uom_id = fields.Many2one('grind_inventory.uom', string="Unit of Measure", help="Unit of Measure for the item", required=True)
    date_added = fields.Date(string="Date Added", default=datetime.now(),  help="Date the item was added to inventory")
    active = fields.Boolean(string="Active", default=True, help="Is this item currently active?")
    inventory_type = fields.Selection([('shop_product', 'Shop Product'),
                                         ('ingredient', 'Ingredient'),
                                         ('both_product_ingredient', 'Both Shop Product & Ingredient'),
                                         ],
                                        'Inventory Type')
    menu_id = fields.Many2one('grind_menu.model', string="Menu",)


    def _compute_quantity_available(self):
        #calculate available quantity using inventory movements
        for rec in self:
            quantity_available=0
            for movement in rec.grind_inventory_movement_ids:
                #if movement is an stock in add the quantity_available
                if movement.movement_type =='stock_in':
                    quantity_available=quantity_available+movement.quantity
                elif movement.movement_type =='sell':
                    quantity_available = quantity_available - movement.quantity
                elif movement.movement_type =='balance':
                    quantity_available = quantity_available + movement.balance_quantity
            rec.quantity_available=quantity_available