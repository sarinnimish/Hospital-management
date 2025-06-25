from odoo import models,fields,api

class LabTestInfo(models.Model):

    _name = "lab.result"
    _description = "This model store the created test result"

    date_of_analysis = fields.Datetime(string="Date of Analysis")
    Physician = fields.Many2one('health.center',string="Pathologist Physician")
    test_type = fields.Many2one('lab.test.type',string="Test Type")
    patient_id = fields.Many2one('hospital.management',string="Patient")
    date_requests = fields.Datetime(string="Date requested")
    total_cases_ids = fields.Many2many('patient.total.cases')
    results = fields.Char(string="Results")
    diagnosis = fields.Boolean(string="Diagnosis")
    
    test_id  =fields.Char(string="ID",copy=False, readonly=True, index=True ,default=lambda self: ('New'))
    @api.model
    def create(self, vals):
        if vals.get('test_id',('New'))==('New'):
          vals['test_id']=self.env['ir.sequence'].next_by_code('lab.result') or('New')
        result=super(LabTestInfo, self).create(vals)
        return result

class PatientTotalCases(models.Model):

    _name = "patient.total.cases"
    _description = "This model stores the total cases of patient"

    # sequence= fields.Many2one('lab.result', string="Sequence")
    sequence= fields.Char(string="Sequence",readonly="True")
    case_name = fields.Char(string="Name")
    case_result = fields.Char(string="Result Text")
    normal_range = fields.Char(string="Normal Range")
    units = fields.Integer(string="Units")

    # @api.onchange('sequence')
    # def onchange_sequence(self):
    #     for record in self:
    #         if record. sequence:
    #             record.seq = record.sequence.test_id
    #         else:
    #             record.seq = ''