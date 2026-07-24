from odoo import Command, api, fields, models


class VisitReportWizard(models.TransientModel):
    _name = "visit.report.wizard"
    _description = 'Visit Report Wizard'

    doctor_ids = fields.Many2many("hospital.doctor")

    patient_ids = fields.Many2many("hospital.patient")

    date_from = fields.Date()

    date_to = fields.Date()

    completed_only = fields.Boolean()

    disease_id = fields.Many2one(
        "hospital.disease"
    )

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)

        active_model = self.env.context.get('active_model')
        active_ids = self.env.context.get('active_ids', [])

        if active_model == 'hospital.doctor':
            res['doctor_ids'] = [Command.set(active_ids)]

        elif active_model == 'hospital.patient':
            res['patient_ids'] = [Command.set(active_ids)]

        return res

    def action_generate_report(self):
        self.ensure_one()

        domain = []

        if self.doctor_ids:
            domain.append(('doctor_id', 'in', self.doctor_ids.ids))

        if self.patient_ids:
            domain.append(('patient_id', 'in', self.patient_ids.ids))

        if self.date_from:
            domain.append(('scheduled_datetime', '>=', self.date_from))

        if self.date_to:
            domain.append(('scheduled_datetime', '<=', self.date_to))

        if self.completed_only:
            domain.append(('status', '=', 'done'))

        if self.disease_id:
            domain.append(('disease_id', '=', self.disease_id.id))

        return {
            'type': 'ir.actions.act_window',
            'name': 'Visits',
            'res_model': 'hospital.visit',
            'view_mode': 'list,form',
            'domain': domain,
        }
