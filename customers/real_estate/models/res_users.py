from odoo import models, fields


class Res_Users(models.Model):
    _inherit = 'res.users'
    property_ids = fields.One2many('estate.property', 'salesperson_id', string='Properties')
    score = fields.Float(string='Score')
