from odoo import models,fields

class LabResult(models.TransientModel):
    
    _name = "lab.result.1"
    _description = "Create the lab test result"

    request_id= fields.Many2one("lab.requests", string="Lab Test")

    def confirm(self):
        """Confirm test and mark as Tested"""
        if self.request_id:
            self.request_id.state = 'tested'

        return {
            'name': 'Lab Test Result Info',
            'type': 'ir.actions.act_window',
            'res_model': 'lab.result',
            'view_mode': 'list,form',
        }
    @staticmethod  
    def cancel():
        """This function close the wizard window"""
        return {'type': 'ir.actions.act_window_close'}