from datetime import date

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

    def _compute_display_name(self):
        for record in self:
            patient = record.patient_id.name or ''
            doctor = record.doctor_id.name or ''
            category = record.doctor_id.category_id.name or ''
            date = record.assignment_date or ''

            record.display_name = f'{patient} - {doctor} ({category}) {date}'

    @api.constrains('patient_id', 'assignment_date', 'change_date')
    def _check_dates(self):
        for record in self:
            record._check_date_order()
            record._check_overlapping_history()

    @api.model
    def _get_current_history(self, patient):
        today = fields.Date.today()

        return self.search([
            ('patient_id', '=', patient.id),
            ('assignment_date', '<=', today),
            '|',
            ('change_date', '=', False),
            ('change_date', '>', today),
        ], order='assignment_date desc, id desc', limit=1)

    def _is_current(self):
        self.ensure_one()
        today = fields.Date.today()
        return self.assignment_date <= today and (not self.change_date or self.change_date > today)

    def _check_date_order(self):
        if self.assignment_date and self.change_date and self.change_date < self.assignment_date:
            raise ValidationError('The change date cannot be earlier than the assignment date.')

    def _check_overlapping_history(self):
        self.ensure_one()

        others = self.search([
            ('patient_id', '=', self.patient_id.id),
            ('id', '!=', self.id),
        ])

        for other in others:
            start1 = self.assignment_date
            end1 = self.change_date or date.max

            start2 = other.assignment_date
            end2 = other.change_date or date.max

            if start1 < end2 and start2 < end1:
                raise ValidationError(
                    f'This assignment overlaps the existing assignment '
                    f'from {other.assignment_date} to {other.change_date or "ongoing"} '
                    f'for doctor "{other.doctor_id.name}".'
                )

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

    @api.model
    def cron_sync_current_doctors(self):
        patients = self.env['hospital.patient'].search([])

        for patient in patients:
            current = self._get_current_history(patient)

            doctor = current.doctor_id if current else False

            if patient.doctor_id != doctor:
                patient.with_context(skip_history_sync=True).write({
                    'doctor_id': doctor.id if doctor else False,
                })
