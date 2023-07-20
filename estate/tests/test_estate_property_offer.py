from odoo.exceptions import UserError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class PropertyOfferTestCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.sold_property = cls.env["estate.property"].create(
            {
                "name": "Property A",
                "expected_price": 200000,
                "state": "sold",
            }
        )

        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Test partner",
                "email": "test@test_domain.xyz",
                "is_company": False,
            }
        )

    def test_should_not_allow_create_offer_in_sold_property(self):
        """New offers can just be created in properties which are not sold"""

        with self.assertRaises(UserError):
            self.env["estate.property.offer"].create(
                {
                    "price": 200000,
                    "partner_id": self.partner.id,
                    "property_id": self.sold_property.id,
                }
            )
