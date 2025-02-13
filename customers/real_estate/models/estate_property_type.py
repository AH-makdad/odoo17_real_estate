from odoo import models, fields, api
from odoo.exceptions import UserError


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property type'

    name = fields.Char(string="name", required=True)
    property_ids = fields.One2many('estate.property', 'property_type_id', string='Properties')
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Offers')
    offer_count = fields.Integer(string='Offer Count', compute='count_offers')

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'The property type name must be unique.')
    ]

    @api.depends("offer_ids")
    def count_offers(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
            print("count offers ", len(record.offer_ids))
