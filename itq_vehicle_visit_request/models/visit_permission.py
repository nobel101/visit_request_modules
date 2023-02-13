from odoo import api, fields, models


class VisitPermission(models.Model):
    _inherit = 'visit.permission'

    vehicle_visit_id = fields.Many2one('vehicle.visit.request', string='Daily Visit Request')