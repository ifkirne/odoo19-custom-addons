# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Hospital Appointments'
    _rec_name = 'patient_id'

    # Added the required relation model (assuming 'hospital.patient')
    patient_id = fields.Many2one(
        'hospital.patient',
        string="Patient")
    doctor_id = fields.Many2one('hospital.doctor', string="Doctor")

    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender")
    appointment_time = fields.Datetime(string='Appointment Time', default=fields.Datetime.now)
    # Changed default to fields.Date.context_today since it's a Date field, not Datetime
    booking_date = fields.Date(string='Booking Date', default=fields.Date.context_today)
    ref = fields.Integer(string="Reference")
    active = fields.Boolean(string="Active", default=True)

    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('done', 'Done'),
            ('cancel', 'Cancelled'),
        ],
        string="Status",
        default='draft'
    )

    #Sends registration confirmation email using an email template
    def action_send_registration_email(self):
        template = self.env.ref('hospital_management.email_template_appointment_registration', raise_if_not_found=False)

        if not template:
            raise UserError("Email template 'email_template_appointment_registration' not found.")

        for rec in self:
            if not rec.patient_id:
                raise UserError("Please select a patient first.")
            if not rec.patient_id.email:
                raise UserError(f"Patient '{rec.patient_id.name}' has no email configured.")

            # FIXED: We are now forcing the 'email_to' value directly via Python
            template.send_mail(
                rec.id,
                force_send=True,
                email_values={'email_to': rec.patient_id.email}
            )


    @api.onchange('patient_id')
    def onchange_patient_id(self):
        # We loop through self to ensure safety, a standard Odoo best practice!
        for rec in self:
            if rec.patient_id:
                rec.ref = rec.patient_id.ref
                rec.gender = rec.patient_id.gender
            else:
                # Clear the fields if the user removes the selected patient
                rec.ref = ''
                rec.gender = ''

    #     CRUD OPERATION #####################################

# def action_delete(self):
#     """ DELETE: Dynamically delete the current appointment and return to list """
#     for rec in self:
#         rec.unlink()
#
#     # Redirect the user back to the list view after deleting
#     return {
#         'name': 'Appointments',
#         'type': 'ir.actions.act_window',
#         'res_model': 'hospital.appointment',
#         'view_mode': 'tree,kanban,form',
#         'target': 'current',
#     }
