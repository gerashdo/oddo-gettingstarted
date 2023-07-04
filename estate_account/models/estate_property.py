from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_set_property_as_sold(self):
        self.ensure_one()
        self.check_access_rights("write")
        self.check_access_rule("write")

        move_type = "out_invoice"
        invoice_line_vals = self._create_invoice_lines()

        invoice_vals = {
            "partner_id": self.buyer_id.id,
            "move_type": move_type,
            "invoice_line_ids": invoice_line_vals,
        }

        self.env["account.move"].sudo().create([invoice_vals])

        return super().action_set_property_as_sold()

    def _create_invoice_lines(self):
        invoice_line_vals = [
            Command.create(
                {
                    "name": "Invoice",
                    "quantity": 1,
                    "price_unit": self.selling_price * 0.06,
                }
            ),
            Command.create(
                {
                    "name": "Administrative fees",
                    "quantity": 1,
                    "price_unit": 100,
                }
            ),
        ]
        return invoice_line_vals
