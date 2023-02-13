from odoo import api, fields, models


class VisitAdditionalItems(models.Model):
    _name = 'visit.additional.items'
    _description = 'Visit Additional Items'

    name = fields.Char(string='Name', required=True)
    quantity = fields.Integer(string='Quantity', required=True)
    description = fields.Text(string='Description')