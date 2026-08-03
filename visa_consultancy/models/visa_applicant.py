from odoo import models, fields

class VisaApplicant(models.Model):
    _name = 'visa.applicant'
    _description = 'Visa Applicant'

    name = fields.Char(string="Full Name", required=True)
    passport_number = fields.Char(string="Passport Number")
    nationality = fields.Char(string="Nationality")
    date_of_birth = fields.Date(string="Date of Birth")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string="Gender")
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    address = fields.Text(string="Address")
    notes = fields.Text(string="Notes")