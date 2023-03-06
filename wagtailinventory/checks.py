from django.conf import settings
from django.core.checks import Info, Tags, Warning, register


def dal_select2_check_all():
    """Ensure django-autocomplete-light is fully installed"""
    try:
        from dal import autocomplete  # noqa: F401
    except (ModuleNotFoundError, ImportError):
        return False

    return (
        "dal" in settings.INSTALLED_APPS and
        "dal_select2" in settings.INSTALLED_APPS
    )


@register(Tags.compatibility)
def dal_select2_system_check(app_configs, **kwargs):
    errors = []

    if not dal_select2_check_all():
        errors.append(
            Warning(
                (
                    "django-autocomplete-light is not installed or configured. "
                    "Block inventory will fall back on built-in select widgets."
                ),
                hint=(
                    "Install django-autocomplete-light and add 'dal' and"
                    "'dal_select2' to INSTALLED_APPS. "
                    "Add this check result to SILENCED_SYSTEM_CHECKS if "
                    "you do not wish to use django-autocomplete-light."
                ),
                id="wagtailinventory.W001",
            )
        )

    return errors
