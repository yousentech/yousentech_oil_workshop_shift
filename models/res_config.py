from odoo import models, api, fields, _

class res_config_settings(models.TransientModel):
    _inherit = "res.config.settings"
    
    shift_limit = fields.Selection([('daily','Daily'),
                                    ('unspecified','unspecified')],
                                    string="Shift Limit", config_parameter='yousentech_oil_workshop.shift_limit',
                                    default='daily'  )

    
    @api.model
    def get_values(self):
        res = super(res_config_settings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            l_shift_limit = params.get_param('shift_limit', default=False)
           
        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param("shift_limit", self.shift_limit)
       