from urllib.parse import urlencode

from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from wagtail.core.models import Page
from wagtail.tests.utils import WagtailTestUtils


class SearchViewTests(WagtailTestUtils, TestCase):
    fixtures = ["test_blocks.json"]

    def setUp(self):
        self.login()

    def get(self, params=None):
        path = reverse("wagtailinventory:search")

        if params:
            path += "?" + urlencode(params)

        return self.client.get(path)

    def test_empty_query_returns_200_and_all_pages_ordered_by_title(self):
        response = self.get()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["pages"].object_list,
            list(Page.objects.order_by("title")),
        )

    def test_get_bad_formset_query_returns_400(self):
        response = self.get(
            {
                "form-TOTAL_FORMS": 1,
                "form-INITIAL_FORMS": 0,
                "form-0-has": "invalid",
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_valid_query_returns_200_and_only_appropriate_pages(self):
        call_command("block_inventory", verbosity=0)

        response = self.get(
            {
                "form-TOTAL_FORMS": 1,
                "form-INITIAL_FORMS": 0,
                "form-0-has": "includes",
                "form-0-block": "wagtailinventory.tests.testapp.blocks.Organism",  # noqa
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["pages"].object_list,
            [Page.objects.get(slug="multiple-streamfields-page")],
        )
