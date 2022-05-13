from django.test import TestCase

from wagtail.core.models import Page

from wagtailinventory.helpers import get_page_blocks


CORE_BLOCKS = "wagtail.core.blocks"


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
