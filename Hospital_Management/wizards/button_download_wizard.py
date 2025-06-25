from odoo import http
from odoo.http import request
import base64
import io
from odoo.tools.misc import xlsxwriter


class ExcelDownloadController(http.Controller):

    @http.route('/download/hospital_excel', type='http', auth='user')
    def download_excel(self, **kwargs):
      
        patients = request.env['hospital.management'].sudo().search([])

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('Hospital Data')

       
        header_format = workbook.add_format({'bold': True, 'align': 'center', 'font_size': 12})
        headers = ['Name', 'Date of Birth', 'Marital Status', 'Gender', 'Address', 'Currency']
        for col, header in enumerate(headers):
            sheet.write(0, col, header, header_format)

    
        row = 1
        for patient in patients:
            sheet.write(row, 0, patient.name or '')
            sheet.write(row, 1, str(patient.Date_of_Birth) if patient.Date_of_Birth else '')
            sheet.write(row, 2, patient.Marital_Status or '')
            sheet.write(row, 3, patient.gender or '')
            sheet.write(row, 4, patient.Address or '')
            sheet.write(row, 5, patient.currency_id.name or '')
            row += 1

        workbook.close()
        output.seek(0)

        return request.make_response(
            output.read(),
            headers=[
                ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition', 'attachment; filename="hospital_report.xlsx"')
            ]
        )

    