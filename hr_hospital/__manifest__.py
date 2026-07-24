# noinspection PyStatementEffect
{
    'name': 'HR Hospital',
    'summary': 'hr hospital system',
    'author': 'gavrilenko_an',
    'category': 'Human Resources',
    'version': '19.0.1.0.0',

    'depends': [
        'base',
    ],

    'data': [
        'security/ir.model.access.csv',

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

    'images': [
        'static/description/icon.png',
    ],

    'installable': True,
    'auto_install': False,
}
