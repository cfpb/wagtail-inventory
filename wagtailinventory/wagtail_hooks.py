from django.contrib.auth.models import Permission
from django.urls import include, path, reverse

from wagtail import hooks
from wagtail.admin.menu import MenuItem

from wagtailinventory.helpers import (
    create_page_inventory,
    delete_page_inventory,
    update_page_inventory,
)
from wagtailinventory.views import BlockInventoryReportView


@hooks.register("after_create_page")
def do_after_page_create(request, page):
    create_page_inventory(page)


@hooks.register("after_edit_page")
def do_after_page_edit(request, page):
    update_page_inventory(page)


@hooks.register("after_delete_page")
def do_after_page_dete(request, page):
    delete_page_inventory(page)


@hooks.register("register_permissions")
def register_permissions():
    return Permission.objects.filter(
        content_type__app_label="wagtailinventory",
        codename__in=["view_pageblock"],
    )


class CanViewBlockInventoryMenuItem(MenuItem):
    def is_shown(self, request):
        return BlockInventoryReportView.check_permissions(request)


@hooks.register("register_reports_menu_item")
def register_inventory_report_menu_item():
    return CanViewBlockInventoryMenuItem(
        "Block inventory",
        reverse("wagtailinventory:block_inventory_report"),
        icon_name=BlockInventoryReportView.header_icon,
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
            "results/",
            BlockInventoryReportView.as_view(results_only=True),
            name="block_inventory_report_results",
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
