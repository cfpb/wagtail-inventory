from django.apps import AppConfig

from . import checks  # noqa F401


class WagtailInventoryAppConfig(AppConfig):
    name = "wagtailinventory"
    verbose_name = "Wagtail Inventory"
    default_auto_field = "django.db.models.BigAutoField"
