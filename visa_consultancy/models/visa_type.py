from odoo import models, fields

class VisaType(models.Model):
    _name = 'visa.type'
    _description = 'Visa Type'

    name = fields.Char(string="Visa Type", required=True)
    country_id = fields.Many2one('visa.country', string="Country")
    description = fields.Text(string="Description")
    active = fields.Boolean(default=True)