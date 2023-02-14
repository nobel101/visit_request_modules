from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class VehicleVisitRequest(models.Model):
    _name = 'vehicle.visit.request'
    _description = 'Vehicle Visit Request'
    _inherit = ['visit.request.abstract']


    # Fields
    driver_name = fields.Char(string='Driver Name')
    vehicle_request_line_ids = fields.One2many('vehicle.visit.request.line', 'vehicle_visit_request_id', string='Vehicle Request Lines')
    type = fields.Selection(default='vehicle')
    permission_ids = fields.One2many('visit.permission', 'vehicle_visit_id', string='Permission', readonly=True)
    vehicle_move_type= fields.Selection([('in', 'In'), ('out', 'Out')], string='Vehicle Move Type', default='in',required=True)
    out_reason = fields.Text(string='Out Reason',required=True)
    vehicle_content = fields.Text(string='Vehicle Content', help='Vehicle Content Description when the move type is (in)')
    # Methods
    @api.model
    def create(self, vals):
        if vals.get('request_number', _('New')) == _('New'):
            vals['request_number'] = self.env['ir.sequence'].next_by_code('vehicle.visit.request.sequence') or _('New')
        if not vals.get('visit_request_long_line_ids'):
            raise ValidationError(_('You cannot create a visit request without lines.'))
        result = super(VehicleVisitRequest, self).create(vals)
        return result

    def action_permission_view(self):
        action = self.env.ref('itq_vehicle_visit_request.action_visit_vehicle_permission').read()[0]
        action['domain'] = [('vehicle_visit_id', '=', self.id), ('type', '=', 'vehicle')]
        return action

    def generate_permission(self):
        for record in self:
            for line in record.vehicle_request_line_ids.filtered(lambda l: l.is_legitimate == True):
                record.state = 'approved'
                self.env['visit.permission'].sudo().create({
                    'name': 'Permission Number ' + record.request_number or '' + ' For ' + line.visitor_name or '',
                    'vehicle_visit_id': record.id,
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
                    'type': 'vehicle',
                })

    def action_send_request(self):
        super(VehicleVisitRequest, self).action_send_request()
        for record in self:
            record.state = 'under_approve'
            for line in record.vehicle_request_line_ids:
                if line.state != 'approved':
                    line.write({'state': 'under_review'})
        return {
            'type': 'ir.actions.act_window',
            'name': _('Under Review Vehicle Visit Requests'),
            'res_model': 'vehicle.visit.request',
            'view_mode': 'tree',
            'view_id': self.env.ref('itq_visit_request_abstract.visit_request_abstract_tree_view').id,
            'target': 'main',
            'domain': [('state', '=', 'under_review'),('type','=','vehicle')],
        }

    def action_approve_reject(self):
        super(VehicleVisitRequest, self).action_approve_reject()
        for record in self:
            record.state = 'approver_rejected'
            record.vehicle_request_line_ids.write({'state': 'rejected'})
        return {
            'type': 'ir.actions.act_window',
            'name': _('Approver Rejected Vehicle Visit Requests'),
            'res_model': 'vehicle.visit.request',
            'view_mode': 'tree',
            'view_id': self.env.ref('itq_visit_request_abstract.visit_request_abstract_tree_view').id,
            'target': 'main',
            'domain': [('state', '=', 'under_approve'),('type','=','vehicle')],
        }

    def action_cancel(self):
        super(VehicleVisitRequest, self).action_cancel()
        for record in self:
            record.state = 'cancel'
            record.vehicle_request_line_ids.write({'state': 'cancel'})
        return {
            'type': 'ir.actions.act_window',
            'name': _('Cancelled Vehicle Visit Requests'),
            'res_model': 'vehicle.visit.request',
            'view_mode': 'tree',
            'view_id': self.env.ref('itq_visit_request_abstract.visit_request_abstract_tree_view').id,
            'target': 'main',
            'domain': [('state', '=', 'cancelled'),('type','=','vehicle')],
        }

    def action_approve(self):
        super(VehicleVisitRequest, self).action_approve()
        for record in self:
            record.state = 'approved'
            record.vehicle_request_line_ids.write({'state': 'approved'})
        return {
            'type': 'ir.actions.act_window',
            'name': _('Approved Vehicle Visit Requests'),
            'res_model': 'vehicle.visit.request',
            'view_mode': 'tree',
            'view_id': self.env.ref('itq_visit_request_abstract.visit_request_abstract_tree_view').id,
            'target': 'main',
            'domain': [('state', '=', 'under_approve'),('type','=','vehicle')],
        }

    def action_confirm(self):
        super(VehicleVisitRequest, self).action_confirm()
        for record in self:
            record.state = 'under_review'
            record.vehicle_request_line_ids.write({'state': 'under_review'})
        return {
            'type': 'ir.actions.act_window',
            'name': _('New Vehicle Visit Requests'),
            'res_model': 'vehicle.visit.request',
            'view_mode': 'tree',
            'view_id': self.env.ref('itq_visit_request_abstract.visit_request_abstract_tree_view').id,
            'target': 'main',
            'domain': [('state', '=', 'new'),('type','=','vehicle')],
        }

    def action_review_reject(self):
        super(VehicleVisitRequest, self).action_review_reject()
        for record in self:
            record.state = 'review_rejected'
            record.vehicle_request_line_ids.write({'state': 'rejected'})
            record.vehicle_request_line_ids.write({'is_legitimate': False})
        return {
            'type': 'ir.actions.act_window',
            'name': _('Review Rejected Vehicle Visit Requests'),
            'res_model': 'vehicle.visit.request',
            'view_mode': 'tree',
            'view_id': self.env.ref('itq_visit_request_abstract.visit_request_abstract_tree_view').id,
            'target': 'main',
            'domain': [('state', '=', 'under_review'),('type','=','vehicle')],
        }

    def set_draft(self):
        super(VehicleVisitRequest, self).set_draft()
        for record in self:
            record.state = 'draft'
            record.vehicle_request_line_ids.write({'state': 'draft'})
            record.vehicle_request_line_ids.write({'is_legitimate' : True})
        return {
            'type': 'ir.actions.act_window',
            'name': _('New Vehicle Visit Requests'),
            'res_model': 'vehicle.visit.request',
            'view_mode': 'tree',
            'view_id': self.env.ref('itq_visit_request_abstract.visit_request_abstract_tree_view').id,
            'target': 'main',
            'domain': [('state', '=', 'new'),('type','=','vehicle')],
        }