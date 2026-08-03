{
    'name': 'Visa Consultancy Management',

    'version': '19.0.1.0.0',

    'category': 'Services',
    'sequence': -10,

    'summary': 'Manage visa applications, applicants, documents and payments',

    'description': """
        Visa Consultancy Management System

        Features:
        - Applicant Management
        - Visa Applications
        - Document Tracking
        - Payment Management
        - Appointment Management
    """,

    'author': 'Ilyas Rahman',

    'depends': [
        'base',
        'mail',
        'contacts',
        'account',
    ],

    'data': [

        'security/security.xml',
        'security/ir.model.access.csv',

        'views/applicant_views.xml',
        'views/country_views.xml',
        'views/visa_type_views.xml',
        'views/menu_views.xml',


    ],

    'installable': True,

    'application': True,

    'license': 'LGPL-3',
}