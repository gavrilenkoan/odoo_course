from odoo import fields, models


class HRHospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Hospital Patient'
    _inherit = 'hospital.medic.info'

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)

    doctor_id = fields.Many2one(
        comodel_name='hospital.doctor',
        string='Personal Doctor',
    )

    insurance_policy_number = fields.Char(
        string='Insurance Policy Number',
        size=20,
    )

    visit_ids = fields.One2many(
        comodel_name='hospital.visit',
        inverse_name='patient_id',
        string='Visits',
    )

    history_ids = fields.One2many(
        comodel_name='hospital.doctor.history',
        inverse_name='patient_id',
        string='Doctor History',
    )

    def write(self, vals):
        if self.env.context.get('skip_history_sync'):
            return super().write(vals)

        if 'doctor_id' not in vals:
            return super().write(vals)

        history_model = self.env['hospital.doctor.history']
        change_date = fields.Date.today()

        changed_patients = self.env['hospital.patient']

        for patient in self:
            old_doctor = patient.doctor_id
            new_doctor_id = vals.get('doctor_id')

            if old_doctor.id == new_doctor_id:
                continue

            changed_patients |= patient

            current_history = history_model.search([
                ('patient_id', '=', patient.id),
                ('change_date', '=', False),
            ], limit=1)

            if current_history:
                current_history.write({'change_date': change_date})

        result = super().write(vals)

        for patient in changed_patients:
            if patient.doctor_id:
                history_model.with_context(skip_history_sync=True).create({
                    'patient_id': patient.id,
                    'doctor_id': patient.doctor_id.id,
                    'assignment_date': change_date,
                })

        return result
