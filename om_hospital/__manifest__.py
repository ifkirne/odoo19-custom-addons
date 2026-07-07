{
    'name': 'Hospital Management Test',
    'version': '19.0.1.0.0',
    'category': 'Healthcare',
    'sequence': -100,
    'summary': 'Manage hospital operations, patients, and appointments.',
    'description': """Hospital Management System for Odoo 19.""",
    'author': 'Ilyas Rahman',
    'depends': [
      'sales_team',
      'account_payment',
      'utm',
],
    'data': [
    'views/menu.xml',
],
    'demo': [],

    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}