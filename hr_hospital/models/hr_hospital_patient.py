from odoo import api, fields, models


class HRHospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Hospital Patient'
    _inherit = 'hospital.medic.info'

    name = fields.Char(required=True)
    insurance_policy_number = fields.Char(size=20)
    phone = fields.Char()
    active = fields.Boolean(default=True)

    user_id = fields.Many2one(
        comodel_name='res.users',
        string='System User',
    )

    doctor_id = fields.Many2one(
        comodel_name='hospital.doctor',
        string='Personal Doctor',
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

    visit_count = fields.Integer(
        compute='_compute_visit_count',
    )

    @api.depends('visit_ids')
    def _compute_visit_count(self):
        for patient in self:
            patient.visit_count = len(patient.visit_ids)

    def action_view_visits(self):
        self.ensure_one()
        action_name = self.env._('Visit History')
        return {
            'type': 'ir.actions.act_window',
            'name': action_name,
            'res_model': 'hospital.visit',
            'view_mode': 'list,form',
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id},
        }

    def action_create_visit(self):
        self.ensure_one()
        action_name = self.env._('New Visit')
        return {
            'type': 'ir.actions.act_window',
            'name': action_name,
            'res_model': 'hospital.visit',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_patient_id': self.id,
                'default_doctor_id': self.doctor_id.id,
            },
        }

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

            current_history = history_model._get_current_history(patient)

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
