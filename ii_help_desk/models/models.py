# -*- coding: utf-8 -*-

from odoo import models, fields, api, _ 
from datetime import datetime
from random import randint
from odoo.exceptions import UserError
from werkzeug.urls import url_encode


class HDTicket(models.Model):
    _name = 'hd.ticket'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    _description = 'Helpdesk Tickets'
    _rec_name = 'ticket_id'

    READONLY_STATES = {
        'solved': [('readonly', True)],
        'cancel': [('readonly', True)],
    }

    name = fields.Text(states=READONLY_STATES,required=True)
    ticket_id = fields.Char(string='Ticket ID',  copy=False, readonly=True,
                        index=True,)
    @api.model
    def create(self, vals):
        res = super(HDTicket, self).create(vals)
        if not vals.get('ticket_id'):
            if res.team_id:
                team_name = self.env['hd.team'].search([('id','=',res.team_id.id)])
                res.ticket_id=  team_name.name +   self.env['ir.sequence'].next_by_code('hd.ticket') 
                return res

    submit_date = fields.Datetime(default = datetime.now(),readonly=True)
    description = fields.Text(required=True,states=READONLY_STATES)
    team_id = fields.Many2one('hd.team',tracking=True,states=READONLY_STATES,required=True)
    company_id = fields.Many2one('res.company', 'Company', required=True, readonly=True,index=True, states=READONLY_STATES, default=lambda self: self.env.company.id)

    user_id = fields.Many2one('res.users',tracking=True,states=READONLY_STATES,required=True)
    priority = fields.Selection([('low', 'Low'), ('meduim', 'Meduim'), ('high','High')],
                             string="Priority",index=True, help="Priority of tickets",tracking=True,states=READONLY_STATES)
    partner_id = fields.Many2one('res.partner','Customer',tracking=True,states=READONLY_STATES,required=True)
    partner_name = fields.Char(string='Customer Name', compute='_compute_partner_info', store=True, readonly=True)
    partner_email = fields.Char(string='Customer Email', compute='_compute_partner_info', store=True, readonly=True)
    partner_phone = fields.Char(string='Customer Phone', compute='_compute_partner_info', store=True, readonly=True)

    @api.depends('partner_id')
    def _compute_partner_info(self):
        for ticket in self:
            if ticket.partner_id:
                ticket.partner_name = ticket.partner_id.name
                ticket.partner_email = ticket.partner_id.email
                ticket.partner_phone = ticket.partner_id.phone

    tags_id = fields.Many2many('hd.tags', string='Tags',states=READONLY_STATES)
    host_type = fields.Selection([('on_premise', 'on-premise'), ('cloud', 'Cloud')],
                             index=True,tracking=True,required=True,states=READONLY_STATES)
    server_url = fields.Text('Server URL',states=READONLY_STATES)
    resolution_time = fields.Char('Resolution Time',readonly=False,states=READONLY_STATES)


    state = fields.Selection([
        ('new', 'New'),
        ('inprogress', 'In Progress'),
        ('solved','Solved'),
        ('cancel', 'Cancelled')], string='State',
        default='new', required=True)

    def unlink(self):
        for rec in self:
            if rec.state in ['inprogress','solved']:
                raise UserError(
                    _('You are not allow to delete the inprogress or solved tickets.'))
        res = super(HDTicket, self).unlink()
        return res

    def submit(self):
        for rec in self:
            rec.state = 'inprogress'
    def done(self):
        for rec in self:
            rec.state = 'solved'
            create_date = fields.Datetime.from_string(rec.create_date)
            diff_date = fields.Datetime.now() - create_date
            float_days = diff_date.days + float(diff_date.seconds)/ 86400
            days_number = int(float_days)
            rec.resolution_time = days_number
    def cancel(self):
        for rec in self:
            rec.state = 'cancel'   
    def _ticket_notification(self):
        return True    
class HDTeam(models.Model):
    _name = 'hd.team'
    _description = 'Helpdesk Team'

    name = fields.Char()
    max_resolution_time = fields.Integer()

class HDTags(models.Model):
    _name = 'hd.tags'
    _description = 'Helpdesk Tickets Tags'


    name = fields.Char()


    def _get_default_color(self):
        return randint(1, 11)

    color = fields.Integer('Color', default=_get_default_color)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]