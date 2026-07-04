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

        patients.write(
            {
                'doctor_id': self.doctor_id.id,
            }
        )

        return {'type': 'ir.actions.act_window_close'}
