import json

from django.test import TestCase

from wagtailinventory.helpers import get_page_blocks
from wagtailinventory.tests.testapp.models import (
    MultipleStreamFieldsPage, NoStreamFieldsPage, SingleStreamFieldPage
)


class TestGetPageBlocks(TestCase):
    def test_page_with_no_streamfields_returns_empty_list(self):
        page = NoStreamFieldsPage(title='test', slug='test', content='test')
        self.assertEqual(get_page_blocks(page), [])

    def make_page_with_streamfields(self, page_cls, **streamfields):
        page_kwargs = {
            'title': 'test',
            'slug': 'test',
        }

        for field, content in streamfields.items():
            page_kwargs.update({field: json.dumps(content)})

        return page_cls(**page_kwargs)

    def test_empty_streamfield_returns_empty_list(self):
        page = self.make_page_with_streamfields(SingleStreamFieldPage)
        self.assertEqual(get_page_blocks(page), [])

    def test_streamfield_with_single_block(self):
        page = self.make_page_with_streamfields(
            SingleStreamFieldPage,
            content=[{'type': 'text', 'value': 'foo'}]
        )

        self.assertEqual(
            get_page_blocks(page),
            ['wagtail.wagtailcore.blocks.field_block.CharBlock']
        )

    def test_streamfield_with_multiple_blocks_of_same_type(self):
        page = self.make_page_with_streamfields(
            SingleStreamFieldPage,
            content=[
                {'type': 'text', 'value': 'foo'},
                {'type': 'text', 'value': 'bar'},
            ]
        )

        self.assertEqual(
            get_page_blocks(page),
            ['wagtail.wagtailcore.blocks.field_block.CharBlock']
        )

    def test_streamfield_with_structblock_includes_nested_blocks(self):
        page = self.make_page_with_streamfields(
            SingleStreamFieldPage,
            content=[
                {'type': 'atom', 'value': {'title': 'foo'}},
            ]
        )

        self.assertEqual(
            get_page_blocks(page),
            [
                'wagtail.wagtailcore.blocks.field_block.CharBlock',
                'wagtailinventory.tests.testapp.blocks.Atom',
            ]
        )

    def test_streamfield_with_deeply_nested_blocks(self):
        page = self.make_page_with_streamfields(
            SingleStreamFieldPage,
            content=[
                {
                    'type': 'organism',
                    'value': {
                        'molecules': [
                            {'title': 'foo', 'atoms': []},
                            {'title': 'bar', 'atoms': []},
                        ],
                    },
                },
            ]
        )

        self.assertEqual(
            get_page_blocks(page),
            [
                'wagtail.wagtailcore.blocks.field_block.CharBlock',
                'wagtail.wagtailcore.blocks.list_block.ListBlock',
                'wagtailinventory.tests.testapp.blocks.Molecule',
                'wagtailinventory.tests.testapp.blocks.Organism',
            ]
        )

    def test_multiple_streamfields(self):
        page = self.make_page_with_streamfields(
            MultipleStreamFieldsPage,
            first=[{'type': 'atom', 'value': 'foo'}],
            second=[
                {
                    'type': 'organism',
                    'value': {
                        'molecules': [
                            {'title': 'foo', 'atoms': []},
                        ]
                    }
                },
            ]
        )

        self.assertEqual(
            get_page_blocks(page),
            [
                'wagtail.wagtailcore.blocks.field_block.CharBlock',
                'wagtail.wagtailcore.blocks.list_block.ListBlock',
                'wagtailinventory.tests.testapp.blocks.Atom',
                'wagtailinventory.tests.testapp.blocks.Molecule',
                'wagtailinventory.tests.testapp.blocks.Organism',
            ]
        )
