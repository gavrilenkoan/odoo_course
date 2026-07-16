from odoo import api, fields, models


class HospitalMedicInfo(models.AbstractModel):
    _name = "hospital.medic.info"
    _description = "Medical Information"

    blood_group = fields.Selection(
        selection=[
            ("o_pos", "O(I) Rh+"),
            ("o_neg", "O(I) Rh-"),
            ("a_pos", "A(II) Rh+"),
            ("a_neg", "A(II) Rh-"),
            ("b_pos", "B(III) Rh+"),
            ("b_neg", "B(III) Rh-"),
            ("ab_pos", "AB(IV) Rh+"),
            ("ab_neg", "AB(IV) Rh-"),
        ],
        string="Blood Group",
    )

    gender = fields.Selection(
        selection=[
            ("male", "Male"),
            ("female", "Female"),
        ],
        string="Gender",
    )

    birth_date = fields.Date(
        string="Birth Date",
    )

    age = fields.Integer(
        string="Age",
        compute="_compute_age",
    )

    @api.depends('birth_date')
    def _compute_age(self):
        today = fields.Date.today()

        for record in self:
            if not record.birth_date:
                record.age = 0
                continue

            age = today.year - record.birth_date.year
            if (today.month, today.day) < (
                record.birth_date.month,
                record.birth_date.day,
            ):
                age -= 1

            record.age = age
