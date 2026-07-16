from odoo import fields, models
from odoo.exceptions import ValidationError


class HRHospitalVisit(models.Model):
    _name = 'hospital.visit'
    _description = 'Hospital Visit'

    name = fields.Char(
        required=True,
    )
    active = fields.Boolean(default=True)

    status = fields.Selection(
        [
            ('planned', 'Planned'),
            ('done', 'Completed'),
            ('cancelled', 'Cancelled'),
        ],
        required=True,
        default='planned',
    )

    scheduled_datetime = fields.Datetime(
        string='Scheduled Date',
    )

    visit_datetime = fields.Datetime(
        string='Visit Date',
    )

    summary = fields.Html()

    doctor_id = fields.Many2one(
        comodel_name='hospital.doctor',
        string='Doctor',
        required=True,
    )

    patient_id = fields.Many2one(
        comodel_name='hospital.patient',
        string='Patient',
        required=True,
    )

    disease_id = fields.Many2one(
        comodel_name='hospital.disease',
        string='Disease',
    )

    def write(self, vals):
        protected = {
            "doctor_id",
            "scheduled_datetime",
            "visit_datetime",
        }

        for record in self:
            if record.status == "done":
                if vals.get('active') is False:
                    raise ValidationError('Completed visits cannot be archived.')

                if protected.intersection(vals):
                    raise ValidationError('Completed visits cannot be modified.')

        return super().write(vals)

    def unlink(self):
        for record in self:
            if record.status == "done":
                raise ValidationError('Completed visits cannot be deleted.')
        return super().unlink()
