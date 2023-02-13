from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class DailyVisitRequest(models.Model):
    _name = 'daily.visit.request'
    _inherit = 'visit.request.abstract'
    _description = 'Daily Visit Request'

    # Fields
    type = fields.Selection([('daily', 'Daily'), ('long', 'Long'), ('trainee', 'Trainee')], string='Visit Type', default='daily',readonly=True)
    permission_count = fields.Integer(string='Permission Count', default=0, readonly=True)
    permission_ids = fields.One2many('visit.permission', 'daily_visit_id', string='Permission', readonly=True)
    daily_request_line_ids = fields.One2many('daily.request.line', 'daily_visit_id', string='Daily Request Line', readonly=True)
    state = fields.Selection([('draft', 'Draft'),('under_approve','Under Approve'), ('approved', 'Approved'), ('approver_rejected', 'Approver Rejected'),('cancel','Cancelled')], string='State', default='draft', readonly=True)
    # methods
    def _compute_permission_count(self):
        for record in self:
            record.permission_count = len(record.permission_ids)

    def action_permission_view(self):
        action = self.env.ref('itq_daily_visit_request.action_visit_daily_permission').read()[0]
        action['domain'] = [('daily_visit_id', '=', self.id), ('type', '=', 'daily')]
        return action

    def generate_permission(self):
        for record in self:
            for line in record.daily_request_line_ids.filtered(lambda l: l.is_legitimate == True):
                record.state = 'approved'
                self.env['visit.permission'].sudo().create({
                    'name': 'Permission Number ' + record.request_number or '' + ' For ' + line.visitor_name or '',
                    'daily_visit_id': record.id,
                    'date_start': record.date_start,
                    'date_end': record.date_end,
                    'visit_duration': record.visit_duration,
                    'hr_department_id': record.hr_department_id.id,
                    'user_id': record.user_id.id,
                    'date_request': record.date_request,
                    'request_reason': record.request_reason,
                    'visitor_name': line.visitor_name,
                    'visitor_id': line.visitor_id_number,
                    'visitor_phone': line.visitor_phone,
                    'country_id': line.country_id.id,
                    'need_car_authorization': line.need_car_authorization,
                    'car_model': line.car_model,
                    'car_sign': line.car_sign,
                    'car_color': line.car_color,
                    'car_type': line.car_type,
                    'type': 'daily',
                })

    @api.model
    def create(self, vals):
        if vals.get('request_number', _('New')) == _('New'):
            vals['request_number'] = self.env['ir.sequence'].next_by_code('daily.visit.request.sequence') or _('New')
        if not vals.get('daily_request_line_ids'):
            raise ValidationError(_('You cannot create a visit request without lines.'))
        result = super(DailyVisitRequest, self).create(vals)
        return result

    def action_send_request(self):
        super(DailyVisitRequest, self).action_send_request()
        for record in self:
            record.state = 'under_approve'
            for line in record.daily_request_line_ids:
                if line.state != 'approved':
                    line.write({'state': 'under_review'})
        return {
            'type': 'ir.actions.act_window',
            'name': _('Under Review Daily Visit Requests'),
            'res_model': 'daily.visit.request',
            'view_mode': 'tree',
            'view_id': self.env.ref('itq_visit_request_abstract.visit_request_abstract_tree_view').id,
            'target': 'main',
            'domain': [('state', '=', 'under_review'),('type','=','daily')],
        }

    def action_approve_reject(self):
        super(DailyVisitRequest, self).action_approve_reject()
        for record in self:
            record.state = 'approver_rejected'
            record.daily_request_line_ids.write({'state': 'rejected'})
        return {
            'type': 'ir.actions.act_window',
            'name': _('Approver Rejected Daily Visit Requests'),
            'res_model': 'daily.visit.request',
            'view_mode': 'tree',
            'view_id': self.env.ref('itq_visit_request_abstract.visit_request_abstract_tree_view').id,
            'target': 'main',
            'domain': [('state', '=', 'under_approve'),('type','=','daily')],
        }
    def action_cancel(self):
        super(DailyVisitRequest, self).action_cancel()
        for record in self:
            record.state = 'cancel'
            record.daily_request_line_ids.write({'state': 'cancel'})
        return {
            'type': 'ir.actions.act_window',
            'name': _('Cancelled Daily Visit Requests'),
            'res_model': 'daily.visit.request',
            'view_mode': 'tree',
            'view_id': self.env.ref('itq_visit_request_abstract.visit_request_abstract_tree_view').id,
            'target': 'main',
            'domain': [('state', '=', 'cancelled'),('type','=','daily')],
        }

    def action_approve(self):
        super(DailyVisitRequest, self).action_approve()
        for record in self:
            record.state = 'approved'
            record.daily_request_line_ids.write({'state': 'approved'})
        return {
            'type': 'ir.actions.act_window',
            'name': _('Approved Daily Visit Requests'),
            'res_model': 'daily.visit.request',
            'view_mode': 'tree',
            'view_id': self.env.ref('itq_visit_request_abstract.visit_request_abstract_tree_view').id,
            'target': 'main',
            'domain': [('state', '=', 'under_approve'),('type','=','daily')],
        }