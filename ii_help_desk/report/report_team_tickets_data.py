# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2012-Today Serpent Consulting Services Pvt. Ltd. (<http://www.serpentcs.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################

from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, models, _
from odoo.exceptions import UserError
from operator import itemgetter
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT




class OldCustomerReport(models.AbstractModel):
    _name = 'report.ii_help_desk.report_team_ticketsdata'
    _description = 'ticket per team report'

    def get_ticket_info(self, team_id,state):
        list1 = []
        tickets = self.env['hd.ticket']
        
        for s in state:
       

            self.env.cr.execute('SELECT t.id '\
                            'FROM hd_ticket as t '\
                            'INNER JOIN hd_team team '\
                            'on team.id = t.team_id '\
                            'where team.id = ' + str(team_id)
                           )
            ticket = self._cr.fetchall()
            ticket = ticket and [x[0] for x in ticket] or []
            dict1 = {}

            for res in self.env['hd.ticket'].browse(ticket).filtered(lambda x:x.state == s):

                                        
                dict1.update({
                    'ticket_id': res.ticket_id,
                    'name': res.name,
                    'time': res.submit_date,
                    'prioraty': res.priority,
                    'resolution_time': res.resolution_time,
                    'state':s,
                    })
                if dict1:
                    list1.append(dict1)
        result = [dict(tupleized) for tupleized in set(
            tuple(item.items()) for item in list1)]
        sorted_lst = sorted(result, key=itemgetter('state'))
        return sorted_lst



    @api.model
    def _get_report_values(self, docids, data=None):
        lang_code = self.env.context.get('lang') or 'en_US'
        lang = self.env['res.lang']
        lang_id = lang._lang_get(lang_code)
        date_format = lang_id.date_format
        strftime_format = (u"%s %s" %
                           (lang_id.date_format, lang_id.time_format))
        if not data.get('form'):
            raise UserError(
                _("Form content is missing, this report cannot be printed."))
        register_ids = self.env.context.get('active_ids', [])
        tickets = self.env['hd.ticket'].browse(register_ids)
        team_id = state = company = False
        if data['form'].get('team_id'):
            team_id = data['form'].get('team_id')[0]
            team_name = data['form'].get('team_id')[1]
        if data['form'].get('state'):
            state = data['form'].get('state')[0]
        else:
            state = ['new','inprogress','solved','cancel']
        if data['form'].get('company'):
            company = self.env['res.company'].browse(
                data['form'].get('company')[0])
        lines_data = self.get_ticket_info(team_id,state)
        return {
            'doc_ids': register_ids,
            'doc_model': 'hd.ticket',
            'docs': tickets,
            'data': data,
            'company':company,
            'lines_data': lines_data,
            'state':state,
            'current_datetime': datetime.now().strftime(strftime_format),
            'current_date': datetime.now().strftime(date_format),
        }
