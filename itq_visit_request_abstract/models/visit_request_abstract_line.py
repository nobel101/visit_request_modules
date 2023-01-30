from odoo import api, fields, models


class VisitRequestAbstract(models.Model):
    _name = 'visit.request.abstract.line'
    _description = 'Visit Request Abstract Line'
    _rec_name = 'visitor_name'

    def _get_forbidden_country_ids(self):
        country_ids = self.env['ir.config_parameter'].sudo().get_param('forbidden_country_ids')
        return [('id','not in',country_ids)]
    sequence = fields.Integer(string='Sequence',default=10)
    visitor_name = fields.Char(string='Visitor Name', required=True)
    visitor_id_number = fields.Char(string='Visitor ID Number', required=True)
    country_id = fields.Many2one('res.country', string='Visitor Nationality', required=True,domain=_get_forbidden_country_ids)
    visitor_phone = fields.Char(string='Visitor Phone', required=True)
    need_car_authorization = fields.Boolean(string='Need Car Authorization',default=True)
    car_type = fields.Char(string='Car Type')
    car_model = fields.Char(string='Car Model')
    car_color = fields.Char(string='Car Color')
    car_sign = fields.Char(string='Car Sign')
    state = fields.Selection([('draft','Draft'),
                              ('under_review', 'Under Review'),
                              ('rejected','Rejected'),
                              ('approved', 'Approved'),
                              ('cancel', 'Cancelled')],
                             readonly=True,
                             default='draft'
                             )

    def action_line_approve(self):
        pass

    def action_line_reject(self):
        pass

    @api.onchange('need_car_authorization')
    def _onchange_need_car_authorization(self):
        if not self.need_car_authorization:
            self.car_type = False
            self.car_model = False
            self.car_color = False
            self.car_sign = False