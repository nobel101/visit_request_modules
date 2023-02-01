from odoo import api, fields, models


class VisitAdditionalItems(models.Model):
    _name = 'visit.additional.items'
    _description = 'Visit Additional Items'

    name = fields.Char(string='Name', required=True)
    quantity = fields.Integer(string='Quantity', required=True)
    visit_request_line_id = fields.Many2one('visit.request.concrete.long.line', string='Visit Request Line',invisible=True,readonly=True)