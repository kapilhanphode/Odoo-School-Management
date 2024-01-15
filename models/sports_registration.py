from odoo import api,fields,models,_
from datetime import date
from odoo.exceptions import ValidationError
from dateutil import relativedelta

class SportRegistration(models.Model):
    _name = 'sport.registration'
    _description = 'Sports Registration'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'sport_name'

    sport_name = fields.Char("Sport's Name")

class StudentSportRegistration(models.Model):
    _name = 'student.sport.registration'
    _description = 'Student Sports Registration'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'sport_name'

    stud_name = fields.Many2many('student.registration', string='Student Name', domain="[('fav_sport', '=', sport_name)]")
    sport_name = fields.Many2one('sport.registration',"Sport's Name")


    @api.onchange('sport_name')
    def _onchange_sport_name(self):
        print('uid',self.env.user)
        print('uid1',self.env.uid)

    # @api.onchange('sport_name')
    # def onchange_stud_name(self):
    #     print('hello')
    #     domain = {'stud_name': [('fav_sport', '=', self.sport_name)]}
    #     print('domain',domain)
    #     return {'domain': domain}

# class _inhertpurchase(models.Model):
#     _inherit = 'purchase.order'
#
#     def button_confirm(self):
#         print('clicked confirm button')
#         super(_inhertpurchase, self).button_confirm()

