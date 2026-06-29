import logging

from odoo import models, fields

_logger = logging.getLogger(__name__)

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'

    name = fields.Char()

    active = fields.Boolean(default=True)
    description = fields.Text()

    res_partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Main Author',
    )

    res_partner_ids = fields.Many2many(
        comodel_name='res.partner',
        string='Additional Authors',
    )