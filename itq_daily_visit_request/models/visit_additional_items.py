from odoo import api, fields, models


class VisitAdditionalItems(models.Model):
    _name = 'daily.visit.additional.items'
    _inherit = ['visit.additional.items']
    _description = 'Visit Additional Items'
    daily_visit_request_line_id = fields.Many2one('daily.request.line', string='Visit Request Line',invisible=True,readonly=True)