import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)

class HRHospitalPatient(models.Model):
    _name = 'hr.hospital.patient'
    _description = 'Hospital Patient'

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)

    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Doctor',
    )
