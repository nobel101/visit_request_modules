from odoo import api, fields, models


class RejectionReason(models.TransientModel):
    _name = 'rejection.reason.wizard'
    _description = 'Rejection Reason'

    reviewer_rejection_reason = fields.Text(string='Reviewer Rejection Reason', required=True)
    approver_rejection_reason = fields.Text(string='Approver Rejection Reason', required=True)

    def action_review_reject(self):
        active_id = self.env.context.get('active_id')
        active_model = self.env.context.get('active_model')
        active_record = self.env[active_model].browse(active_id)
        active_record.reviewer_rejection_reason = self.reviewer_rejection_reason
        active_record.action_review_reject()

    def action_approve_reject(self):
        active_id = self.env.context.get('active_id')
        active_model = self.env.context.get('active_model')
        active_record = self.env[active_model].browse(active_id)
        active_record.approver_rejection_reason = self.approver_rejection_reason
        active_record.action_approve_reject()