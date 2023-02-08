from django.db.models.fields import BLANK_CHOICE_DASH
from django.test import TestCase

from wagtail.models import Page, Site

from wagtailinventory.forms import PageBlockQueryForm, PageBlockQueryFormSet
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


class TestPageBlockQueryFormSet(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.root_page = Page.objects.get(pk=1)
        cls.site_root = Site.objects.get(is_default_site=True).root_page

        cls.apple_page = Page(title="Apple", slug="apple")
        cls.site_root.add_child(instance=cls.apple_page)
        PageBlock.objects.create(page=cls.apple_page, block="blocks.apple")

        cls.banana_page = Page(title="Banana", slug="banana")
        cls.site_root.add_child(instance=cls.banana_page)
        PageBlock.objects.create(page=cls.banana_page, block="blocks.banana")

    def test_empty_formset_returns_all_pages(self):
        formset = PageBlockQueryFormSet(
            data={
                "form-TOTAL_FORMS": "1",
                "form-INITIAL_FORMS": "0",
            }
        )
        self.assertQuerysetEqual(formset.get_query(), Page.objects.all())

    def test_invalid_formset_returns_all_pages(self):
        formset = PageBlockQueryFormSet(
            data={
                "form-TOTAL_FORMS": "1",
                "form-INITIAL_FORMS": "0",
                "form-0-block": "invalid",
                "form-0-has": None,
            }
        )
        self.assertQuerysetEqual(formset.get_query(), Page.objects.all())

    def test_formset_filtering_includes(self):
        formset = PageBlockQueryFormSet(
            data={
                "form-TOTAL_FORMS": "1",
                "form-INITIAL_FORMS": "0",
                "form-0-block": "blocks.apple",
                "form-0-has": PageBlockQueryForm.INCLUDES_BLOCK,
            }
        )
        self.assertQuerysetEqual(formset.get_query(), [self.apple_page])

    def test_formset_filtering_excludes(self):
        formset = PageBlockQueryFormSet(
            data={
                "form-TOTAL_FORMS": "1",
                "form-INITIAL_FORMS": "0",
                "form-0-block": "blocks.apple",
                "form-0-has": PageBlockQueryForm.EXCLUDES_BLOCK,
            }
        )
        self.assertQuerysetEqual(
            formset.get_query(),
            [self.root_page, self.site_root, self.banana_page],
        )
