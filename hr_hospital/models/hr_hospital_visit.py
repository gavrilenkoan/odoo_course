from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HRHospitalVisit(models.Model):
    """Patient visit to a doctor: schedule, status, disease, and summary,
    with completed visits protected from changes."""

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
        """Count all visits sharing this visit's disease into
        ``current_disease_visit_count``."""
        visit_model = self.env['hospital.visit']
        for visit in self:
            if visit.disease_id:
                visit.current_disease_visit_count = visit_model.search_count([
                    ('disease_id', '=', visit.disease_id.id)
                ])
            else:
                visit.current_disease_visit_count = 0

    def action_open_current_disease_visits(self):
        """Open all visits with the same disease as this one.

        :return: an ``ir.actions.act_window`` dict filtered by disease.
        """
        self.ensure_one()
        action_name = self.env._('Visits')
        return {
            'type': 'ir.actions.act_window',
            'name': action_name,
            'res_model': 'hospital.visit',
            'view_mode': 'list,form',
            'domain': [('disease_id', '=', self.disease_id.id)],
        }

    def action_done(self):
        """Mark the visit(s) as completed and stamp the current date/time
        as the visit date."""
        self.ensure_one()
        self.write({
            'status': 'done',
            'visit_datetime': fields.Datetime.now(),
        })

    def action_cancel(self):
        """Set the status of the visit(s) to 'cancelled'."""
        self.ensure_one()
        self.write({'status': 'cancelled'})

    def write(self, vals):
        """Protect completed visits.

        :param vals: values to write.
        :raises ValidationError: when archiving, or changing the doctor,
            schedule, or visit date of a completed visit.
        :return: the result of ``super().write``.
        """
        protected = {
            "doctor_id",
            "scheduled_datetime",
            "visit_datetime",
        }

        for record in self:
            if record.status == "done":
                if vals.get('active') is False:
                    raise ValidationError(self.env._('Completed visits cannot be archived.'))

                if protected.intersection(vals):
                    raise ValidationError(self.env._('Completed visits cannot be modified.'))

        return super().write(vals)

    def unlink(self):
        """Prevent deletion of completed visits.

        :raises ValidationError: if any record has status 'done'.
        :return: the result of ``super().unlink``.
        """
        for record in self:
            if record.status == "done":
                raise ValidationError(self.env._('Completed visits cannot be deleted.'))
        return super().unlink()
