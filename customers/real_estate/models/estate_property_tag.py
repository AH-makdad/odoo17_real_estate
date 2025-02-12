from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'
    name = fields.Char(string="Name", required=True)
    score = fields.Char(string="Score")
    sequence_tag = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    color = fields.Integer(string='Color')
    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'The property tag name must be unique.')
    ]
