from django.conf.urls import url

from wagtailinventory.views import SearchView


app_name = 'wagtailinventory'


urlpatterns = [
    url(r'^$', SearchView.as_view(), name='search'),
]
