from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'


    forbidden_country_ids = fields.Many2many('res.country', string='Forbidden Countries',
                                            help='Countries that are not allowed to be selected in the visit request form.',
                                             config_parameter='itq_visit_request_abstract.forbidden_country_ids')

    @api.multi
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param("your_module.forbidden_country_ids", self.forbidden_country_ids.ids)

    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        forbidden_country_ids = self.env['ir.config_parameter'].sudo().get_param("your_module.forbidden_country_ids", default=[])
        res.update(forbidden_country_ids=forbidden_country_ids)
        return res