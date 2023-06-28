from odoo import fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of a property"

    name = fields.Char()
    property_ids = fields.One2many("estate.property", "property_type_id")

    _sql_constraints = [("name_unique", "UNIQUE(name)", "The name must be unique.")]
