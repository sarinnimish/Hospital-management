from odoo import models, fields, api

class AppointmentEvaluation(models.TransientModel):
    _name = "appointment.evaluation"
    _description = "This model stores the appointment evaluation data per doctor"

    name_of_physician = fields.Many2many('appoinments.management', string="Name of Physician", domain=lambda self: self._get_physician_domain())
    speciality = fields.Many2one('appoinments.management', string="Speciality", domain=lambda self: self._get_speciality_domain())
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")

    @api.model
    def _get_physician_domain(self):
        """Fetch all unique physician names from appointment records."""
        physicians = self.env['appoinments.management'].search([]).mapped('physician')
        return [('physician', 'in', list(set(physicians)))]

    @api.model
    def _get_speciality_domain(self):
        """Fetch all unique specialities from appointment records."""
        specialities = self.env['appoinments.management'].search([]).mapped('speciality')
        return [('speciality', 'in', list(set(specialities)))]

    def show(self):
        """Filters appointments based on the provided field values and opens the filtered list"""
        domain = []

        if self.name_of_physician:
            physician_names = self.name_of_physician.mapped('physician')
            domain.append(('physician', 'in', physician_names))

        if self.speciality:
            domain.append(('speciality', '=', self.speciality.id))

        if self.start_date:
            domain.append(('Appoinment_Date', '>=', self.start_date))

        if self.end_date:
            domain.append(('Appoinment_End', '<=', self.end_date))

        return {
            'type': 'ir.actions.act_window',
            'name': 'Filtered Appointments',
            'res_model': 'appoinments.management',
            'view_mode': 'tree,form',
            'domain': domain,
            'target': 'current',
        }

    def cancel(self):
        """Closes the wizard window"""
        return {'type': 'ir.actions.act_window_close'}