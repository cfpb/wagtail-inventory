from __future__ import absolute_import, unicode_literals

from django.conf.urls import include, url
from django.core.urlresolvers import reverse
from wagtail.wagtailadmin.menu import MenuItem
from wagtail.wagtailcore import hooks

from wagtailinventory.helpers import (
    create_page_inventory, delete_page_inventory, update_page_inventory
)
from wagtailinventory.views import SearchView


@hooks.register('after_create_page')
def do_after_page_create(request, page):
    create_page_inventory(page)


@hooks.register('after_edit_page')
def do_after_page_edit(request, page):
    update_page_inventory(page)


@hooks.register('after_delete_page')
def do_after_page_dete(request, page):
    delete_page_inventory(page)


@hooks.register('register_admin_urls')
def register_inventory_urls():
    return [
        url(
            r'^inventory/',
            include(
                [url(r'$', SearchView.as_view(), name='search')],
                namespace='wagtailinventory'
            )
        ),
    ]


@hooks.register('register_settings_menu_item')
def register_inventory_menu_item():
    return MenuItem(
        'Block Inventory',
        reverse('wagtailinventory:search'),
        classnames='icon icon-placeholder',
        order=11000
    )
