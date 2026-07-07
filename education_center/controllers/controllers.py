# from odoo import http


# class EducationCenter(http.Controller):
#     @http.route('/education_center/education_center', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/education_center/education_center/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('education_center.listing', {
#             'root': '/education_center/education_center',
#             'objects': http.request.env['education_center.education_center'].search([]),
#         })

#     @http.route('/education_center/education_center/objects/<model("education_center.education_center"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('education_center.object', {
#             'object': obj
#         })

