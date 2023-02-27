from django.conf import settings
from django.core.checks import Info, Tags, Warning, register


def dal_present_check():
    """Check that the django-autocomplete-light package is installed"""
    try:
        from dal import autocomplete  # noqa: F401
    except (ModuleNotFoundError, ImportError):
        return False

    return True


def dal_installed_check():
    """Check that the dal Django app is in INSTALLED_APPS"""
    try:
        assert "dal" in settings.INSTALLED_APPS
    except AssertionError:
        return False

    return True


def dal_select2_installed_check():
    """Check that the dal_select2 Django app is in INSTALLED_APPS"""
    try:
        assert "dal_select2" in settings.INSTALLED_APPS
    except AssertionError:
        return False

    return True


def dal_select2_check_all():
    """Ensure django-autocomplete-light is usable with all the above"""
    return (
        dal_present_check()
        and dal_installed_check()
        and dal_select2_installed_check()
    )


@register(Tags.compatibility)
def dal_select2_system_check(app_configs, **kwargs):
    errors = []

    if not dal_present_check():
        errors.append(
            Info(
                "Could not import django-autocomplete-light autocomplete",
                hint="Is the package installed?",
                id="wagtailinventory.I001",
            )
        )

    if not dal_installed_check():
        errors.append(
            Info(
                "django-autocomplete-lite is not in INSTALLED_APPS",
                hint="Add 'dal' to INSTALLED_APPS",
                id="wagtailinventory.I002",
            )
        )

    if not dal_select2_installed_check():
        errors.append(
            Info(
                "django-autocomplete-lite's Select2 is not in INSTALLED_APPS",
                hint="Add 'dal_select2' to INSTALLED_APPS",
                id="wagtailinventory.I003",
            )
        )

    if len(errors) > 0:
        errors.append(
            Warning(
                (
                    "django-autocomplete-lite is not installed or configured. "
                    "Block inventory will fall back on built-in select widgets."
                ),
                hint=(
                    "Install django-autocomplete-light and add 'dal' and"
                    "'dal_select2' to INSTALLED_APPS. "
                    "Add these check results to SILENCED_SYSTEM_CHECKS if "
                    "you do not wish to use django-autocomplete-light."
                ),
                id="wagtailinventory.W001",
            )
        )

    return errors
