from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    # Chapter 11
    # List Order
    _order = "price desc"
    price = fields.Float(string='Price', required=True)
    status = fields.Selection(string='Status', selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    property_type_id = fields.Many2one('estate.property.type', string='Property',
                                       related='property_id.property_type_id', required=True)
    validity = fields.Integer(string='Validity', default=7)
    create_date = fields.Date(string='Create Date', default=fields.Date.context_today)
    date_deadline = fields.Date(string='Deadline Date', compute='_compute_date_deadline',
                                inverse='_inverse_date_deadline')
    _sql_constraints = [('check_price', 'CHECK(price > 10000)', 'The offer price must be big than 10000.')]

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date and offer.validity:
                offer.date_deadline = offer.create_date + timedelta(days=offer.validity)
            else:
                offer.date_deadline = False

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.date_deadline and offer.create_date:
                offer.validity = (offer.date_deadline - offer.create_date).days

    def offer_accepted(self):
        for record in self:
            if record.status == 'accepted':
                raise UserError("it is already accepted")
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id

    def offer_refused(self):
        for record in self:
            if record.status == 'refused':
                raise UserError("it is already refused")
            record.status = "refused"

    @api.model
    def create(self, vals):
        property_id = vals.get('property_id')
        if property_id:
            property = self.env['estate.property'].browse(property_id)
            if property.state != 'new':
                property.state = 'offer_received'
            if vals.get('price') < property.expected_price * 0.5:
                raise ValidationError('The offer price cannot be lower than 50% of expected price .')
        return super(EstatePropertyOffer, self).create(vals)
