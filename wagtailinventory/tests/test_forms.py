from django.db.models.fields import BLANK_CHOICE_DASH
from django.test import TestCase

from wagtail.core.models import Page, Site

from wagtailinventory.forms import PageBlockQueryForm
from wagtailinventory.models import PageBlock


class TestPageBlockQueryForm(TestCase):
    def test_no_page_blocks_in_database_form_has_blank_choice(self):
        form = PageBlockQueryForm()
        form_choices = form.fields["block"].choices

        self.assertEqual(len(form_choices), 1)
        self.assertEqual(form_choices, BLANK_CHOICE_DASH)

    def test_form_choices_alphabetized(self):
        root_page = Site.objects.get(is_default_site=True).root_page
        page = Page(title="Title", slug="title")
        root_page.add_child(instance=page)

        for block in (
            "blocks.mango",
            "blocks.apple",
            "blocks.banana",
        ):
            PageBlock.objects.create(page=page, block=block)

        form = PageBlockQueryForm()
        form_choices = form.fields["block"].choices

        self.assertEqual(len(form_choices), 4)
        self.assertEqual(form_choices[1][0], "blocks.apple")
        self.assertEqual(form_choices[2][0], "blocks.banana")
        self.assertEqual(form_choices[3][0], "blocks.mango")
