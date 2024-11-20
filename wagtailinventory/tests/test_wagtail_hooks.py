from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser, Permission
from django.http import HttpRequest
from django.test import TestCase
from django.urls import reverse

from wagtail.models import Page, Site
from wagtail.test.utils import WagtailTestUtils

from wagtailinventory.models import PageBlock
from wagtailinventory.wagtail_hooks import (
    CanViewBlockInventoryMenuItem,
    register_permissions,
)


User = get_user_model()


class TestWagtailHooks(TestCase, WagtailTestUtils):
    def setUp(self):
        self.root_page = Site.objects.get(is_default_site=True).root_page

        self.login()

    def test_page_edit_hooks(self):
        self.assertEqual(PageBlock.objects.all().count(), 0)

        # Creating a page should create its inventory with 2 blocks.
        post_data = {
            "title": "test",
            "slug": "test",
            "content-count": 2,
            "content-0-deleted": "",
            "content-0-order": 0,
            "content-0-type": "atom",
            "content-0-value-title": "atom",
            "content-1-deleted": "",
            "content-1-order": 1,
            "content-1-type": "molecule",
            "content-1-value-title": "molecule",
            "content-1-value-atoms-count": 0,
        }

        response = self.client.post(
            reverse(
                "wagtailadmin_pages:add",
                args=("testapp", "singlestreamfieldpage", self.root_page.id),
            ),
            post_data,
        )
        self.assertEqual(response.status_code, 302)

        page = Page.objects.get(slug="test")

        self.assertEqual(
            list(PageBlock.objects.values_list("page", flat=True)),
            [page.pk] * 4,
        )
        self.assertEqual(
            list(
                PageBlock.objects.order_by("block").values_list(
                    "block", flat=True
                )
            ),
            [
                "wagtail.blocks.field_block.CharBlock",
                "wagtail.blocks.list_block.ListBlock",
                "wagtailinventory.tests.testapp.blocks.Atom",
                "wagtailinventory.tests.testapp.blocks.Molecule",
            ],
        )

        # Updating the page should update its inventory.
        post_data = {
            "title": "test",
            "slug": "test",
            "content-count": 1,
            "content-0-deleted": "",
            "content-0-order": 0,
            "content-0-type": "atom",
            "content-0-value-title": "modified",
            "action-publish": "Publish",
        }

        response = self.client.post(
            reverse("wagtailadmin_pages:edit", args=[page.pk]),
            post_data,
        )
        self.assertEqual(response.status_code, 302)

        self.assertEqual(
            list(PageBlock.objects.values_list("page", flat=True)),
            [page.pk] * 2,
        )
        self.assertEqual(
            list(
                PageBlock.objects.order_by("block").values_list(
                    "block", flat=True
                )
            ),
            [
                "wagtail.blocks.field_block.CharBlock",
                "wagtailinventory.tests.testapp.blocks.Atom",
            ],
        )

        # Deleting the page should delete its inventory.
        response = self.client.post(
            reverse("wagtailadmin_pages:delete", args=[page.pk]),
        )
        self.assertEqual(response.status_code, 302)

        self.assertEqual(PageBlock.objects.count(), 0)

    def test_menu_item(self):
        item = CanViewBlockInventoryMenuItem("Test", "/admin/test/")

        admin_request = HttpRequest()
        admin_request.user = User.objects.filter(is_superuser=True).first()
        self.assertTrue(item.is_shown(admin_request))

        insufficient_permissions_request = HttpRequest()
        insufficient_permissions_request.user = AnonymousUser()
        self.assertFalse(item.is_shown(insufficient_permissions_request))

    def test_register_permissions(self):
        self.assertQuerySetEqual(
            register_permissions(),
            Permission.objects.filter(
                content_type__app_label="wagtailinventory",
                codename__in=["view_pageblock"],
            ),
        )
