from odoo import api, fields, models


class VisitAdditionalItems(models.Model):
    _inherit = 'visit.additional.items'

    vehicle_visit_request_line_id = fields.Many2one('vehicle.visit.request.line', string='Vehicle Visit Request Line', ondelete='cascade')