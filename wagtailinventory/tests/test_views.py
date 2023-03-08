from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from wagtail.models import Page
from wagtail.test.utils import WagtailTestUtils


class BlockAutocompleteViewTestCase(WagtailTestUtils, TestCase):
    fixtures = ["test_blocks.json"]

    def setUp(self):
        self.login()

    def test_get_list(self):
        call_command("block_inventory", verbosity=0)
        response = self.client.get(
            reverse("wagtailinventory:block_autocomplete")
        )

        json_response = response.json()
        self.assertIn("results", json_response)

        results = json_response["results"]

        # There are six unique block types in our test fixture
        self.assertEqual(len(results), 6)

        # Make sure that one of the results matches our expected id/text
        # pairing
        self.assertIn(
            {
                "id": "wagtail.blocks.field_block.CharBlock",
                "text": "wagtail.blocks.field_block.CharBlock",
            },
            results,
        )


class BlockInventoryReportViewTestCase(WagtailTestUtils, TestCase):
    fixtures = ["test_blocks.json"]

    def setUp(self):
        self.login()

    def test_view(self):
        response = self.client.get(
            reverse("wagtailinventory:block_inventory_report")
        )
        self.assertIn("object_list", response.context)

        # Right now our queryset just returns all pages, to be filtered by the
        # superclass. We might want to put some guardrails around that later,
        # in which case this test will be more useful. For now this test just
        # tests that it does that.
        view_qs = response.context["object_list"]
        page_qs = Page.objects.order_by("title")
        self.assertEqual(list(view_qs), list(page_qs))
