from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate property model"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        copy=False, default=fields.Date.add(fields.Date.today(), months=3), help="Date from when it will be available."
    )
    expected_price = fields.Float(required=True, help="Price at which you wish to sell the property.")
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ]
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        required=True,
        default="new",
        copy=False,
        string="Status",
    )
    property_type_id = fields.Many2one("estate.property.type")
    buyer_id = fields.Many2one("res.partner", copy=False)
    salesperson_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")
    company_id = fields.Many2one("res.company", required=True, default=lambda self: self.env.company)

    _sql_constraints = [
        ("check_expected_price", "CHECK(expected_price > 0)", "The expected price must be strictly positive."),
        ("check_selling_price", "CHECK(selling_price >= 0)", "The selling price must be strictly positive."),
    ]

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price")) if record.offer_ids else 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = None

    @api.constrains("expected_price", "selling_price")
    def _check_selling_price(self):
        for record in self.filtered(lambda element: element.selling_price > 0):
            if float_compare(record.selling_price, record.expected_price * 0.9, 2) < 0:
                raise ValidationError(
                    _(
                        "The selling price must be at least 90% of the expected price. "
                        "You must reduce the expected price if you want to accept this offer."
                    )
                )

    @api.ondelete(at_uninstall=False)
    def _unlik_if_new_or_canceled(self):
        if any(property.state not in ["new", "canceled"] for property in self):
            raise UserError(_("Only new or canceled properties can be deleted."))

    def action_set_property_as_sold(self):
        self.ensure_one()

        if self.state == "canceled":
            raise UserError(_("A canceled property can not be sold."))
        self.state = "sold"
        return True

    def action_set_property_as_canceled(self):
        self.ensure_one()

        if self.state == "sold":
            raise UserError(_("A sold property can not be canceled."))
        self.state = "canceled"
        return True
