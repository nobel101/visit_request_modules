from odoo import api, fields, models


class VisitRequestTrainee(models.Model):
    _name = 'visit.request.trainee'
    _inherit = ['visit.request.abstract']

