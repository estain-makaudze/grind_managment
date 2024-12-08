from odoo import fields, models, api


class BillingTariff(models.Model):
    _name = 'billing_tariff.model'
    _description = 'Billing Tariff'
    _rec_name='distance'

    distance = fields.Char(string="Distance (km)")
    price = fields.Monetary(string="Price")
    currency_id = fields.Many2one('res.currency', string="Employee", required=True, default=lambda self: self.env.ref('base.USD').id)

