from odoo import models, api, fields, _

class res_config_settings(models.TransientModel):
    _inherit = "res.config.settings"
    
    shift_limit = fields.Selection([('daily','Daily'),
                                        ('unspecified','unspecified')], string="Shift Limit", config_parameter='yousentech_oil_workshop.max_letters',  default='daily'
    )