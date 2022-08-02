# -*- coding: utf-8 -*-
##############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import xlsxwriter
import base64
import datetime
from datetime import *
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import UserError


class ticketperteam(models.TransientModel):
    _name = 'ticket.team.report'
    _description = 'Tickets Per Team Wizard'

    team_id = fields.Many2one('hd.team', required=True)
    state = fields.Selection([
        ('new', 'New'),
        ('inprogress', 'In Progress'),
        ('solved','Solved'),
        ('cancel', 'Cancelled')], string='State',
        )
    company = fields.Many2one(
        'res.company', default=lambda self: self.env[
            'res.company']._company_default_get(), string="Company")
    def print_report(self):
        data = self.read()[0]
        res = {'ids': [],
               'model': 'hd.ticket',
               'form': data
               }
        return self.env.ref('ii_help_desk.report_team_tickets_data').report_action([], data=res)
# excel report

    document = fields.Binary('Documents')
    file = fields.Char('Report File Name', readonly=1)

    def print_data_excel(self):
            
        for rec in self:
            state = ['new','inprogress','solved','cancel']
            file_path = 'Tickets Per Team Report' + '.xlsx'
            workbook = xlsxwriter.Workbook('/tmp/' + file_path)
            float_format = workbook.add_format({'num_format': '#,##0.00'})
            file_name = _('Lenses Report.xlsx')
            ormat = workbook.add_format()
            title = workbook.add_format({'bold': True, 'border': 1})
            title.set_align('center')
            title_format = workbook.add_format({'bold': True, 'bg_color': 'D9D9D9', 'border': 1})
            title_format.set_align('center')
            format1 = workbook.add_format()
            for s in state:
                    tickets_id = self.env['hd.ticket'].search([('state','=',s),('team_id','=',rec.team_id.id)])
                    if tickets_id:
                        worksheet = workbook.add_worksheet(s)
                        worksheet.set_column(0, 10, 12)
                        col = 0
                        row = 2
                        worksheet.merge_range('B2:D2', 'Tickets Per Team Report',)
                        row += 1
                        worksheet.merge_range('B3:D3', rec.team_id.name,)
                        row = 4
                        # Header
                        worksheet.write(row, col, 'Ticket ID.',title_format)
                        col += 1
                        worksheet.write(row, col,'Name',title_format)
                        col += 1
                        worksheet.write(row, col, 'Time Submitted',title_format)
                        col += 1
                        worksheet.write(row, col,'Priority',title_format)
                        col += 1
                        worksheet.write(row, col, 'Resolution Time',title_format)

                    
                    
                        col = 0
                        row += 1
                        for t in tickets_id:
                            worksheet.write(row, col, t.ticket_id, format1)
                            col+= 1
                            worksheet.write(row, col, t.name, format1)
                            col += 1
                            worksheet.write(row, col, t.submit_date, format1)
                            col+= 1
                            worksheet.write(row, col, t.priority, format1)
                            col += 1
                            worksheet.write(row, col, t.resolution_time, format1)
                            row += 1
                            col = 0
                        worksheet.set_landscape()

            workbook.close()
            buf = base64.b64encode(open('/tmp/' + file_path, 'rb+').read())
            rec.document = buf
            rec.file = 'Tickets Per Team Report' + '' + '.xlsx'
            return {
                    'res_id': rec.id,
                    'name': 'Files to Download',
                    'view_type': 'form',
                    "view_mode": 'form',
                    'res_model': 'ticket.team.report',
                    'type': 'ir.actions.act_window',
                    'target': 'new',
                }

