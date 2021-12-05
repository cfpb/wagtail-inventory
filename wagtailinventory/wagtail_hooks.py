from django.conf.urls import include, url
from django.contrib.auth.models import Permission

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

    

class PermissionCheckingMenuItem(MenuItem):
    """
    MenuItem that only displays if the user has a certain permission.
    This subclassing approach is recommended by the Wagtail documentation:
    https://docs.wagtail.io/en/stable/reference/hooks.html#register-admin-menu-item
    """

    def __init__(self, *args, **kwargs):
        self.permission = kwargs.pop('permission')
        super(PermissionCheckingMenuItem, self).__init__(*args, **kwargs)

    def is_shown(self, request):
        if request.user.is_superuser or request.user.has_perm(self.permission):
            return True


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




@hooks.register('register_permissions')
def register_permissions():
    return Permission.objects.filter(
        content_type__app_label='wagtailinventory',
        codename__in=['index_wagtailinventory',]
    )


@hooks.register("register_settings_menu_item")
def register_inventory_menu_item():
    return PermissionCheckingMenuItem(
        "Block Inventory",
        reverse("wagtailinventory:search"),
        classnames="icon icon-placeholder",
        order=11000,
        permission='wagtailinventory.index_wagtailinventory'
    )
