from odoo import fields, models, api, _
from datetime import date, datetime

class GrindInventoryMovementWizard(models.TransientModel):
    _name = 'grind_inventory_movement.wizard'
    _description = 'Grind Inventory Movement Wizard'

    grind_inventory_id = fields.Many2one('grind_inventory.model', string='Product', required=True)
    movement_type = fields.Selection([
        ('stock_in', 'Stock In'),
        ('sell', 'Sell Out'),
        ('balance', 'Balance')
    ], string='Movement Type', required=True, tracking=True)
    quantity = fields.Float(string='Quantity', required=True)
    current_quantity = fields.Float(string='Quantity', required=True)
    grind_inventory_uom_id = fields.Many2one('grind_inventory.uom', string='Unit of Measure', required=True)
    movement_date = fields.Datetime(string='Movement Date', default=datetime.now())

    @api.model
    def default_get(self, fields):
        # GET THE INVENTORY OF THE CURRENT OPEN INVENTORY ID
        res = super().default_get(fields)
        grind_inventory_movement = self.env['grind_inventory.model'].search([('id', '=', self._context.get('active_id'))])
        res['grind_inventory_id']=grind_inventory_movement.id
        res['current_quantity']=grind_inventory_movement.quantity_available
        res['grind_inventory_uom_id']=grind_inventory_movement.grind_inventory_uom_id.id
        return res

    def action_add_movement(self):
        """action to add the movement of the invetory"""
        if self.movement_type == 'balance':
            vals = {
                'grind_inventory_id': self.grind_inventory_id.id,
                'movement_date': self.movement_date,
                'balance_quantity': self.quantity - self.current_quantity,
                'quantity': self.quantity,
                'grind_inventory_uom_id': self.grind_inventory_uom_id.id,
                'movement_type': self.movement_type,
                'state': 'done',
            }
        else:
            vals = {
                'grind_inventory_id': self.grind_inventory_id.id,
                'movement_date': self.movement_date,
                'quantity': self.quantity,
                'grind_inventory_uom_id': self.grind_inventory_uom_id.id,
                'movement_type': self.movement_type,
                'state': 'done',
            }
        self.env['grind_inventory.movement'].create(vals)
