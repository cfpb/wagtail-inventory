from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from wagtail.models import Page
from wagtail.test.utils import WagtailTestUtils


User = get_user_model()


class BlockInventoryReportViewTestCase(WagtailTestUtils, TestCase):
    fixtures = ["test_blocks.json"]

    def test_view(self):
        self.login()

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

    def test_view_no_permissions(self):
        # Create a user that can access the Wagtail admin but doesn't have
        # permission to view the block inventory report.
        user_without_permission = User.objects.create_user(
            username="noperm", email="", password="password"
        )
        user_without_permission.user_permissions.add(
            Permission.objects.get(
                content_type__app_label="wagtailadmin", codename="access_admin"
            )
        )

        self.client.login(username="noperm", password="password")
        response = self.client.get(
            reverse("wagtailinventory:block_inventory_report")
        )

        self.assertRedirects(response, reverse("wagtailadmin_home"))
        self.assertEqual(
            response.context["message"],
            "Sorry, you do not have permission to access this area.",
        )
