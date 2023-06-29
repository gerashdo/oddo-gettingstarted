from odoo import api, fields, models


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offers for properties"

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7, string="Validity (days)")
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_validity", string="Deadline")

    def _inverse_validity(self):
        for record in self:
            end_date = fields.Date.to_date(record.create_date) if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - end_date).days

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            start_date = record.create_date if record.create_date else fields.Date.today()
            record.date_deadline = fields.Date.add(start_date, days=record.validity)
