from django.test import TestCase

from wagtail.core.models import Page

from wagtailinventory.models import PageBlock


class TestPageBlock(TestCase):
    def test_page_str(self):
        page_block = PageBlock(
            page=Page(title="Title", slug="title"), block="path.to.block"
        )
        self.assertEqual(str(page_block), "<Title, path.to.block>")
