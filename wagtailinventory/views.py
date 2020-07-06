from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.views.generic import View

import wagtail
from wagtail.core.models import Page

from wagtailinventory.forms import PageBlockQueryFormSet


class SearchView(View):
    template_name = "wagtailinventory/search.html"

    def get(self, request):
        if len(request.GET) > 1:
            formset = PageBlockQueryFormSet(request.GET)
            if not formset.is_valid():
                return HttpResponseBadRequest("invalid query")

            queryset = formset.get_query()
        else:
            formset = PageBlockQueryFormSet()
            queryset = Page.objects.all()

        queryset = queryset.order_by("title")

        # https://docs.wagtail.io/en/latest/releases/2.5.html#changes-to-admin-pagination-helpers
        if wagtail.VERSION < (2, 5):
            from wagtail.utils.pagination import paginate

            paginator, pages = paginate(request, queryset)
        else:  # pragma: no cover
            from django.core.paginator import Paginator

            paginator = Paginator(queryset, per_page=20)
            pages = paginator.get_page(request.GET.get("p"))

        for page in pages:
            page.can_choose = True

        return render(
            request, self.template_name, {"formset": formset, "pages": pages}
        )
