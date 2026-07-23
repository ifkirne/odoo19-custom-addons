# -*- coding: utf-8 -*-
from datetime import date
from odoo.exceptions import ValidationError
from odoo import api, fields, models


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _description = "Hospital Patient"

    # Basic database fields for patient information
    name = fields.Char(string="Patient Name", required=True)
    ref = fields.Integer(string="Reference")
    date_of_birth = fields.Date(string="Date of Birth")
    admission_date = fields.Date(string="Admission Date", default=fields.Date.context_today)
    weight = fields.Float(string="Weight (kg)")
    is_admitted = fields.Boolean(string="Admitted", default=False)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string="Gender",
                              default="male")
    medical_history = fields.Text(string="Medical History")

    # Computed field to dynamically calculate patient age
    age = fields.Integer(string="Age", compute="_compute_age")

    # Tracks the patient's lifecycle state in the hospital
    state = fields.Selection(
        [('draft', 'Draft'), ('admitted', 'Admitted'), ('treatment', 'Under Treatment'), ('discharged', 'Discharged')],
        string='Status', default='draft', tracking=True)

    # UI widget fields for visual representation and contact
    image = fields.Image(string="Patient Photo")
    phone = fields.Char(string="Phone Number")
    email = fields.Char(string="Email Address")
    priority = fields.Selection([('0', 'Normal'), ('1', 'Low'), ('2', 'High'), ('3', 'Emergency')], string="Priority",
                                default='0')

    # Relational field linking the patient to a specific doctor
    doctor_id = fields.Many2one("hospital.doctor", string="Assigned Doctor", ondelete="restrict")

    # Relational field showing all appointments for this patient
    appointment_id = fields.One2many('hospital.appointment', 'patient_id', string="Appointments")

    # Smart button field to count related appointments
    appointment_count = fields.Integer(string="Total Appointments", compute="_compute_appointment_count")

    # Python constraint to prevent admission date before birth date
    @api.constrains('admission_date', 'date_of_birth')
    def _check_admission_date(self):
        for rec in self:
            if rec.admission_date and rec.date_of_birth and rec.admission_date < rec.date_of_birth:
                raise ValidationError("The Admission Date cannot be earlier than the Date of Birth.")

    # Compute logic for calculating the patient's age based on DOB
    @api.depends('date_of_birth')
    def _compute_age(self):
        today = date.today()
        for rec in self:
            rec.age = (today.year - rec.date_of_birth.year) if rec.date_of_birth else 1

    # Compute logic to count the total number of linked appointments
    def _compute_appointment_count(self):
        for rec in self:
            rec.appointment_count = len(rec.appointment_id)

    # Opens the appointment view directly from the patient's smart button
    def action_view_patient_appointments(self):
        return {
            'name': 'Patient Appointments',
            'type': 'ir.actions.act_window',
            'res_model': 'hospital.appointment',
            'view_mode': 'list,form,kanban',
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id},
            'target': 'current',
        }

    # Statusbar transition: Moves patient to 'Admitted' state
    def action_dynamic_update(self):
        for rec in self:
            rec.state = 'admitted'
            rec.is_admitted = True

    # Statusbar transition: Moves patient to 'Under Treatment' state
    def action_start_treatment(self):
        for rec in self:
            rec.state = 'treatment'

    # Statusbar transition: Resets patient to 'Draft' state
    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    # Duplicates the current patient record with a 'Copy' suffix
    def action_dynamic_create_copy(self):
        for rec in self:
            rec.copy(default={'name': f"{rec.name} (Copy)", 'ref': 0, 'is_admitted': False})

    # Deletes the current patient and redirects the user to the list view
    def action_dynamic_delete(self):
        for rec in self:
            rec.unlink()
        return {
            'name': 'Patients',
            'type': 'ir.actions.act_window',
            'res_model': 'hospital.patient',
            'view_mode': 'list,kanban,form',
            'target': 'current',
        }

        # =========================================================
        # ADDED FOR DAY 16: TASK 3 & 5 - PATIENT STATUS UPDATE CRON
        # =========================================================
        @api.model
        def cron_update_long_term_patients(self):
            """
            Task 3: Search for patients admitted more than 30 days ago,
            update their status, and log the action in the Chatter.
            """
            # Calculate the threshold date (30 days ago)
            threshold_date = fields.Date.context_today(self) - timedelta(days=30)

            # Search for patients who are admitted, but skip those who are already 'long_term' or 'discharged'
            eligible_patients = self.search([
                ('state', 'in', ['admitted', 'treatment']),
                ('admission_date', '<=', threshold_date)
            ])

            # Handle empty recordsets gracefully
            if not eligible_patients:
                return

            for patient in eligible_patients:
                # Update their status
                patient.write({
                    'state': 'long_term'
                })

                # Log the updated record in the Chatter
                patient.message_post(
                    body="System Automated Action: Patient status escalated to 'Long-Term Admission' (Admitted > 30 days).",
                    subtype_xmlid="mail.mt_note"  # Logs it as an internal note
                )