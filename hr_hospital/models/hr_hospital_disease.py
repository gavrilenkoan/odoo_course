from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HRHospitalDisease(models.Model):
    _name = 'hospital.disease'
    _description = 'Disease'

    _parent_name = "parent_id"
    _parent_store = True

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)

    description = fields.Text()

    parent_id = fields.Many2one(
        comodel_name='hospital.disease',
        string='Parent Disease',
    )

    child_ids = fields.One2many(
        comodel_name='hospital.disease',
        inverse_name='parent_id',
        string='Sub Diseases',
    )

    parent_path = fields.Char(
        index=True,
    )

    @api.constrains('parent_id')
    def _check_parent(self):
        if not self._check_recursion():
            raise ValidationError('Recursive disease hierarchy is not allowed.')

    def _compute_display_name(self):
        for record in self:
            names = []
            current = record

            while current:
                names.append(current.name or '')
                current = current.parent_id

            record.display_name = ' / '.join(reversed(names))
