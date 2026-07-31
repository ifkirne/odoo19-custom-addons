# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class HospitalDoctor(models.Model):
    _name = "hospital.doctor"
    _description = "Hospital Doctor"
    _rec_name = "doctor_name"
    _order = "doctor_name asc"

    # ADDED FOR DAY 16: Inherit mail modules to enable Chatter and email logging
    # _inherit = ['mail.thread', 'mail.activity.mixin']

    # ---------------------------------------------------------
    # Basic Information
    # ---------------------------------------------------------
    doctor_name = fields.Char(string="Doctor Name", required=True, tracking=True)
    employee_id = fields.Integer(string="Employee ID")
    specialization = fields.Selection([
        ('general', 'General Physician'),
        ('cardiology', 'Cardiology'),
        ('neurology', 'Neurology'),
        ('orthopedic', 'Orthopedic'),
        ('pediatrics', 'Pediatrics'),
    ], string="Specialization", tracking=True)
    phone = fields.Char(string="Phone Number")
    email = fields.Char(string="Email", tracking=True)
    experience = fields.Integer(string="Experience (Years)")
    consultation_fee = fields.Float(string="Consultation Fee", default=1500)
    active = fields.Boolean(string="Active", default=True)
    joining_date = fields.Date(string="Joining Date", default=fields.Date.context_today)

    # ---------------------------------------------------------
    # Widgets & Smart Buttons
    # ---------------------------------------------------------
    image = fields.Image(string="Doctor Photo")
    patient_count = fields.Integer(string="Total Patients", compute="_compute_patient_count")

    # ---------------------------------------------------------
    # RELATIONSHIPS
    # ---------------------------------------------------------
    department_id = fields.Many2one('hospital.department', string="Department", domain="[('active', '=', True)]")
    patient_ids = fields.One2many('hospital.patient', 'doctor_id', string="Patients")

    # ---------------------------------------------------------
    # CONSTRAINTS
    # ---------------------------------------------------------
    _sql_constraints = [
        ('employee_id_unique', 'unique(employee_id)', 'The Doctor Employee ID must be unique!'),
        ('unique_doctor_email', 'unique(email)', 'This email address is already assigned.')
    ]

    @api.constrains('consultation_fee')
    def _check_consultation_fee(self):
        for rec in self:
            if rec.consultation_fee <= 0:
                raise ValidationError("Invalid Fee: The Consultation Fee must be strictly greater than zero.")

    # ---------------------------------------------------------
    # COMPUTE METHODS & ACTIONS
    # ---------------------------------------------------------
    def _compute_patient_count(self):
        for rec in self:
            rec.patient_count = len(rec.patient_ids)

    def action_view_doctor_patients(self):
        return {
            'name': 'Assigned Patients',
            'type': 'ir.actions.act_window',
            'res_model': 'hospital.patient',
            'view_mode': 'list,form',
            'domain': [('doctor_id', '=', self.id)],
            'context': {'default_doctor_id': self.id},
            'target': 'current',
        }

    def action_capitalize_name(self):
        for rec in self:
            if rec.doctor_name:
                rec.write({'doctor_name': rec.doctor_name.upper(), 'experience': rec.experience + 1})

    def unlink(self):
        for rec in self:
            if rec.active:
                raise ValidationError("You cannot delete an active doctor profile. Please archive them first!")
            if rec.patient_ids:
                rec.patient_ids.write({'doctor_id': False})
        return super(HospitalDoctor, self).unlink()

    def action_delete(self):
        return self.unlink()

    # =========================================================
    # ADDED FOR DAY 16: WEEKLY REMINDER CRON METHOD
    # =========================================================
    @api.model
    def cron_weekly_doctor_reminder(self):
        """
        Task 2: Search for active doctors, send them an email reminder,
        and log the execution in the Chatter.
        """
        # 1. Search for active doctors who actually have an email address
        available_doctors = self.search([
            ('active', '=', True),
            ('email', '!=', False)
        ])

        # Handle empty recordset gracefully
        if not available_doctors:
            return

        for doctor in available_doctors:
            # 2. Prepare the email
            mail_values = {
                'subject': 'Weekly Schedule Reminder',
                'body_html': f'<p>Hello Dr. {doctor.doctor_name},</p><p>This is your automated weekly reminder to check your upcoming patient schedule in the clinic system.</p>',
                'email_to': doctor.email,
                # Fallback email if company email isn't configured
                'email_from': self.env.user.company_id.email or 'admin@nerithonx.com',
            }

            # # 3. Send the email using the mail framework
            # mail = self.env['mail.mail'].sudo().create(mail_values)
            # mail.send()
            #
            # # 4. Log the execution in the Chatter
            # doctor.message_post(
            #     body="System Automated Action: Weekly schedule reminder email sent successfully.",
            #     subtype_xmlid="mail.mt_note"
            # )