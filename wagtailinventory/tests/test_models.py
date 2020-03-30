from django.test import TestCase

from wagtailinventory.models import PageBlock


try:
    from wagtail.core.models import Page
except ImportError:  # pragma: no cover; fallback for Wagtail <2.0
    from wagtail.wagtailcore.models import Page


class TestPageBlock(TestCase):
    def test_page_str(self):
        page_block = PageBlock(
            page=Page(title="Title", slug="title"), block="path.to.block"
        )
        self.assertEqual(str(page_block), "<Title, path.to.block>")
