from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HRHospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _description = 'Hospital Doctor'
    _inherit = 'hospital.medic.info'

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)

    specialization = fields.Char(required=True)
    category_id = fields.Many2one(
        comodel_name='hospital.doctor.category',
        string='Qualification',
        required=True,
    )

    user_id = fields.Many2one(
        comodel_name='res.users',
        string='System User',
    )

    is_intern = fields.Boolean(
        string='Doctor is Intern',
        compute='_compute_is_intern',
        store=True,
    )

    @api.depends('category_id')
    def _compute_is_intern(self):
        intern = self.env.ref(
            'hr_hospital.doctor_category_intern',
            raise_if_not_found=False,
        )

        for record in self:
            record.is_intern = bool(intern and record.category_id == intern)

    mentor_id = fields.Many2one(
        comodel_name='hospital.doctor',
        string='Mentor',
    )

    @api.onchange('category_id')
    def _onchange_category_id(self):
        if not self.is_intern:
            self.mentor_id = False

    @api.constrains('mentor_id', 'is_intern')
    def _check_mentor(self):
        for record in self:
            if record.mentor_id and record.mentor_id.is_intern:
                raise ValidationError('The selected mentor cannot be an intern.')

            if record.is_intern and not record.mentor_id:
                raise ValidationError('An intern must have a mentor.')

    patient_ids = fields.One2many(
        comodel_name='hospital.patient',
        inverse_name='doctor_id',
        string='Patients',
    )

    visit_ids = fields.One2many(
        comodel_name='hospital.visit',
        inverse_name='doctor_id',
        string='Visits',
    )
