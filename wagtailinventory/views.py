from __future__ import absolute_import, unicode_literals

from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.views.generic import View
from wagtail.utils.pagination import paginate, replace_page_in_query
from wagtail.wagtailcore.models import Page

from wagtailinventory.forms import PageBlockQueryFormSet


class SearchView(View):
    template_name = 'wagtailinventory/search.html'

    def get(self, request):
        if len(request.GET) > 1:
            formset = PageBlockQueryFormSet(request.GET)
            if not formset.is_valid():
                return HttpResponseBadRequest('invalid query')

            pages = formset.get_query()
        else:
            formset = PageBlockQueryFormSet()
            pages = Page.objects.all()

        paginator, pages = paginate(request, pages.order_by('title'))

        for page in pages:
            page.can_choose = True

        return render(request, self.template_name, {
            'base_url': replace_page_in_query(request.GET.urlencode(), None),
            'formset': formset,
            'pages': pages,
        })
