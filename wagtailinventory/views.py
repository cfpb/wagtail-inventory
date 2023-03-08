from wagtail.admin.filters import WagtailFilterSet
from wagtail.admin.views.reports import PageReportView
from wagtail.models import Page

import django_filters
from dal import autocomplete

from wagtailinventory.models import PageBlock


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
        widget=autocomplete.Select2Multiple(
            url="wagtailinventory:block_autocomplete"
        ),
    )
    exclude_page_blocks = django_filters.AllValuesMultipleFilter(
        field_name="page_blocks__block",
        label="Exclude Blocks",
        distinct=True,
        exclude=True,
        widget=autocomplete.Select2Multiple(
            url="wagtailinventory:block_autocomplete"
        ),
    )

    class Meta:
        model = Page
        fields = ["include_page_blocks", "exclude_page_blocks"]


class BlockInventoryReportView(PageReportView):
    title = "Block inventory"
    header_icon = "placeholder"
    filterset_class = BlockInventoryFilterSet

    def get_queryset(self):
        self.queryset = Page.objects.order_by("title")
        return super().get_queryset()
