from odoo import fields, models, api
import csv
import base64
import io


class UploadOldQrCode(models.TransientModel):
    _name = 'upload_old_qr_code.wizard'

    excell_sheet = fields.Binary()

    def _find_employee_flexible(self, first_name, last_name):
        """Helper method to find employee with flexible name matching"""
        # First try exact match with provided names
        name = f'{first_name} {last_name}'
        hr_employee = self.env['hr.employee'].search([('name', 'ilike', name)])

        if hr_employee:
            return hr_employee

        # If no exact match, search for employees where both first and last names are present
        # This will catch cases with middle names
        domain = [
            '&',
            ('name', 'ilike', first_name),
            ('name', 'ilike', last_name)
        ]
        hr_employee = self.env['hr.employee'].search(domain)

        return hr_employee

    def upload_old_qr_code(self):
        if not self.excell_sheet:
            return

        csv_data = base64.b64decode(self.excell_sheet)
        csv_file = io.StringIO(csv_data.decode('utf-8'))
        reader = csv.reader(csv_file, delimiter=',')

        # Skip header if exists
        next(reader, None)

        # Keep track of matches and mismatches
        updated_employees = []
        not_found_employees = []
        multiple_matches = []

        for row in reader:
            first_name = row[1].strip()
            last_name = row[2].strip()
            qr_code = row[0]

            hr_employee = self._find_employee_flexible(first_name, last_name)

            if hr_employee:
                if len(hr_employee) > 1:
                    # If multiple matches found, log them for review
                    multiple_matches.append({
                        'excel_name': f'{first_name} {last_name}',
                        'matched_names': hr_employee.mapped('name'),
                        'qr_code': qr_code
                    })
                else:
                    # Update the employee record
                    hr_employee.write({
                        'old_qr_code': qr_code
                    })
                    updated_employees.append(hr_employee.name)
            else:
                not_found_employees.append(f'{first_name} {last_name}')

        # Create a summary message
        message = f"""
            Update Summary:
            - Successfully updated {len(updated_employees)} employees
            - Could not find {len(not_found_employees)} employees
            - Found multiple matches for {len(multiple_matches)} employees
        
            Employees not found:
            {', '.join(not_found_employees)}
        
            Multiple matches found:
            {', '.join([f"{m['excel_name']} matched with {', '.join(m['matched_names'])}" for m in multiple_matches])}
            """
        print(message)

    # def upload_old_qr_code(self):
    #     #access the current selected into a loop
    #     if not self.excell_sheet:
    #         return
    #     csv_data = base64.b64decode(self.excell_sheet)
    #     csv_file = io.StringIO(csv_data.decode('utf-8'))
    #     reader = csv.reader(csv_file, delimiter=',')
    #     next(reader, None)
    #     for row in reader:
    #         #search the current row selected into hr
    #         name=f'{row[1]} {row[2]}'
    #         hr_employee = self.env['hr.employee'].search(
    #             [('name', 'ilike', name)])
    #         #if found then update with qrcode
    #         if hr_employee:
    #             hr_employee.write({
    #                 'old_qr_code':row[0]
    #             })
    #         else:
    #             print(name)
    #             print()
            #else print it

