from odoo import fields, models


class HRHospitalDoctorCategory(models.Model):
    _name = 'hospital.doctor.category'
    _description = 'Doctor Qualification'
    _order = 'sequence, id'

    name = fields.Char(required=True)
    sequence = fields.Integer(default=10)

    doctor_ids = fields.One2many(
        comodel_name='hospital.doctor',
        inverse_name='category_id',
        string='Doctors',
    )

    _unique_name = models.Constraint(
        'UNIQUE(name)',
        'Qualification name must be unique.',
    )
