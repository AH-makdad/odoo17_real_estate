# from odoo import models, models
from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo.tools import float_is_zero, float_compare


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'
    _order = 'id desc'  # Order by descending ID
    name = fields.Char(string='Name', required=True)
    username = fields.Char(string='username')
    postcode = fields.Integer(string="postcode")
    selling_price = fields.Float(string='Selling Price', readonly=True)
    active = fields.Boolean(string='Active', default=True)
    state = fields.Selection(
        string='State',
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled')
        ], default='new'
    )
    expected_price = fields.Float(string='Expected Price', required=True)
    available_date = fields.Date(string='Available From')
    # description variables
    bedrooms = fields.Integer(string="Bedrooms")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage", default=False)
    # using Many2one
    partner_id = fields.Many2one('res.partner', string='Partner')
    property_type_id = fields.Many2one('estate.property.type', string='Property Type', required=True)
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    salesperson_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    # using Many2many
    tag_ids = fields.Many2many('estate.property.tag', string='Property Tag')
    # using one2many
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    living_area = fields.Float(string='Living Area')
    garden_area = fields.Float(string='Garden Area')
    total_area = fields.Float(string='Total Area', compute='_compute_total_area')
    proprety_type_name = fields.Char(related="property_type_id.name")
    total = fields.Float(compute="_compute_total", inverse="_inverse_total")
    amount = fields.Float()
    gardenP = fields.Boolean(string='Garden')
    area = fields.Float(string='Garden Area')
    orientationP = fields.Char(string='Garden Orientation')
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)', 'The expected price must be strictly positive.'),
        ('check_selling_price', 'CHECK(selling_price >= 0)', 'The selling price must be positive.')
    ]

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("amount")
    def _compute_total(self):
        for record in self:
            record.total = 2.0 * record.amount

    def _inverse_total(self):
        for record in self:
            record.amount = record.total / 2.0

    @api.onchange("gardenP")
    def _onchange_partner_id(self):
        if self.gardenP:
            self.area = 10
            self.orientationP = "North"

        else:
            self.area = 0
            self.orientationP = False

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError('A sold property cannot be canceled.')
            record.state = 'canceled'

    def action_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError('A canceled property cannot be set as sold.')
            print(" Action sold modele parent work ")
            record.state = 'sold'

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_digits=2):
                continue
            if float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) < 0:
                raise ValidationError('The selling price cannot be lower than 90% of the expected price.')

    def unlink(self):
        for record in self:
            if record.state not in ['new', 'canceled']:
                raise UserError('You cannot delete a property that is not in the "New" or "Canceled" state.')
        return super(EstateProperty, self).unlink()
