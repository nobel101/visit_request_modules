from odoo import api, fields, models


class VisitPermission(models.Model):
    _name= 'visit.permission'
    _description = 'Visit Permission'

    name= fields.Char(string='Name',readonly=True)
    visit_request_id = fields.Many2one('visit.request.long', string='Visit Request',readonly=True)
    date_start = fields.Date(string='Start Date',readonly=True)
    date_end = fields.Date(string='End Date',readonly=True)
    visit_duration = fields.Selection([('morning', 'Morning'), ('night', 'Night'), ('both', 'Both')],
                                        string='Visit Duration',readonly=True)
    hr_department_id = fields.Many2one('hr.department', string='Requester Unit',readonly=True)
    user_id = fields.Many2one('res.users', 'Authorized User',readonly=True)
    date_request = fields.Date(string='Request Date',readonly=True)
    request_reason = fields.Text(string='Request Reason',readonly=True)
    visitor_name = fields.Char(string='Visitor Name',readonly=True)
    visitor_id =  fields.Char(string='Visitor ID',readonly=True)
    country_id = fields.Many2one('res.country', string='Country',readonly=True)
    visitor_phone = fields.Char(string='Visitor Phone',readonly=True)
    need_car_authorization = fields.Boolean(string='Need Car Authorization',readonly=True)
    car_type = fields.Char(string='Car Type', readonly=True)
    car_model = fields.Char(string='Car Model', readonly=True)
    car_color = fields.Char(string='Car Color', readonly=True)
    car_sign = fields.Char(string='Car Sign', readonly=True)