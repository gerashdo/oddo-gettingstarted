from odoo import _, api, fields, models
from odoo.exceptions import UserError


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

    _sql_constraints = [
        ("check_price", "CHECK(price > 0)", "The price must be strictly positive"),
    ]

    def _inverse_validity(self):
        for record in self:
            end_date = fields.Date.to_date(record.create_date) if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - end_date).days

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            start_date = record.create_date if record.create_date else fields.Date.today()
            record.date_deadline = fields.Date.add(start_date, days=record.validity)

    def action_accept_offer(self):
        self.ensure_one()

        if self.property_id.buyer_id:
            raise UserError(_("There is an offer accepted already for this property."))

        self.status = "accepted"
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id
        self.property_id.state = "offer_accepted"
        return True

    def action_refuse_offer(self):
        self.ensure_one()

        if self.property_id.offer_ids.filtered(lambda record: record.id == self.id and record.status == "accepted"):
            self.property_id.selling_price = 0
            self.property_id.buyer_id = False
            self.property_id.state = "offer_received"

        self.status = "refused"
        return True
