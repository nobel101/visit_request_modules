from odoo import api, fields, models


class VisitPermission(models.Model):
    _inherit = 'visit.permission'

    long_visit_id = fields.Many2one('long.visit.request', string='Long Visit Request')