from odoo import fields, models


class MassReassignDoctorWizard(models.TransientModel):
    """Wizard to reassign many patients to a new doctor from a given date,
    updating their assignment history."""

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
        """Reassign all selected patients (``active_ids``) to the chosen
        doctor: close the current history, add a new line, and, when the
        date is not in the future, update the patients' current doctor.

        :return: an action-window-close dict.
        """
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
