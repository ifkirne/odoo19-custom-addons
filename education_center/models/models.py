# from odoo import models, fields, api


# class education_center(models.Model):
#     _name = 'education_center.education_center'
#     _description = 'education_center.education_center'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

