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

    @api.model
    def _get_current_history(self, patient):
        today = fields.Date.today()

        return self.search(
            [
                ('patient_id', '=', patient.id),
                ('assignment_date', '<=', today),
                '|',
                ('change_date', '=', False),
                ('change_date', '>', today),
            ],
            order='assignment_date desc, id desc',
            limit=1,
        )

    def _is_current(self):
        self.ensure_one()
        today = fields.Date.today()
        return self.assignment_date <= today and (not self.change_date or self.change_date > today)

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)

        if self.env.context.get('skip_history_sync'):
            return records

        for record in records:
            if not record._is_current():
                continue

            previous = self._get_current_history(record.patient_id)

            if previous and previous != record:
                previous.with_context(skip_history_sync=True).write({
                    'change_date': fields.Date.today(),
                })

            record.patient_id.with_context(skip_history_sync=True).write({
                'doctor_id': record.doctor_id.id,
            })

        return records

    def write(self, vals):
        was_active = {record.id: record._is_current() for record in self}

        res = super().write(vals)

        for record in self:
            is_active = record._is_current()

            if was_active[record.id] and not is_active:
                record.patient_id.with_context(skip_history_sync=True).write({
                    'doctor_id': False,
                })

            elif (not was_active[record.id] and is_active) or (is_active and 'doctor_id' in vals):
                record.patient_id.with_context(skip_history_sync=True).write({
                    'doctor_id': record.doctor_id.id,
                })

        return res

    def unlink(self):
        for record in self:
            if record._is_current():
                record.patient_id.with_context(skip_history_sync=True).write({
                    'doctor_id': False,
                })

        return super().unlink()

    @api.constrains("assignment_date", "change_date")
    def _check_dates(self):
        if self.assignment_date and self.change_date and self.change_date < self.assignment_date:
            raise ValidationError('The date of the change of the doctor cannot be earlier than the date of the assignment.')

    def _compute_display_name(self):
        for record in self:
            patient = record.patient_id.name or ''
            doctor = record.doctor_id.name or ''
            category = record.doctor_id.category_id.name or ''
            date = record.assignment_date or ''

            record.display_name = f'{patient} - {doctor} ({category}) {date}'
