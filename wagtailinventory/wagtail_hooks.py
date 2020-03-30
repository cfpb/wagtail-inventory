from django.conf.urls import include, url

from wagtailinventory import urls
from wagtailinventory.helpers import (
    create_page_inventory,
    delete_page_inventory,
    update_page_inventory,
)


try:
    from django.urls import reverse
except ImportError:  # pragma: no cover; fallback for Django <1.10
    from django.core.urlresolvers import reverse

try:
    from wagtail.admin.menu import MenuItem
    from wagtail.core import hooks  # pragma: no cover
except ImportError:  # pragma: no cover; fallback for Wagtail <2.0
    from wagtail.wagtailadmin.menu import MenuItem
    from wagtail.wagtailcore import hooks


@hooks.register("after_create_page")
def do_after_page_create(request, page):
    create_page_inventory(page)


@hooks.register("after_edit_page")
def do_after_page_edit(request, page):
    update_page_inventory(page)


@hooks.register("after_delete_page")
def do_after_page_dete(request, page):
    delete_page_inventory(page)


@hooks.register("register_admin_urls")
def register_inventory_urls():
    return [
        url(r"^inventory/", include(urls, namespace="wagtailinventory")),
    ]


@hooks.register("register_settings_menu_item")
def register_inventory_menu_item():
    return MenuItem(
        "Block Inventory",
        reverse("wagtailinventory:search"),
        classnames="icon icon-placeholder",
        order=11000,
    )
