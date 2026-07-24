{
    'name': 'HR Hospital',
    'version': '19.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'Manage doctors, patients, visits, diseases and medical history',
    'author': 'gavrilenko_an',
    'website': 'https://github.com/gavrilenkoan/odoo_course',
    'license': 'LGPL-3',
    'application': True,

    'images': [
        'static/description/banner.png',
        'static/description/icon.png',
    ],

    'assets': {
        'web.report_assets_common': [
            'hr_hospital/static/src/scss/hr_hospital_report.scss',
        ],
    },

    'depends': [
        'base',
        'web',
    ],

    'data': [
        'security/hr_hospital_groups.xml',
        'security/ir.model.access.csv',
        'security/hr_hospital_security.xml',

        'wizard/hr_hospital_mass_reassign_doctor_wizard_views.xml',
        'wizard/hr_hospital_visit_report_wizard_views.xml',
        'wizard/hr_hospital_disease_report_wizard_views.xml',

        'views/hr_hospital_menu.xml',
        'views/hr_hospital_doctor_views.xml',
        'views/hr_hospital_patient_views.xml',
        'views/hr_hospital_disease_views.xml',
        'views/hr_hospital_visit_views.xml',
        'views/hr_hospital_doctor_category_views.xml',
        'views/hr_hospital_doctor_history_views.xml',

        'report/hr_hospital_doctor_reports.xml',
        'report/hr_hospital_doctor_report_templates.xml',

        'data/hr_hospital_disease_data.xml',
        'data/hr_hospital_doctor_category_data.xml',

        'data/hr_hospital_cron.xml',
    ],

    'demo': [
        'demo/hr_hospital_doctor_demo.xml',
        'demo/hr_hospital_patient_demo.xml',
        'demo/hr_hospital_visit_demo.xml',
        'demo/hr_hospital_doctor_history_demo.xml',
    ],

    'installable': True,
    'auto_install': False,
}
