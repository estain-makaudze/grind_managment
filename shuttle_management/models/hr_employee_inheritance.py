# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import base64
import qrcode
from io import BytesIO
from odoo.exceptions import ValidationError


class EmployeeInheritance(models.Model):
    """THIS INHERITS EMPLOYEE TO ADD SHUTTLE MANAGEMENT FUNCTIONS"""
    _inherit = 'hr.employee'

    shuttles_model=fields.Many2one('shuttles.model', string='Shuttle', tracking=True)
    billing_tariff_id=fields.Many2one('billing_tariff.model', string='Billing Tariff',tracking=True)
    driver_login_id=fields.Char(string='Driver Login Id', tracking=True)
    shuttles_driver=fields.Many2one(related='shuttles_model.driver_id', string='Shuttle Driver')
    max_seating_capacity=fields.Integer(related='shuttles_model.capacity', store=True, string='Shuttle Max Seating Capacity')
    service_status=fields.Selection(related='shuttles_model.service_status', store=True, string='Shuttle Service Status')
    shuttle_route=fields.Many2many(related='shuttles_model.shuttle_route', string='Shuttle Route')
    employee_schedules_ids=fields.One2many('employee_schedules.model', 'employee_id', string='Driver Schedules')
    shuttle_onboard_history_ids=fields.One2many('shuttle_onboard_history.model', 'employee_id', string='Shuttle Onboard History')
    qr_code_image = fields.Binary(string="QR Code")
    street = fields.Char(related='address_home_id.street',string="Street")
    street2 = fields.Char(related='address_home_id.street2',string="Street2")
    city = fields.Char(related='address_home_id.city',string="City")
    old_qr_code = fields.Char(string="Old QR Code")
    onboarding_stage = fields.Selection([('new_employee', 'New Employee'),
                                         ('allocated_schedule', 'Allocated Schedule'),
                                         ('qr_code_printed', 'Qr Code Printed'),
                                         ('qr_code_collected', 'Qr Code Collected'),
                                         ('done', 'Done'),
                                         ],
                                        'Onboarding Stage', required=True, default='new_employee')

    @api.constrains('driver_login_id')
    def _check_driver_login_id(self):
        """CHECK IF DRIVER LOGIN ID IS UNIQUE"""
        for record in self:
            if record.driver_login_id:
                # Search for other records with the same driver_login_id
                existing_driver = self.search([
                    ('driver_login_id', '=', record.driver_login_id),
                    ('id', '!=', record.id)  # Ensure it's not the same record
                ], limit=1)

                if existing_driver:
                    raise ValidationError('The driver login ID must be unique. This one already exists!')

    def action_new_employee(self):
        self.onboarding_stage = 'new_employee'

    def action_qr_printed(self):
        self.onboarding_stage = 'qr_code_printed'

    def action_allocated_schedule(self):
        """THIS FUNCTION IS FOR ONBOARDING A NEW EMPLOYEE TO A SHUTTLE, SCHUDULE AND A DRIVER"""
        self.onboarding_stage = 'allocated_schedule'

    def action_qr_code_printed(self):
        self.onboarding_stage = 'qr_code_printed'

    def action_qr_code_collected(self):
        self.onboarding_stage = 'qr_code_collected'

    def action_done(self):
        self.onboarding_stage = 'done'

    def create_qr_code_for_employee(self):
        """Generates and saves a QR code for each employee."""
        for employee in self:
            #check if billing tarrif is filled in
            if not employee.billing_tariff_id:
                raise ValidationError(_(f"Please Select Billing Tarrif for {employee.name} so as to generate the Qr Code"))

            data = f"Name: {employee.name}, ID: {employee.id}, Code: {employee.x_studio_employee_code}"
            qr_code = self.generate_qr_code(data)
            employee.qr_code_image = qr_code

    def generate_qr_code(self, data):
        """Generates a QR code for the given data."""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue())


#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
