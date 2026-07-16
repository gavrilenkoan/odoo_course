from odoo import fields, models


class MassReassignDoctorWizard(models.TransientModel):
    _name = "mass.reassign.doctor.wizard"
    _description = "Mass Reassign Doctor Wizard"

    doctor_id = fields.Many2one(
        "hospital.doctor",
        required=True,
        string="New Doctor",
    )

    change_date = fields.Date(
        default=fields.Date.today,
    )

    def action_reassign(self):
        self.ensure_one()

        patients = self.env['hospital.patient'].browse(self.env.context.get('active_ids', []))

        history_model = self.env['hospital.doctor.history']

        for patient in patients:
            current = history_model._get_current_history(patient)

            if current:
                current.write({
                    'change_date': self.change_date,
                })

            history_model.create({
                'patient_id': patient.id,
                'doctor_id': self.doctor_id.id,
                'assignment_date': self.change_date
            })

            if self.change_date <= fields.Date.today():
                patient.with_context(skip_history_sync=True).write({
                    'doctor_id': self.doctor_id.id,
                })

        return {'type': 'ir.actions.act_window_close'}
