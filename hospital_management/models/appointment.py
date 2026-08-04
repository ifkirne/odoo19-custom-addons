# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Hospital Appointments'

    _rec_name = 'name'

    # =========================================================
    # FIELDS
    # =========================================================
    name = fields.Char(string='Appointment Number', required=True, copy=False, readonly=True, default='New')
    appointment_date = fields.Date(string='Appointment Date', required=True, default=fields.Date.context_today)
    notes = fields.Text(string='Appointment Notes')

    patient_id = fields.Many2one('hospital.patient', string="Patient", required=True)
    doctor_id = fields.Many2one('hospital.doctor', string="Doctor")
    partner_id = fields.Many2one('res.partner', string="Customer", required=True)
    product_id = fields.Many2one('product.product', string="Service")
    sale_order_id = fields.Many2one('sale.order', string="Quotation")

    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender")
    appointment_time = fields.Datetime(string='Appointment Time', default=fields.Datetime.now)
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

    # =========================================================
    # ACTION METHODS
    # =========================================================
    def action_view_sale_order(self):
        """Opens the linked Sale Order or creates a new one if missing."""
        self.ensure_one()

        # Auto-create quotation if none exists
        if not self.sale_order_id:
            self.action_create_quotation()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Quotation',
            'res_model': 'sale.order',
            'view_mode': 'form',
            'res_id': self.sale_order_id.id,
            'target': 'current',
        }

    def action_create_quotation(self):
        if not self.partner_id:
            raise ValidationError("Please select Customer")

        if not self.product_id:
            raise ValidationError("Please select Service")

        sale_order = self.env['sale.order'].create({
            'partner_id': self.partner_id.id,
            'origin': self.name,
        })

        self.env['sale.order.line'].create({
            'order_id': sale_order.id,
            'product_id': self.product_id.id,
            'product_uom_qty': 1,
            'price_unit': self.product_id.lst_price,
        })

        self.sale_order_id = sale_order.id

        return {
            'type': 'ir.actions.act_window',
            'name': 'Quotation',
            'res_model': 'sale.order',
            'view_mode': 'form',
            'res_id': sale_order.id,
        }

    def action_send_registration_email(self):
        template = self.env.ref('hospital_management.email_template_appointment_registration', raise_if_not_found=False)

        if not template:
            raise UserError("Email template 'email_template_appointment_registration' not found.")

        for rec in self:
            if not rec.patient_id:
                raise UserError("Please select a patient first.")
            if not rec.patient_id.email:
                raise UserError(f"Patient '{rec.patient_id.name}' has no email configured.")

            template.send_mail(
                rec.id,
                force_send=True,
                email_values={'email_to': rec.patient_id.email}
            )

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        for rec in self:
            if rec.patient_id:
                rec.ref = rec.patient_id.ref
                rec.gender = rec.patient_id.gender
            else:
                rec.ref = False
                rec.gender = False