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
        patients = self.env['hospital.patient'].browse(self.env.context.get('active_ids', []))

        for patient in patients:
            if patient.doctor_id == self.doctor_id:
                continue

            current_history = self.env['hospital.doctor.history'].search(
                [
                    ('patient_id', '=', patient.id),
                    ('change_date', '=', False),
                ],
                limit=1,
            )

            if current_history:
                current_history.write({'change_date': self.change_date})

            self.env['hospital.doctor.history'].create(
                {
                    'patient_id': patient.id,
                    'doctor_id': self.doctor_id.id,
                    'assignment_date': self.change_date,
                }
            )

            patient.write({'doctor_id': self.doctor_id.id})

        return {'type': 'ir.actions.act_window_close'}
