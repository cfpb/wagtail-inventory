from wagtailinventory.views import SearchView


try:
    from django.urls import re_path
except ImportError:
    from django.conf.urls import url as re_path


app_name = "wagtailinventory"


urlpatterns = [
    re_path(r"^$", SearchView.as_view(), name="search"),
]
