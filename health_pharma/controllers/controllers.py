# from odoo import http


# class HealthPharma(http.Controller):
#     @http.route('/health_pharma/health_pharma', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/health_pharma/health_pharma/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('health_pharma.listing', {
#             'root': '/health_pharma/health_pharma',
#             'objects': http.request.env['health_pharma.health_pharma'].search([]),
#         })

#     @http.route('/health_pharma/health_pharma/objects/<model("health_pharma.health_pharma"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('health_pharma.object', {
#             'object': obj
#         })

