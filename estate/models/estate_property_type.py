from odoo import fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of a property"
    _order = "secuence, name"

    name = fields.Char()
    property_ids = fields.One2many("estate.property", "property_type_id")
    secuence = fields.Integer(default=1)

    _sql_constraints = [("name_unique", "UNIQUE(name)", "The name must be unique.")]
