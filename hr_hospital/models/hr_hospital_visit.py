import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)

class HRHospitalVisit(models.Model):
    _name = 'hr.hospital.visit'
    _description = 'Hospital Visit'

    name = fields.Char()
    active = fields.Boolean(default=True)

    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Doctor',
        required=True,
    )

    patient_id = fields.Many2one(
        comodel_name='hr.hospital.patient',
        string='Patient',
        required=True,
    )

    visit_date = fields.Datetime(
        string='Visit Date',
        default=fields.Datetime.now,
    )

    notes = fields.Text()
