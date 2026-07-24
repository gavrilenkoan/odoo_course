from odoo import Command, api, fields, models


class DiseaseReportWizard(models.TransientModel):
    _name = 'disease.report.wizard'
    _description = 'Disease Report Wizard'

    doctor_ids = fields.Many2many(
        comodel_name='hospital.doctor',
        string='Doctors',
    )

    disease_ids = fields.Many2many(
        comodel_name='hospital.disease',
        string='Diseases',
    )

    date_from = fields.Date()
    date_to = fields.Date()

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_model = self.env.context.get('active_model')
        active_ids = self.env.context.get('active_ids', [])
        if active_model == 'hospital.doctor':
            res['doctor_ids'] = [Command.set(active_ids)]
        elif active_model == 'hospital.disease':
            res['disease_ids'] = [Command.set(active_ids)]
        return res

    def action_generate_report(self):
        self.ensure_one()

        domain = []
        if self.doctor_ids:
            domain.append(('doctor_id', 'in', self.doctor_ids.ids))
        if self.disease_ids:
            domain.append(('disease_id', 'child_of', self.disease_ids.ids))
        if self.date_from:
            domain.append(('scheduled_datetime', '>=', self.date_from))
        if self.date_to:
            domain.append(('scheduled_datetime', '<=', self.date_to))

        return {
            'type': 'ir.actions.act_window',
            'name': 'Disease Report',
            'res_model': 'hospital.visit',
            'view_mode': 'list,form',
            'domain': domain,
            'context': {'search_default_group_disease': 1},
        }
