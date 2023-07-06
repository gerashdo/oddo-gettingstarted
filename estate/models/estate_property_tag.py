from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tags for properties"
    _order = "name"

    name = fields.Char(required=True)

    _sql_constraints = [("name_unique", "UNIQUE(name)", "The name must be unique.")]
