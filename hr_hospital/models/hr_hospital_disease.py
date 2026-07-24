from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HRHospitalDisease(models.Model):
    """Hierarchical disease classifier (``_parent_store``) with parent and
    sub-diseases and a full-path display name."""

    _name = 'hospital.disease'
    _description = 'Disease'

    _parent_name = "parent_id"
    _parent_store = True

    name = fields.Char(
        required=True,
        translate=True,
    )

    description = fields.Text(translate=True)
    active = fields.Boolean(default=True)

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

    def _compute_display_name(self):
        """Build the display name as the full path from the root,
        e.g. 'Respiratory / Viral / Flu'."""
        for record in self:
            names = []
            current = record

            while current:
                names.append(current.name or '')
                current = current.parent_id

            record.display_name = ' / '.join(reversed(names))

    @api.constrains('parent_id')
    def _check_parent(self):
        """Forbid recursive hierarchies.

        :raises ValidationError: if a disease becomes its own ancestor.
        """
        if self._has_cycle():
            raise ValidationError(self.env._('Recursive disease hierarchy is not allowed.'))
