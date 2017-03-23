from __future__ import absolute_import, unicode_literals

from django import forms
from django.db.models.fields import BLANK_CHOICE_DASH
from django.forms import formset_factory
from wagtail.wagtailcore.models import Page

from wagtailinventory.models import PageBlock


class PageBlockQueryForm(forms.Form):
    INCLUDES_BLOCK = 'includes'
    EXCLUDES_BLOCK = 'excludes'

    block = forms.ChoiceField(
        choices=(),
        required=False,
        label='Block type',
        widget=forms.Select(attrs={'style': 'width: 50%'})
    )

    has = forms.ChoiceField(
        choices=((c, c) for c in (INCLUDES_BLOCK, EXCLUDES_BLOCK)),
        label=None,
        widget=forms.Select(attrs={'style': 'width: 100px'})
    )

    def __init__(self, *args, **kwargs):
        super(PageBlockQueryForm, self).__init__(*args, **kwargs)
        block_choices = BLANK_CHOICE_DASH + [
            (b, b) for b in
            PageBlock.objects.values_list('block', flat=True).distinct()
        ]
        self.fields['block'].choices = block_choices


class BasePageBlockQueryFormSet(forms.BaseFormSet):
    def get_query(self):
        qs = Page.objects.all()

        for form in self.forms:
            if not form.is_valid():
                continue

            form_block = form.cleaned_data.get('block')

            if not form_block:
                continue

            condition = {'page_blocks__block': form_block}

            if form.cleaned_data['has'] == form.INCLUDES_BLOCK:
                qs = qs.filter(**condition)
            else:
                qs = qs.exclude(**condition)

        return qs


PageBlockQueryFormSet = formset_factory(
    PageBlockQueryForm,
    formset=BasePageBlockQueryFormSet,
    extra=3,
    max_num=3
)
