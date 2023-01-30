from odoo import api, fields, models, _
from odoo.addons.hijri_date_util.models import itq_date_util as Hijri
from odoo.exceptions import ValidationError
from odoo.tools import datetime


class VisitRequestAbstract(models.Model):
    _name = 'visit.request.abstract'
    _description = 'Visit Request Abstract'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'request_number'

    request_number = fields.Char(string='Name', required=True, copy=False, readonly=True, index=True,
                                 default=lambda self: _('New'))
    hr_department_id = fields.Many2one('hr.department', string='Requester Unit', ondelete='cascade', required=True)
    user_id = fields.Many2one('res.users', 'Authorized User', default=lambda self: self.env.user)
    date_request = fields.Date(string='Request Date', default=fields.Date.today())
    request_reason = fields.Text(string='Request Reason', required=True)
    date_start = fields.Date(string='Start Date', required=True)
    date_end = fields.Date(string='End Date', required=True)
    visit_duration = fields.Selection([('morning', 'Morning'), ('night', 'Night'), ('both', 'Both')],
                                      string='Visit Duration', required=True, default='morning')
    state = fields.Selection([('draft', 'Draft'),
                              ('under_review', 'Under Review'),
                              ('under_approve', 'Under Approve'),
                              ('approved', 'Approved'),
                              ('review_rejected', 'Reviewer Rejected'),
                              ('approver_rejected', 'Approver Rejected'),
                              ('returned', 'Returned'),
                              ('cancel', 'Cancelled')],
                             string='Status', default='draft', track_visibility='onchange', readonly=True)
    visibility_flag = fields.Boolean()
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id)
    reviewer_rejection_reason = fields.Text(string='Reviewer Rejection Reason', readonly=True)
    approver_rejection_reason = fields.Text(string='Approver Rejection Reason', readonly=True)

    # the request to be returned in concrete class (long or trainee)
    def action_confirm(self):
        pass

    def action_done(self):
        pass

    def action_cancel(self):
        pass

    def action_send_request(self):
        for record in self:
            record.visibility_flag = True

    def action_return_request(self):
        for record in self:
            record.visibility_flag = False

    def set_draft(self):
        pass

    def action_approve(self):
        pass

    def action_review_reject(self):
        pass

    def action_approve_reject(self):
        pass


    @api.constrains('date_start', 'date_end')
    def _check_date(self):
        for record in self:
            if record.date_start > record.date_end:
                raise ValidationError(_('Start Date must be before End Date'))
            if record.date_start < fields.Date.today():
                raise ValidationError(_('Start Date must be at least today'))
            if record.date_end < fields.Date.today():
                raise ValidationError(_('End Date cannot be in the past'))
            if record.date_end < record.date_start:
                raise ValidationError(_('End Date must be after Start Date'))

    def _get_hijri_date(self, date):
        if date:
            rec_date = datetime.strptime(date, '%Y-%m-%d')
            date = Hijri.create_hij_from_greg(rec_date)
            return str(date.year) + "/" + str(date.month) + "/" + str(date.day)
