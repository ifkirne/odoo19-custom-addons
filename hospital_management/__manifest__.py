{
    'name': 'Hospital Management',
    'version': '19.0.1.0.0',
    'category': 'Healthcare',
    'summary': 'Hospital Management System',
    'sequence': -100,

    'description': """
Hospital Management System

Features:
- Patient Management
- Doctor Management
- Appointment Scheduling
- Billing
- Reports
""",

    'author': 'Ilyas Rahman',

    'depends': [
        'base',
        'mail',  # This MUST be here
        'website',
        'portal',
         'sale',
    ],

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',

        # Reports
        'report/patient_report_template.xml',
        'report/report.xml',
        'report/doctor_report_template.xml',
        'report/doctor_report.xml',

        # Views
        'views/patient_view.xml',
        'views/doctor_view.xml',
        'views/department_view.xml',
        'views/appointment_view.xml',

        # Cron job
        'data/cron.xml',
        #Email
        'data/mail_template.xml',
        # website
        'views/website_templates.xml', # Add this line

        # Wizard
        'wizard/patient_discharge_wizard_views.xml',
        # Portal
        'views/portal_templates.xml',
        # Menus
        'views/menu.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
