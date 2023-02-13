from odoo import api, fields, models


class VisitAdditionalItems(models.Model):
    _name = 'long.visit.additional.items'
    _inherit = ['visit.additional.items']
    _description = 'Visit Additional Items'
    visit_request_line_id = fields.Many2one('long.visit.request.concrete.line', string='Visit Request Line',invisible=True,readonly=True)