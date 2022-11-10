from django.core.management import call_command
from django.test import TestCase

import wagtail
from wagtail.core.models import Page

from wagtailinventory.helpers import (
    get_page_blocks,
    get_page_inventory,
    update_page_inventory,
)


if wagtail.VERSION < (3, 0):  # pragma: nocover
    CORE_BLOCKS = "wagtail.core.blocks"
else:
    CORE_BLOCKS = "wagtail.blocks"


class TestGetPageBlocks(TestCase):
    fixtures = ["test_blocks.json"]

    def test_page_with_no_streamfields_returns_empty_list(self):
        page = Page.objects.get(slug="no-streamfields-page")
        self.assertEqual(get_page_blocks(page), [])

    def test_empty_streamfield_returns_empty_list(self):
        page = Page.objects.get(slug="single-streamfield-page-no-content")
        self.assertEqual(get_page_blocks(page), [])

    def test_streamfield_with_single_block(self):
        page = Page.objects.get(slug="single-streamfield-page-content")
        self.assertEqual(
            get_page_blocks(page),
            [
                CORE_BLOCKS + ".field_block.CharBlock",
                "wagtailinventory.tests.testapp.blocks.Atom",
            ],
        )

    def test_multiple_streamfields(self):
        page = Page.objects.get(slug="multiple-streamfields-page")
        self.assertEqual(
            get_page_blocks(page),
            [
                CORE_BLOCKS + ".field_block.CharBlock",
                CORE_BLOCKS + ".list_block.ListBlock",
                "wagtailinventory.tests.testapp.blocks.Atom",
                "wagtailinventory.tests.testapp.blocks.Molecule",
                "wagtailinventory.tests.testapp.blocks.Organism",
            ],
        )

    def test_nested_streamblocks(self):
        page = Page.objects.get(slug="nested-streamblock-page")
        self.assertEqual(
            get_page_blocks(page),
            [
                CORE_BLOCKS + ".field_block.CharBlock",
                CORE_BLOCKS + ".stream_block.StreamBlock",
                "wagtailinventory.tests.testapp.blocks.Atom",
            ],
        )


class TestPageInventoryHelpers(TestCase):
    fixtures = ["test_blocks.json"]

    def setUp(self):
        call_command("block_inventory", verbosity=0)

    def test_get_all_pageblocks(self):
        self.assertEqual(get_page_inventory().count(), 10)

    def test_get_pageblocks_filtered_by_page(self):
        page = Page.objects.get(slug="single-streamfield-page-content")
        self.assertEqual(get_page_inventory(page).count(), 2)

    def test_update_page(self):
        # First the page has 2 blocks.
        page = Page.objects.get(slug="single-streamfield-page-content")
        self.assertEqual(get_page_inventory(page).count(), 2)

        # Delete the page's blocks.
        page = page.specific
        page.content = []
        page.save_revision().publish()

        # Updating the page should remove the block inventory.
        update_page_inventory(page)
        self.assertEqual(get_page_inventory(page).count(), 0)
