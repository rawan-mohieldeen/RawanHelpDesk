# -*- coding: utf-8 -*-
##############################################################################
from odoo import api, fields, models, _



class ResPartner(models.Model):
    _inherit = 'res.partner'

    ticket_count = fields.Integer(
        compute="ticket_count", string='Tickets Count')


    def ticket_count(self):
        tickets = self.env['hd.ticket']
        for rec in self:
            rec.ticket_count = 0
            tickets_count_id = tickets.search(
                [('partner_id', '=', rec.id)])
            rec.ticket_count = len(tickets_count_id.ids)

class Users(models.Model):
    _inherit = 'res.users'


    ticket_count = fields.Integer(
        compute="ticket_count", string='Tickets Count')


    def ticket_count(self):
        tickets = self.env['hd.ticket']
        for rec in self:
            rec.ticket_count = 0
            tickets_count_id = tickets.search(
                [('user_id', '=', rec.id)])
            rec.ticket_count = len(tickets_count_id.ids)

    team_id = fields.Many2many('hd.team')