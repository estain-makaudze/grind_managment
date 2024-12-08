from odoo import fields, models, api
from datetime import date


class ShuttleOnboardHistory(models.Model):
    _name = 'shuttle_onboard_history.model'
    _description = 'Shuttle Onboard History'

    onboard_date_time = fields.Datetime(string='Onboard Date Time', required=True)
    onboard_date = fields.Date(string='Onboard Date', required=True)
    employee_id = fields.Many2one('hr.employee', string='Shuttle', required=True)
    driver_id = fields.Many2one('hr.employee', string='driver', required=True)
    shuttle_id = fields.Many2one('shuttles.model', string='Shuttle', readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        res = super(ShuttleOnboardHistory, self).create(vals_list)
        # Get the start and end dates for the current month
        today = date.today()
        month_start = today.replace(day=1)
        month_end = today.replace(day=1).replace(month=today.month + 1) if today.month < 12 else today.replace(day=31, month=12)
        # Loop through each record created
        for record in res:
            employee_expense_exists = self.env['employee_expense.model'].search([
                ('employee_id', '=', record.employee_id.id),
                ('create_date', '>=', month_start),
                ('create_date', '<', month_end)
            ])
            if employee_expense_exists:
                # upate a record which the bill of the shuttle
                for rec in employee_expense_exists:
                    employee_expense_exists.write({
                        'shuttle_deduction': record.employee_id.billing_tariff_id.price if record.employee_id.billing_tariff_id else 0,
                    })
            else:
                # create a record which the bill of the shuttle
                self.env['employee_expense.model'].create({
                    'employee_id': record.employee_id.id,
                    'shuttle_deduction': record.employee_id.billing_tariff_id.price if record.employee_id.billing_tariff_id else 0 ,
                })
        return res