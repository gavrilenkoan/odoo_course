from odoo import fields, models


class HRHospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _description = 'Hospital Doctor'

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)

    specialization = fields.Text()
    category_id = fields.Many2one(
        comodel_name='hospital.doctor.category',
        string='Qualification',
    )

    patient_ids = fields.One2many(
        comodel_name='hospital.patient',
        inverse_name='doctor_id',
        string='Patients',
    )

    visit_ids = fields.One2many(
        comodel_name='hospital.visit',
        inverse_name='doctor_id',
        string='Visits',
    )
