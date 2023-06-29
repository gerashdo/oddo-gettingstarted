from odoo import fields, models


class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tags for properties"

    name = fields.Char(required=True)
