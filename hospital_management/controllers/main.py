# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class HospitalWebsite(http.Controller):

    # ---------------------------------------------------
    # Existing Route from Day 22
    # ---------------------------------------------------
    @http.route('/hospital/doctors', type='http', auth='public', website=True)
    def doctor_list(self, **kwargs):
        doctors = request.env['hospital.doctor'].sudo().search([])
        return request.render('hospital_management.doctor_list_template', {
            'doctors': doctors
        })

    # ---------------------------------------------------
    # Task 3: Route to Show Appointment Form
    # ---------------------------------------------------
    @http.route('/hospital/appointment', type='http', auth='public', website=True)
    def appointment_form(self, **kwargs):
        # Fetch active doctors so we can show them in a dropdown on the form
        doctors = request.env['hospital.doctor'].sudo().search([('active', '=', True)])

        return request.render('hospital_management.appointment_form_template', {
            'doctors': doctors
        })

    # ---------------------------------------------------
    # Task 4, 5 & 6: Route to Handle Form Submission
    # ---------------------------------------------------
    @http.route('/hospital/appointment/submit', type='http', auth='public', website=True, methods=['POST'])
    def submit_appointment(self, **post):
        # 1. Print values to server log for debugging (Task 5)
        print("Received Form Data:", post)

        # 2. Extract the data safely
        patient_name = post.get('patient_name')
        email = post.get('email')
        phone = post.get('phone')
        appointment_date = post.get('appointment_date')
        doctor_id = post.get('doctor_id')

        # 3. Create a new Patient record first (since appointments need a patient_id)
        new_patient = request.env['hospital.patient'].sudo().create({
            'name': patient_name,
            'email': email,
            'phone': phone,
        })

        # 4. Create the Appointment record linked to the new patient and selected doctor
        request.env['hospital.appointment'].sudo().create({
            'patient_id': new_patient.id,
            'doctor_id': int(doctor_id) if doctor_id else False,
            # FIX: Changed 'appointment_date' to match the 'appointment_time' field in your model
            'appointment_time': appointment_date,
        })

        # 5. Redirect user to the success page to prevent duplicate submissions
        return request.redirect('/hospital/appointment/success')

    # ---------------------------------------------------
    # Task 7 & 8: Success Page Route
    # ---------------------------------------------------
    @http.route('/hospital/appointment/success', type='http', auth='public', website=True)
    def appointment_success(self, **kwargs):
        return request.render('hospital_management.appointment_success_template')