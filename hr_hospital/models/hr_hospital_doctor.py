import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)

class HRHospitalDoctor(models.Model):
    _name = 'hr.hospital.doctor'
    _description = 'Hospital Doctor'

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)

    specialization = fields.Text()

    patient_ids = fields.One2many(
        comodel_name='hr.hospital.patient',
        inverse_name='doctor_id',
        string='Patients',
    )