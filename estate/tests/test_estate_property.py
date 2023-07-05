from odoo.exceptions import UserError
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class EstatePropertyTestCase(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.property = cls.env["estate.property"].create(
            {
                "name": "Property A",
                "expected_price": 200000,
                "state": "new",
            }
        )

        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Test partner",
                "email": "test@test_domain.xyz",
                "is_company": False,
            }
        )

    def test_should_be_set_as_sold(self):
        """When a property is set as sold, it should change its state to 'sold'"""

        with Form(self.property) as property_form:
            with property_form.offer_ids.new() as offer_form:
                offer_form.price = 200000
                offer_form.partner_id = self.partner

        self.property.offer_ids[0].action_accept_offer()
        self.property.action_set_property_as_sold()

        self.assertEqual(self.property.state, "sold")

    def test_should_not_allow_set_as_sold_if_there_is_no_accepted_offer(self):
        """The property can only be set as sold if an offer has been accepted"""

        with self.assertRaisesRegex(UserError, "There is no offer accepted."):
            self.property.action_set_property_as_sold()

        with Form(self.property) as property_form, property_form.offer_ids.new() as offer_form:
            offer_form.price = 200000
            offer_form.partner_id = self.partner

        with self.assertRaisesRegex(UserError, "There is no offer accepted."):
            self.property.action_set_property_as_sold()
