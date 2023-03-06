from django.urls import include, path, reverse

from wagtail import hooks
from wagtail.admin.menu import AdminOnlyMenuItem

from wagtailinventory.helpers import (
    create_page_inventory,
    delete_page_inventory,
    update_page_inventory,
)
from wagtailinventory.views import (
    BlockAutocompleteView,
    BlockInventoryReportView,
)


@hooks.register("after_create_page")
def do_after_page_create(request, page):
    create_page_inventory(page)


@hooks.register("after_edit_page")
def do_after_page_edit(request, page):
    update_page_inventory(page)


@hooks.register("after_delete_page")
def do_after_page_dete(request, page):
    delete_page_inventory(page)


@hooks.register("register_reports_menu_item")
def register_inventory_report_menu_item():
    return AdminOnlyMenuItem(
        "Block inventory",
        reverse("wagtailinventory:block_inventory_report"),
        classnames="icon icon-" + BlockInventoryReportView.header_icon,
    )


@hooks.register("register_admin_urls")
def register_inventory_report_url():
    report_urls = [
        path(
            "",
            BlockInventoryReportView.as_view(),
            name="block_inventory_report",
        ),
        path(
            "block-autocomplete/",
            BlockAutocompleteView.as_view(),
            name="block_autocomplete",
        ),
    ]

    return [
        path(
            "block-inventory/",
            include(
                (report_urls, "wagtailinventory"),
                namespace="wagtailinventory",
            ),
        )
    ]
