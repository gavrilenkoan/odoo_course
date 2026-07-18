from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HRHospitalVisit(models.Model):
    _name = 'hospital.visit'
    _description = 'Hospital Visit'

    name = fields.Char(
        required=True,
    )
    active = fields.Boolean(default=True)

    status = fields.Selection(
        [
            ('planned', 'Planned'),
            ('done', 'Completed'),
            ('cancelled', 'Cancelled'),
        ],
        required=True,
        default='planned',
    )

    scheduled_datetime = fields.Datetime(
        string='Scheduled Date',
    )

    visit_datetime = fields.Datetime(
        string='Visit Date',
    )

    summary = fields.Html()

    doctor_id = fields.Many2one(
        comodel_name='hospital.doctor',
        string='Doctor',
        required=True,
    )

    patient_id = fields.Many2one(
        comodel_name='hospital.patient',
        string='Patient',
        required=True,
    )

    disease_id = fields.Many2one(
        comodel_name='hospital.disease',
        string='Disease',
    )

    current_disease_visit_count = fields.Integer(
        compute='_compute_current_disease_visit_count',
    )

    @api.depends('disease_id')
    def _compute_current_disease_visit_count(self):
        visit_model = self.env['hospital.visit']
        for visit in self:
            if visit.disease_id:
                visit.current_disease_visit_count = visit_model.search_count([
                    ('disease_id', '=', visit.disease_id.id)
                ])
            else:
                visit.current_disease_visit_count = 0

    def action_open_current_disease_visits(self):
        self.ensure_one()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Visits',
            'res_model': 'hospital.visit',
            'view_mode': 'list,form',
            'domain': [('disease_id', '=', self.disease_id.id)],
        }

    def action_done(self):
        for visit in self:
            visit.write({
                'status': 'done',
                'visit_datetime': fields.Datetime.now(),
            })

    def action_cancel(self):
        for visit in self:
            visit.status = 'cancelled'

    def write(self, vals):
        protected = {
            "doctor_id",
            "scheduled_datetime",
            "visit_datetime",
        }

        for record in self:
            if record.status == "done":
                if vals.get('active') is False:
                    raise ValidationError('Completed visits cannot be archived.')

                if protected.intersection(vals):
                    raise ValidationError('Completed visits cannot be modified.')

        return super().write(vals)

    def unlink(self):
        for record in self:
            if record.status == "done":
                raise ValidationError('Completed visits cannot be deleted.')
        return super().unlink()
