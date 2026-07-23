from odoo import models, fields


class PatientDischargeWizard(models.TransientModel):
    _name = "patient.discharge.wizard"
    _description = "Patient Discharge Wizard"


    patient_id = fields.Many2one(
        "hospital.patient",
        string="Patient",
        readonly=True
    )


    discharge_date = fields.Date(
        string="Discharge Date",
        default=fields.Date.today
    )


    discharge_note = fields.Text(
        string="Discharge Note"
    )


    def action_discharge(self):
        """Confirm patient discharge"""

        if self.patient_id:
            self.patient_id.write({
                "state": "discharged",
            })

        return {
            "type": "ir.actions.act_window_close",
        }


