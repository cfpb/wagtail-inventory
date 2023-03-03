from django.core.management import BaseCommand

from wagtail.models import Page

from tqdm import tqdm

from wagtailinventory.helpers import (
    create_page_inventory,
    delete_page_inventory,
)


class Command(BaseCommand):
    def handle(self, *args, **options):
        delete_page_inventory()

        pages = Page.objects.all()

        if options.get("verbosity"):  # pragma: no cover
            pages = tqdm(pages)

        for page in pages:
            create_page_inventory(page)
