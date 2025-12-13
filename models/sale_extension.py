from odoo import models, fields, api
from odoo.exceptions import UserError

class OilWorkOrder(models.Model):
    _inherit = 'oil.work.order'

    shift_id = fields.Many2one('oil.shift', string='Shift',)

    shift_limit_type = fields.Char(
        default=lambda self: self._default_shift_limit_type(),
        compute="_check_shift_limit_type",
    )
    def _default_shift_limit_type(self):

        params = self.env['ir.config_parameter'].sudo()
        shift_limit_flag = params.get_param('shift_limit',
                                             default=False)
        
        return shift_limit_flag


 

    def _check_shift_limit_type(self):

        params = self.env['ir.config_parameter'].sudo()
        shift_limit_flag = params.get_param('shift_limit',
                                            default=False)
        for rec in self:
            rec.shift_limit_type = shift_limit_flag
        
    def _validate_entries(self):

        res = super()._validate_entries()
        if self.shift_id.start_time:
            if self.order_date.date() < self.shift_id.start_time.date():
                raise UserError(_("THe order date is less than from shift start date - تاريخ امر العمل اقل من تاريخ بدء الشفت"))
           
            if self.shift_limit_type == 'daily':

                if  fields.Date.today().date() != self.shift_id.start_time.date():
                    raise UserError('You must Close opened shift and open new shift before recording a sale.')

                if self.order_date.date() != self.shift_id.start_time.date():
                    raise UserError('Warning .. The work order date does not match the open shift date.')
                
                 

        return res

    allow_change_shfit_num = fields.Boolean(
        compute="_compute_allow_change_shfit_num",
        default=lambda self: self.default_allow_change_shfit_num(),)
    
    @api.depends("company_id")
    def _compute_allow_change_shfit_num(self):
        for rec in self:
            rec.allow_change_shfit_num = self.user_has_groups("yousentech_oil_workshop_shift.group_allow_modify_shift_in_wo")
   
    @api.model
    def default_allow_change_shfit_num(self):
        return self.user_has_groups("yousentech_oil_workshop_shift.group_allow_modify_shift_in_wo")
 

    @api.model
    def create(self, vals):
        # Link to current open shift for the user if exists
        if not vals.get('shift_id'):
            user_id = vals.get('user_id') or self.env.uid
            open_shift = self.env['oil.shift'].search([('company_id','=', vals.get('company_id')),('state','=','open')], limit=1)
            if open_shift:
                if self.shift_limit_type == 'daily':
                    if self.order_date.date() == open_shift.start_time.date() and fields.Date.today() == open_shift.start_time.date():
                        vals['shift_id'] = open_shift.id
                    else:
                        raise UserError('You must Close opened shift and open new shift before recording a sale.')
                else:
                    vals['shift_id'] = open_shift.id
        
                 
            if not open_shift:
                raise UserError('You must open a shift before recording a sale.')

        return super().create(vals)
    
