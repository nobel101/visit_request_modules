from odoo import api, fields, models


class DailyRequestLine(models.Model):
    _name = 'daily.request.line'
    _inherit = ['visit.request.abstract.line']
    _description = 'Daily Request Line Model'

    # Fields
    visit_additional_item_ids = fields.One2many('daily.visit.additional.items', 'daily_visit_request_line_id', string='Additional Items')
    daily_visit_id = fields.Many2one('daily.visit.request', string='Daily Visit Request')