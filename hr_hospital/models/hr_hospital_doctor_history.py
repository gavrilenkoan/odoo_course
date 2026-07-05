from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HRHospitalDoctorHistory(models.Model):
    _name = "hospital.doctor.history"
    _description = "Doctor History"

    patient_id = fields.Many2one(
        comodel_name="hospital.patient",
        string="Patient",
        required=True,
    )

    doctor_id = fields.Many2one(
        comodel_name="hospital.doctor",
        string="Doctor",
        required=True,
    )

    assignment_date = fields.Date(
        string="Assignment Date",
        required=True,
        default=fields.Date.today,
    )

    change_date = fields.Date(
        string="Change Date",
    )

    active = fields.Boolean(default=True)

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)

        if self.env.context.get('skip_history_sync'):
            return records

        for record in records:
            if record.change_date:
                continue

            previous = self.search([
                ('patient_id', '=', record.patient_id.id),
                ('id', '!=', record.id),
                ('change_date', '=', False),
            ], limit=1)

            previous.with_context(skip_history_sync=True).write({
                'change_date': fields.Date.today(),
            })
            (record.patient_id.with_context(skip_history_sync=True).write(
                {'doctor_id': record.doctor_id.id}
            ))

        return records

    def write(self, vals):
        was_active = {record.id: not record.change_date for record in self}

        res = super().write(vals)

        for record in self:
            if 'change_date' in vals and was_active[record.id] and record.change_date:
                record.patient_id.with_context(skip_history_sync=True).write({
                    'doctor_id': False,
                })

            elif 'doctor_id' in vals and was_active[record.id]:
                record.patient_id.with_context(skip_history_sync=True).write({
                    'doctor_id': record.doctor_id.id,
                })

        return res

    def unlink(self):
        for record in self:
            if not record.change_date:
                record.patient_id.with_context(skip_history_sync=True).write({
                    'doctor_id': False,
                })

        return super().unlink()

    @api.constrains("assignment_date", "change_date")
    def _onchange_dates(self):
        if self.assignment_date and self.change_date and self.change_date < self.assignment_date:
            raise ValidationError('The date of the change of the doctor cannot be earlier than the date of the assignment.')

    def _compute_display_name(self):
        for record in self:
            patient = record.patient_id.name or ''
            doctor = record.doctor_id.name or ''
            category = record.doctor_id.category_id.name or ''
            date = record.assignment_date or ''

            record.display_name = f'{patient} - {doctor} ({category}) {date}'
