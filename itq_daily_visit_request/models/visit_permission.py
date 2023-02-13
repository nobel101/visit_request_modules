from odoo import api, fields, models


class VisitPermission(models.Model):
    _inherit = 'visit.permission'

    daily_visit_id = fields.Many2one('daily.visit.request', string='Daily Visit Request')