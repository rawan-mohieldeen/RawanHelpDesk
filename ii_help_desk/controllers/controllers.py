# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from operator import itemgetter

from odoo import http
from odoo.exceptions import AccessError, MissingError, UserError
from odoo.http import request
from odoo.tools.translate import _
from odoo.tools import groupby as groupbyelem
from odoo.addons.portal.controllers.portal import pager as portal_pager, CustomerPortal
from odoo.osv.expression import OR


class CustomerPortal(CustomerPortal):
    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'ticket_count' in counters:
            partner = request.env.user.partner_id
            values['ticket_count'] = request.env['hd.ticket'].search_count([('partner_id','=',partner.id)])

        return values
    def _ticket_get_page_view_values(self, ticket, access_token, **kwargs):
        values = {
            'page_name': 'ticket',
            'ticket': ticket,
        }
        return self._get_page_view_values(project, access_token, values, 'my_projects_history', False, **kwargs)
    @http.route(['/my/tickets'], type='http', auth="user", website=True)
    def portal_my_projects(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        tickets = request.env['hd.ticket'].search([('partner_id','=',partner.id)])
        domain = []

        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'create_date desc'},
            'name': {'label': _('Name'), 'order': 'name'},
        }
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # tickets count
        ticket_count = tickets.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/tickets",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=ticket_count,
            page=page,
            step=self._items_per_page
        )



        values.update({
            'date': date_begin,
            'date_end': date_end,
            'tickets': tickets,
            'page_name': 'project',
            'default_url': '/my/tickets',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby
        })
        return request.render("ii_help_desk.portal_my_tickets", values)
