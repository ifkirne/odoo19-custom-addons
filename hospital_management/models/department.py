# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date


class HospitalDepartment(models.Model):
    _name = 'hospital.department'
    _description = 'Hospital Department'
    # Rec_name tells Odoo to show the department_name in dropdowns/relations
    _rec_name = 'department_name'

    department_name = fields.Selection([
        ('cardiology', 'Cardiology'),
        ('neurology', 'Neurology'),
        ('orthopedic', 'Orthopedic'),
        ('pediatrics', 'Pediatrics'),
    ], string="Department", required=True)  # Added required for safety

    department_code = fields.Char(string="Department Code", required=True)
    floor_number = fields.Integer(string="Floor Number")  # Integer is better for floors
    contact_number = fields.Char(string="Contact Number")
    email = fields.Char(string="Email Address")
    description = fields.Text(string="Description")  # Text gives a larger input box than Char
    active = fields.Boolean(string="Active Status", default=True)
    establishment_date = fields.Date(string="Establishment Date")

    # Task 3: One2many relationship pointing to the doctor model
    doctor_ids = fields.One2many(
        comodel_name="hospital.doctor",
        inverse_name="department_id",
        string="Doctors"
    )

    # =========================================================
    # TASK 11: Smart Button Fields & Methods
    # =========================================================
    doctor_count = fields.Integer(string="Total Doctors", compute="_compute_doctor_count")

    def _compute_doctor_count(self):
        """ Computes the total number of doctors in this department """
        for rec in self:
            rec.doctor_count = len(rec.doctor_ids)

    def action_view_department_doctors(self):
        """ Action triggered by the Smart Button to open related doctors """
        return {
            'name': 'Department Doctors',
            'type': 'ir.actions.act_window',
            'res_model': 'hospital.doctor',
            'view_mode': 'list,form',
            'domain': [('department_id', '=', self.id)],
            'context': {'default_department_id': self.id},
            'target': 'current',
        }

    # =========================================================
    # SQL CONSTRAINTS
    # =========================================================
    _sql_constraints = [
        ('unique_department_code', 'unique(department_code)',
         'The Department Code must be unique. Please choose another code!')
    ]

    # =========================================================
    # PYTHON CONSTRAINTS
    # =========================================================
    @api.constrains('floor_number')
    def _check_floor_number(self):
        """ Prevents negative floor numbers. """
        for rec in self:
            if rec.floor_number < 0:
                raise ValidationError("Invalid Entry: Floor number cannot be negative.")

    @api.constrains('establishment_date')
    def _check_establishment_date(self):
        """ Prevents future dates for establishment. """
        for rec in self:
            if rec.establishment_date and rec.establishment_date > date.today():
                raise ValidationError("Time Travel Error: Establishment date cannot be in the future.")

    # =========================================================
    # DYNAMIC CRUD OPERATIONS
    # =========================================================
    def action_duplicate_department(self):
        """ CREATE: Dynamically duplicate the current department """
        for rec in self:
            rec.copy(default={
                'department_code': f"{rec.department_code} (Copy)"
            })

    def action_archive_department(self):
        """ UPDATE: Dynamically set active to False """
        for rec in self:
            rec.active = False

    def unlink(self):
        """ DELETE: Override default delete to protect data integrity """
        for rec in self:
            if rec.active:
                raise ValidationError("You cannot delete an active department. Please archive it first!")
            if rec.doctor_ids:
                raise ValidationError("You cannot delete a department that has doctors assigned to it.")

        return super(HospitalDepartment, self).unlink()