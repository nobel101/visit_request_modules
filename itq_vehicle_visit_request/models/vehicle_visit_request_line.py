from odoo import api, fields, models


class VehicleVisitRequestLine(models.Model):
    _name = 'vehicle.visit.request.line'
    _description = 'Vehicle Visit Request Line'
    _inherit = ['visit.request.abstract.line']

    # Fields
    vehicle_visit_request_id = fields.Many2one('vehicle.visit.request', string='Vehicle Visit Request', ondelete='cascade')
    visit_additional_item_ids = fields.One2many('visit.additional.items', 'vehicle_visit_request_line_id', string='Additional Items')
    driver_type = fields.Selection([('employee', 'Employee'), ('external', 'External')], string='Driver', default='external',required=True)
