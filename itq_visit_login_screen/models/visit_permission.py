from odoo import api, fields, models,_
from odoo.exceptions import ValidationError


class VisitPermission(models.Model):
    _inherit = 'visit.permission'

    visit_login_ids = fields.One2many('visit.permission.login', 'visit_permission_id', string='Visit Login',
                                      readonly=True)
    login_state = fields.Selection([('in', 'In'), ('out', 'Out')], string='Login State',)
    login_count = fields.Integer(string='Login Count', compute='_compute_login_count')

    @api.depends('visit_login_ids')
    def _compute_login_count(self):
        for rec in self:
            rec.login_count = len(rec.visit_login_ids)

    def action_permission_logins(self):
        self.ensure_one()
        action = self.env.ref('itq_visit_login_screen.window_action_visit_login').read()[0]
        action['domain'] = [('visit_permission_id', '=', self.id)]
        action['context'] = {'group_by': 'type'}
        return action

    def action_in(self):
        self.ensure_one()
        if self.login_state !=  'in':
            self.login_state = 'in'
            self.env['visit.permission.login'].create({
                'visit_permission_id': self.id,
                'type': 'in',
                'enter_time': fields.Datetime.now()
            })
        else:
            raise ValidationError(_('The visitor already with Inside'))
        return True

    def action_out(self):
        self.ensure_one()
        if self.login_state != 'out':
            self.login_state = 'out'
            self.env['visit.permission.login'].create({
                'visit_permission_id': self.id,
                'type': 'out',
                'exit_time': fields.Datetime.now()
            })
        else:
            raise ValidationError(_('The visitor already with Outside'))
        return True