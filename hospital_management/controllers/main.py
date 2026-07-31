# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class HospitalWebsite(http.Controller):

    @http.route('/hospital/doctors', type='http', auth='public', website=True)
    def doctor_list(self, **kwargs):
        # Fetch all doctors using sudo() to ensure public users have read access
        doctors = request.env['hospital.doctor'].sudo().search([])

        # Pass the doctors recordset to the QWeb template
        return request.render('hospital_management.doctor_list_template', {
            'doctors': doctors
        })