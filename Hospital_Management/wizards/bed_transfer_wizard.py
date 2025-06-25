from odoo import models, fields, api

class HospitalBedTransferWizard(models.TransientModel):
    _name = 'hospital.bed.transfer.wizard'
    _description = 'Hospital Bed Transfer Wizard'

    patient_id= fields.Many2one('hospital.management', string="Patient")
    hospitalization_id = fields.Many2one('hospital.patient.hospitalization', string="Hospitalization Record", required=True)
    bed_from = fields.Many2one('hospital.bed', string="Current Bed", readonly=True) 
    bed_to = fields.Many2one('hospital.bed', string="New Bed", required=True, domain="[('id', '!=', bed_from)]")
    reason = fields.Text(string="Reason for Transfer", required=True)

    def action_confirm_transfer(self):
        """Transfers the patient to a new bed and logs the transfer."""
        self.ensure_one()

       
        self.env['hospital.bed.transfer'].create({
            'hospitalization_id': self.hospitalization_id.id,
            'date': fields.Datetime.now(),
            'bed_from': self.bed_from.id,
            'bed_to': self.bed_to.id,
            'reason': self.reason,
        })

        # Update hospitalization record with new bed
        self.hospitalization_id.hospital_bed_id = self.bed_to.id

        return {'type': 'ir.actions.act_window_close'}
