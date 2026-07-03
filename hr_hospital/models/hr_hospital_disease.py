from odoo import fields, models


class HRHospitalDisease(models.Model):
    _name = 'hospital.disease'
    _description = 'Disease'

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)

    description = fields.Text()
