from __future__ import print_function

from django.core.management import BaseCommand
from tqdm import tqdm
from wagtail.wagtailcore.models import Page

from wagtailinventory.helpers import (
    create_page_inventory, delete_page_inventory
)


class Command(BaseCommand):
    def handle(self, *args, **options):
        delete_page_inventory()

        for page in tqdm(Page.objects.all()):
            create_page_inventory(page)
