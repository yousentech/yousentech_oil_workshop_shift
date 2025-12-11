from odoo import models, fields, api
from odoo.exceptions import UserError

class OilWorkOrder(models.Model):
    _inherit = 'oil.work.order'

    shift_id = fields.Many2one('oil.shift', string='Shift',)

    def _validate_entries(self):

        res = super()._validate_entries()
        if self.order_date < self.shift_id.start_time:
            raise UserError(_("THe order date is less than from shift start date - تاريخ امر العمل اقل من تاريخ بدء الشفت"))

        return res


    @api.model
    def create(self, vals):
        # Link to current open shift for the user if exists
        if not vals.get('shift_id'):
            user_id = vals.get('user_id') or self.env.uid
            open_shift = self.env['oil.shift'].search([('company_id','=', vals.get('company_id')),('state','=','open')], limit=1)
            if open_shift:
                vals['shift_id'] = open_shift.id
        
            if not open_shift:
                raise UserError('You must open a shift before recording a sale.')

        return super().create(vals)
