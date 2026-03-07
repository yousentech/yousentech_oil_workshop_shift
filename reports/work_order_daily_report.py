from datetime import datetime, time
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class wo_report(models.TransientModel):
    _inherit = 'oil.wo.daily.report'

    shift_id = fields.Many2one('oil.shift', string="shift",  )
    
    def get_report(self):
        """Call when button 'Get Report' clicked.
        """
        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'date_start': self.date_start,
                'date_end': self.date_end,
                'partner_id': [(i['id']) for i in self.partner_id],
                'shift_id': [(i['id']) for i in self.shift_id],
                
                'company_id': [(i['id']) for i in self.company_id],
                'sale_man_id': [(i['id']) for i in self.sale_man_id],
                'cancel_state': self.cancel_state,
                'group_by_type': self.group_by_type,
 

            },
        }

       
        return self.env.ref('yousentech_oil_workshop.print_oil_daily_report').report_action(self, data=data)

class ReportAttendanceRecap(models.AbstractModel):
    _name = 'report.yousentech_oil_workshop.oil_daily_report_view'

    @api.model
    def _get_report_values(self, docids, data=None):

        date_start = data['form']['date_start']
        date_end = data['form']['date_end']
        l_partner_id = data['form']['partner_id']
        l_shift_id = data['form']['shift_id']
        l_company_id = data['form']['company_id']
       
        
        l_sale_man_id = data['form']['sale_man_id']
       
        l_group_by_type = data['form']['group_by_type']

        l_cancel_state = data['form']['cancel_state']
 
        domain_compelete = []
        domain_compelete = [('date', '>=', date_start), ('date', '<=', date_end), ('move_type', 'in', ['out_invoice','out_refund']),
                            ('work_order_id', '!=',False)]
      
  

        if l_company_id:
            domain_compelete.append(('company_id', 'in', l_company_id))
           
   

        if l_partner_id:
            domain_compelete.append(('partner_id', 'in', l_partner_id))
            

        if l_cancel_state:
            domain_compelete.append(('state', '!=', 'cancel'))
            domain_compelete.append(('work_order_id.state', '!=', 'cancel_request'))
           

        # if l_report_type == 'posted_invoice':
  
        #     domain_compelete.append(('move_id.state', '=', 'posted'))
        # elif l_report_type == 'posted_draft_invoice':

        #     domain_compelete.append(('move_id.state', 'in', ['draft','posted']))
        # elif l_report_type == 'cancel_invoice':

        #     domain_compelete.append(('move_id.state', 'in', ['cancel']))
      
        # elif l_report_type == 'request_not_invoice':
        #     domain_compelete.append(('move_id.work_order_id', '=', False))

        
        if l_sale_man_id:
            domain_compelete.append(('salesman_id', 'in', l_sale_man_id))
        if l_shift_id:
            domain_compelete.append(('work_order_id.shift_id', 'in', l_shift_id))
      
     
        print(domain_compelete)
        request_compelete = self.env['account.move'].search(domain_compelete)
        print("request_compelete",request_compelete)

        if request_compelete:

            l_shifts = self.env['oil.shift'].search([('id', 'in', request_compelete.work_order_id.shift_id.ids)])
            l_companys = self.env['res.company'].search([('id', 'in', request_compelete.company_id.ids)])
            
            l_partner = self.env['res.partner'].search([('id', 'in', request_compelete.partner_id.ids)])
            l_sale_mans = self.env['salesman'].search([('id', 'in',request_compelete.work_order_id.salesman_id.ids)])
            l_technicians = self.env['hr.employee'].search([('id', 'in',request_compelete.work_order_id.employee_id.ids)])
 
            return {
                'doc_ids': data['ids'],
                'doc_model': data['model'],
                'date_start': date_start,
                'date_end': date_end,
                'companys': l_companys,
                'customers': l_partner,
                'shifts': l_shifts,
                
                'sale_mans': l_sale_mans,
                'technicians': l_technicians,
                'group_by_type': l_group_by_type,
                'docs_compelete': request_compelete,
            }
        else:
            raise ValidationError(
                "لا توجد بيانات")
