import wagtail
from wagtail.admin.auth import permission_denied
from wagtail.admin.filters import ContentTypeFilter, WagtailFilterSet
from wagtail.admin.views.reports import PageReportView
from wagtail.models import Page

import django_filters
from dal import autocomplete

from wagtailinventory.models import PageBlock


if wagtail.VERSION >= (6,):
    from wagtail.models import get_page_content_types
else:  # pragma: no cover
    # For Wagtail < 6, use an older method to get the list of page types.
    from wagtail.admin.views.reports.aging_pages import (
        get_content_types_for_filter,
    )

    def get_page_content_types(include_base_page_type=True):
        return get_content_types_for_filter()


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
    content_type = ContentTypeFilter(
        label="Page Type",
        queryset=lambda request: get_page_content_types(),
    )

    class Meta:
        model = Page
        fields = ["include_page_blocks", "exclude_page_blocks", "content_type"]


class BlockInventoryReportView(PageReportView):
    title = "Block inventory"
    header_icon = "placeholder"
    filterset_class = BlockInventoryFilterSet

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
