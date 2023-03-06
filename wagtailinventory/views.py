from django import forms

from wagtail.admin.filters import WagtailFilterSet
from wagtail.admin.views.reports import PageReportView
from wagtail.models import Page

import django_filters

from wagtailinventory.checks import dal_select2_check_all
from wagtailinventory.models import PageBlock


# If django-autocomplete-light is present, we'll do two things:
#
# 1. Set the widget used for the block include/exclude filters to DAL's
#    multi-select;
# 2. Create a list view populated with available blocks to autocomplete.
#
# If it's not present, we'll fall back on Django's built-in SelectMultiple
# widget.
if not dal_select2_check_all():  # pragma: no cover
    autocomplete = None
    block_widget = forms.SelectMultiple()
else:
    from dal import autocomplete

    block_widget = autocomplete.Select2Multiple(
        url="wagtailinventory:block_autocomplete"
    )

    class BlockAutocompleteView(autocomplete.Select2ListView):
        def get_list(self):
            return (
                PageBlock.objects.distinct()
                .order_by("block")
                .values_list("block", flat=True)
            )


class BlockInventoryFilterSet(WagtailFilterSet):
    include_page_blocks = django_filters.AllValuesMultipleFilter(
        field_name="page_blocks__block",
        label="Include Blocks",
        distinct=True,
        widget=block_widget,
    )
    exclude_page_blocks = django_filters.AllValuesMultipleFilter(
        field_name="page_blocks__block",
        label="Exclude Blocks",
        exclude=True,
        widget=block_widget,
    )

    class Meta:
        model = Page
        fields = ["include_page_blocks", "exclude_page_blocks"]


class BlockInventoryReportView(PageReportView):
    template_name = "wagtailadmin/reports/base_page_report.html"
    title = "Block inventory"
    header_icon = "placeholder"
    filterset_class = BlockInventoryFilterSet

    def get_queryset(self):
        self.queryset = Page.objects.order_by("title")
        return super().get_queryset()
