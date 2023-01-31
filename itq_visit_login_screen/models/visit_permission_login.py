from odoo import api, fields, models


class VisitLogin(models.Model):
    _name = 'visit.permission.login'
    _description = 'Visit Login Screen'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name',related='visit_permission_id.name',readonly=True)
    visit_permission_id = fields.Many2one('visit.permission', string='Visit Permission',required=True)
    type = fields.Selection([('in', 'In'), ('out', 'Out')], string='Type')
    enter_time = fields.Datetime(string='Entering Time')
    exit_time = fields.Datetime(string='Exit Time')


