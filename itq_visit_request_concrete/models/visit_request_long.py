from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class VisitRequestLong(models.Model):
    _name = 'visit.request.long'
    _inherit = ['visit.request.abstract']

    visit_request_long_line_ids = fields.One2many('visit.request.concrete.long.line', 'long_visit_request_id')
    visit_permission_ids = fields.One2many('visit.permission', 'visit_request_id', string='Visit Permission')
    permission_count = fields.Integer(compute='_compute_permission_count', string='Permission Count')

    def action_confirm(self):
        res = super(VisitRequestLong, self).action_confirm()
        for record in self:
            if not record.visit_request_long_line_ids:
                raise ValidationError(_('You cannot confirm a visit request without lines.'))
            record.state = 'under_review'
            record.visit_request_long_line_ids.write({'state': 'under_review'})
        return res

    def action_cancel(self):
        res = super(VisitRequestLong, self).action_cancel()
        for record in self:
            record.state = 'cancel'
            record.visit_request_long_line_ids.write({'state': 'cancel'})
        return res

    def action_send_request(self):
        res = super(VisitRequestLong, self).action_send_request()
        for record in self:
            record.state = 'under_approve'
            for line in record.visit_request_long_line_ids:
                if line.state != 'approved':
                    line.write({'state': 'under_review'})
        return res

    def action_return_request(self):
        res = super(VisitRequestLong, self).action_return_request()
        for record in self:
            if record.state == 'under_review':
                record.state = 'draft'
                record.visit_request_long_line_ids.write({'state': 'draft'})
            if record.state == 'under_approve':
                record.state = 'under_review'
                record.visit_request_long_line_ids.write({'state': 'under_review'})
        return res

    def set_draft(self):
        res = super(VisitRequestLong, self).set_draft()
        for record in self:
            record.state = 'draft'
            record.visibility_flag = False
            record.visit_request_long_line_ids.write({'state': 'draft'})
        return res

    def action_approve(self):
        res = super(VisitRequestLong, self).action_approve()
        for record in self:
            for line in record.visit_request_long_line_ids:
                if line.state == 'under_review' and record.state == 'under_approve':
                    self.env['visit.permission'].sudo().create({
                        'name': 'Permission Number ' + record.request_number or ''+ ' For ' + line.visitor_name or '',
                        'visit_request_id': record.id,
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
                        'country_id':line.country_id.id,
                        'need_car_authorization': line.need_car_authorization,
                        'car_model': line.car_model,
                        'car_sign': line.car_sign,
                        'car_color': line.car_color,
                        'car_type': line.car_type,
                    })
                else:
                    continue
            record.state = 'approved'
            record.visit_request_long_line_ids.filtered(lambda rec: rec.state == 'under_review').write({'state': 'approved'})
        return res

    def action_review_reject(self):
        res = super(VisitRequestLong, self).action_review_reject()
        for record in self:
            for line in record.visit_request_long_line_ids:
                if line.state == 'under_review' and record.state == 'under_approve':
                    record.state = 'review_rejected'
                    record.visit_request_long_line_ids.filtered(lambda rec: rec.state == 'under_review').write({'state': 'rejected'})
                else:
                    continue
        return res

    def action_approve_reject(self):
        res = super(VisitRequestLong, self).action_approve_reject()
        for record in self:
            record.state = 'approver_rejected'
            record.visit_request_long_line_ids.write({'state': 'rejected'})
        return res

    @api.model
    def create(self, vals):
        if vals.get('request_number', _('New')) == _('New'):
            vals['request_number'] = self.env['ir.sequence'].next_by_code('visit.request.long.sequence') or _('New')
        if not vals.get('visit_request_long_line_ids'):
            raise ValidationError(_('You cannot create a visit request without lines.'))
        result = super(VisitRequestLong, self).create(vals)
        return result

    def print_invoice_report(self):
        return self.env.ref('itq_visit_request_concrete.long_visit_request_report').report_action(self)


    def _compute_permission_count(self):
        for record in self:
            record.permission_count = len(record.visit_permission_ids)


    def action_permission_view(self):
        action = self.env.ref('itq_visit_request_concrete.action_visit_permission').read()[0]
        action['domain'] = [('visit_request_id', '=', self.id)]
        return action