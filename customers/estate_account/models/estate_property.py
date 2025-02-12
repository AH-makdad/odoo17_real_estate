from odoo import models, Command


# from odoo.exceptions import UserError

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        # Call the original action first
        super_result = super().action_sold()

        for property in self:
            # Create invoice lines
            invoice_lines = [
                Command.create({
                    'name': 'Selling Price Commission (6%)',
                    'quantity': 1,
                    'price_unit': property.selling_price * 0.06,
                }),
                Command.create({
                    'name': 'Administrative Fees',
                    'quantity': 1,
                    'price_unit': 100.00,
                }),
            ]

            # Create the invoice
            self.env['account.move'].create({
                'move_type': 'out_invoice',
                'partner_id': property.buyer_id.id,
                'invoice_line_ids': invoice_lines,
            })

        return super_result
