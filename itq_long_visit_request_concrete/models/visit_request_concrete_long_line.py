from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class LongVisitRequestLine(models.Model):
    _name = 'long.visit.request.concrete.line'
    _inherit = ['visit.request.abstract.line']

    long_visit_request_id = fields.Many2one('long.visit.request', string='Visitor Request')
    visit_additional_item_ids = fields.One2many('long.visit.additional.items', 'visit_request_line_id', string='Additional Items')

    def action_line_approve(self):
        for record in self:
            if max(record.long_visit_request_id.visit_request_long_line_ids.mapped('sequence')) == record.sequence\
                    and record.long_visit_request_id.state == 'under_approve' and record.state == 'under_review'\
                    and any(line.state in ['under_review','draft'] for line in record.long_visit_request_id.visit_request_long_line_ids):
                record.long_visit_request_id.action_approve()
                record.state = 'approved'
            else:
                if not any(line.state in ['under_review','draft'] for line in record.long_visit_request_id.visit_request_long_line_ids):
                    record.long_visit_request_id.action_approve()
                    record.write({'state': 'approved'})
                elif record.state == 'under_review':
                    record.write({'state' : 'approved'})
        return super(LongVisitRequestLine, self).action_line_approve()

    def action_line_reject(self):
        for record in self:
            # if max(record.long_visit_request_id.visit_request_long_line_ids.mapped('sequence')) == record.sequence \
            #         and record.long_visit_request_id.state == 'under_approve' and record.state == 'under_review' \
            #         and any(line.state in ['under_review', 'draft'] for line in
            #                 record.long_visit_request_id.visit_request_long_line_ids):
            #     record.state = 'rejected'
            #     record.long_visit_request_id.action_approve()
            #     if record.long_visit_request_id.state in ['under_approve','under_review']:
            #         record.state = 'rejected'
            #     else:
            #         if any(line.state == 'approved' for line in record.long_visit_request_id.visit_request_long_line_ids):
            #             record.long_visit_request_id.action_approve()
            #         record.state = 'rejected'
            # else:
            #     if record.state == 'under_review':
            #         record.state = 'rejected'
            if max(record.long_visit_request_id.visit_request_long_line_ids.mapped('sequence')) == record.sequence \
                    and record.long_visit_request_id.state == 'under_approve' and record.state == 'under_review' \
                    and any(line.state in ['under_review', 'draft'] for line in
                            record.long_visit_request_id.visit_request_long_line_ids):
                record.state = 'rejected'
                record.is_legitimate = False
                record.long_visit_request_id.action_approve_reject()
            elif record.state == 'under_review':
                record.state = 'rejected'
                record.is_legitimate = False
            else:
                continue
        return super(LongVisitRequestLine, self).action_line_reject()

    @api.model
    def create(self, vals):
        if vals.get('long_visit_request_id'):
            vals['sequence'] = self.env['long.visit.request'].browse(vals['long_visit_request_id']).visit_request_long_line_ids[-1].sequence + 1 if self.env['long.visit.request'].browse(vals['long_visit_request_id']).visit_request_long_line_ids else 1
        return super(LongVisitRequestLine, self).create(vals)


