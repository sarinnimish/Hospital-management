from odoo import models, fields, api
from odoo.exceptions import ValidationError

class PatientHospitalization(models.Model):
    _name = 'hospital.patient.hospitalization'
    _description = 'Patient Hospitalization'
    _rec_name = 'ap_id'
   
    patient_id = fields.Many2one('hospital.management', string="Patient", required=True, ondelete='cascade')
    hospital_bed_id = fields.Many2one('health.center.beds', string="Hospital Bed", required=True, ondelete='restrict')
    hospitalization_date = fields.Datetime(string="Hospitalization Date", default=fields.Datetime.now)
    expected_discharge_date = fields.Datetime(string="Expected Discharge Date")
    attending_physician = fields.Many2one('physician', string="Attending Physician", ondelete='set null')
    operating_physician = fields.Many2one('physician', string="Operating Physician", ondelete='set null')
    admission_type = fields.Selection([('urgent', 'Urgent'), ('normal', 'Normal')], string="Admission Type", required=True)
    reason_for_admission = fields.Many2one('diseases', string="Reason for Admission", ondelete='set null')

    transfer_bed_ids = fields.One2many('hospital.bed.transfer', 'hospitalization_id', string="Bed Transfer History")

    ap_id = fields.Char(string="Registration Code", copy=False, readonly=True, index=True, default=lambda self: ('New'))
    
    @api.model
    def create(self, vals):
        if vals.get('ap_id', ('New')) == ('New'):
            vals['ap_id'] = self.env['ir.sequence'].next_by_code('hospital.patient.hospitalization') or ('New')
        result = super(PatientHospitalization, self).create(vals)
        return result
    
    @api.constrains('hospitalization_date', 'expected_discharge_date')
    def _check_dates(self):
        for record in self:
            if record.expected_discharge_date and record.hospitalization_date and record.expected_discharge_date <= record.hospitalization_date:
                raise ValidationError("The expected discharge date must be after the hospitalization date.")
    
    def action_transfer_bed(self):
        """Open the Bed Transfer Wizard"""
        self.ensure_one()

        return {
            'name': 'Transfer Bed',
            'type': 'ir.actions.act_window',
            'res_model': 'hospital.bed.transfer.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('Hospital_Management.view_hospital_bed_transfer_wizard_form').id,
            'target': 'new',
            'context': {
                'default_hospitalization_id': self.id,
                'default_bed_from': self.hospital_bed_id.id,
            }
        }


class HospitalBed(models.Model):
    _name = 'hospital.bed'
    _description = 'Hospital Bed'
    _rec_name = 'bed'

    bed = fields.Selection([('bed1', 'Bed 1'), ('bed2', 'Bed 2'), ('bed3', 'Bed 3'), ('bed4', 'Bed 4')], string="Bed", required=True)
    ward = fields.Char(string="Ward")


class HospitalBedTransfer(models.Model):
    _name = 'hospital.bed.transfer'
    _description = 'Hospital Bed Transfer'

    hospitalization_id = fields.Many2one('hospital.patient.hospitalization', string="Hospitalization Record", required=True, ondelete='cascade')
    date = fields.Datetime(string="Date", default=fields.Datetime.now)
    bed_from = fields.Many2one('health.center.beds', string="From Bed", readonly=True)
    bed_to = fields.Many2one('health.center.beds', string="To Bed", required=True)
    reason = fields.Text(string="Reason")
