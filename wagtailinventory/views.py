from django.forms.widgets import SelectMultiple

from wagtail.admin.auth import permission_denied
from wagtail.admin.filters import ContentTypeFilter, WagtailFilterSet
from wagtail.admin.views.reports import PageReportView
from wagtail.models import Page, get_page_content_types

import django_filters

from wagtailinventory.models import PageBlock


def get_block_choices():
    return [
        (page_block, page_block)
        for page_block in PageBlock.objects.distinct()
        .order_by("block")
        .values_list("block", flat=True)
    ]


class BlockInventoryFilterSet(WagtailFilterSet):
    include_page_blocks = django_filters.MultipleChoiceFilter(
        field_name="page_blocks__block",
        label="Include Blocks",
        distinct=True,
        choices=get_block_choices,
        widget=SelectMultiple(attrs={"style": "overflow: auto"}),
    )
    exclude_page_blocks = django_filters.MultipleChoiceFilter(
        field_name="page_blocks__block",
        label="Exclude Blocks",
        distinct=True,
        exclude=True,
        choices=get_block_choices,
        widget=SelectMultiple(attrs={"style": "overflow: auto"}),
    )
    content_type = ContentTypeFilter(
        label="Page Type",
        queryset=lambda request: get_page_content_types(),
    )

    class Meta:
        model = Page
        fields = ["include_page_blocks", "exclude_page_blocks", "content_type"]


class BlockInventoryReportView(PageReportView):
    page_title = "Block inventory"
    header_icon = "placeholder"
    filterset_class = BlockInventoryFilterSet
    index_url_name = "wagtailinventory:block_inventory_report"
    index_results_url_name = "wagtailinventory:block_inventory_report_results"

    @classmethod
    def check_permissions(cls, request):
        return request.user.is_superuser or request.user.has_perm(
            "wagtailinventory.view_pageblock"
        )

    def dispatch(self, request, *args, **kwargs):
        if not self.check_permissions(request):
            return permission_denied(request)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        self.queryset = Page.objects.order_by("title")
        return super().get_queryset()
