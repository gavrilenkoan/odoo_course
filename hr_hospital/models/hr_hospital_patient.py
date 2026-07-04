from odoo import fields, models


class HRHospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Hospital Patient'
    _inherit = 'hospital.medic.info'

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)

    doctor_id = fields.Many2one(
        comodel_name='hospital.doctor',
        string='Personal Doctor',
    )

    insurance_policy_number = fields.Char(
        string='Insurance Policy Number',
        size=20,
    )

    visit_ids = fields.One2many(
        comodel_name='hospital.visit',
        inverse_name='patient_id',
        string='Visits',
    )

    history_ids = fields.One2many(
        comodel_name='hospital.doctor.history',
        inverse_name='patient_id',
        string='Doctor History',
    )
