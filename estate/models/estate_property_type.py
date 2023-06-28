from odoo import fields, models


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Type of a property"

    name = fields.Char()

    _sql_constraints = [("name_unique", "UNIQUE(name)", "The name must be unique.")]
