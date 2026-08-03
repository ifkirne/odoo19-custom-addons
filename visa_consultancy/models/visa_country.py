from odoo import models, fields

class VisaCountry(models.Model):
    _name = 'visa.country'
    _description = 'Visa Country'

    name = fields.Char(string="Country Name", required=True)
    code = fields.Char(string="Country Code")
    description = fields.Text(string="Description")
    active = fields.Boolean(default=True)