from odoo import http
from odoo.http import request

class MyController(http.Controller):

    @http.route('/some_url', type='http', auth='public')
    def handler(self):
        hospitals = request.env['hospital.management'].sudo().search([])
        data = [{'id': hospital.id, 'name': hospital.name} for hospital in hospitals]
        return {'hospitals': data}

    @http.route('/hospitals', type='http', auth='public', website=True)
    def hospital_list(self):
        hospitals = request.env['hospital.management'].sudo().search([])
        return request.render('Hospital_Management.hospital_template', {'hospitals': hospitals})

