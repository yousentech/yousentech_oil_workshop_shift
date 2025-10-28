from odoo import models, fields, api

class OilWorkOrder(models.Model):
    _inherit = 'oil.work.order'

    shift_id = fields.Many2one('oil.shift', string='Shift', readonly=True)

    @api.model
    def create(self, vals):
        # Link to current open shift for the user if exists
        if not vals.get('shift_id'):
            user_id = vals.get('user_id') or self.env.uid
            open_shift = self.env['oil.shift'].search([('user_id','=',user_id),('state','=','open')], limit=1)
            if open_shift:
                vals['shift_id'] = open_shift.id
        return super().create(vals)
