from __future__ import print_function

from django.core.management import BaseCommand
from wagtail.wagtailcore.models import Page

from wagtailinventory.helpers import (
    create_page_inventory, delete_page_inventory
)


class Command(BaseCommand):
    def handle(self, *args, **options):
        delete_page_inventory()

        count = Page.objects.count()
        for i, page in enumerate(Page.objects.all()):
            print(i + 1, '/', count, page)
            create_page_inventory(page)
