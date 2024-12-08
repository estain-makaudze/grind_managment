from odoo import fields, models, api
import csv
import base64
import io
from datetime import datetime



class UploadExternalShuttleSchedules(models.TransientModel):
    _name = 'upload_external_shuttle_schedules.wizard'

    excell_sheet = fields.Binary(string="Excell Sheet")
    excell_name = fields.Char(string="Excell Sheet")

    def _format_datetime(self, date_str, time_str):
        """Convert date and time strings to Odoo datetime format"""
        try:
            # Parse the date (assuming format DD/MM/YYYY)
            date_obj = datetime.strptime(date_str, '%d/%m/%Y')

            # Parse the time (handling both 12-hour and 24-hour formats)
            try:
                # Try 12-hour format (e.g., "04:00:00 PM")
                time_obj = datetime.strptime(time_str, '%I:%M:%S %p')
            except ValueError:
                try:
                    # Try 24-hour format (e.g., "16:00:00")
                    time_obj = datetime.strptime(time_str, '%H:%M:%S')
                except ValueError:
                    # Try without seconds
                    try:
                        time_obj = datetime.strptime(time_str, '%I:%M %p')
                    except ValueError:
                        time_obj = datetime.strptime(time_str, '%H:%M')

            # Combine date and time
            combined_datetime = datetime.combine(date_obj.date(), time_obj.time())

            # Format to Odoo's expected format
            return combined_datetime

        except ValueError as e:
            raise ValueError(f"Invalid date/time format. Date: {date_str}, Time: {time_str}. Error: {str(e)}")

    def upload_external_shuttle_schedules(self):
        if not self.excell_sheet:
            return

        csv_data = base64.b64decode(self.excell_sheet)
        csv_file = io.StringIO(csv_data.decode('utf-8'))
        reader = csv.reader(csv_file, delimiter=',')

        # Skip header if exists
        next(reader, None)

        # Track successful and failed records
        success_count = 0
        failed_records = []

        for row in reader:
            # Search if the shuttle exists
            shuttles_model = self.env['shuttles.model'].search([('name', 'ilike', row[0])])
            employee_id = self.env['hr.employee'].search([('name', 'ilike', row[1])])
            if shuttles_model and employee_id:
                # Format the datetime properly
                formatted_datetime = self._format_datetime(row[2], row[3])
                # Create the record
                self.env['shuttle_onboard_history.model'].create({
                    'onboard_date_time': formatted_datetime,
                    'onboard_date': formatted_datetime.date(),  # Keep original date format if needed
                    'employee_id': employee_id.id,
                    'shuttle_id': shuttles_model.id,
                })
            else:
                pass
                #excell sheet of records which got issues

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Shuttle Schedule Upload Complete',
                'sticky': False,
                'type': 'success',
            }
        }

    # def upload_external_shuttle_schedules(self):
    #     #check if there is a excell sheet uploaded
    #     if not self.excell_sheet:
    #         return
    #
    #     csv_data = base64.b64decode(self.excell_sheet)
    #     csv_file = io.StringIO(csv_data.decode('utf-8'))
    #     reader = csv.reader(csv_file, delimiter=',')
    #     # Skip header if exists
    #     next(reader, None)
    #     for row in reader:
    #         #search if the shuttle exists
    #         shuttles_model=self.env['shuttles.model'].search([('name','ilike',row[0])])
    #         employee_id=self.env['hr.employee'].search([('name','ilike',row[1])])
    #         if shuttles_model and employee_id:
    #             self.env['shuttle_onboard_history.model'].create(
    #                 {
    #                     'onboard_date_time':f'{row[2]}T{row[3]}',
    #                     'onboard_date':row[2],
    #                     'employee_id':employee_id.id,
    #                     'shuttle_id':shuttles_model.id,
    #
    #                 }
    #             )
    #     return


        #search inside employee_schedules if it exists and add an onboard history



