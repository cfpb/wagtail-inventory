from django.conf import settings
from django.conf.urls import include, url


try:
    from wagtail.admin import urls as wagtailadmin_urls
    from wagtail.core import urls as wagtailcore_urls  # pragma: no cover
    from wagtail.documents import urls as wagtaildocs_urls  # pragma: no cover
except ImportError:  # pragma: no cover; fallback for Wagtail <2.0
    from wagtail.wagtailadmin import urls as wagtailadmin_urls
    from wagtail.wagtailcore import urls as wagtailcore_urls
    from wagtail.wagtaildocs import urls as wagtaildocs_urls


urlpatterns = [
    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'', include(wagtailcore_urls)),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
