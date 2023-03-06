from unittest import mock

from django.apps import apps
from django.core.checks import Warning
from django.test import TestCase, override_settings

from wagtailinventory.checks import (
    dal_select2_check_all,
    dal_select2_system_check,
)


class WagtailInventoryChecksTestCase(TestCase):
    @mock.patch.dict("sys.modules", {"dal": None})
    def test_dal_select2_check_all_fails_on_import(self):
        self.assertFalse(dal_select2_check_all())

    @override_settings(
        INSTALLED_APPS=[
            "dal_select2",
        ]
    )
    def test_dal_select2_check_all_fails_on_dal_installed(self):
        self.assertFalse(dal_select2_check_all())

    @override_settings(
        INSTALLED_APPS=[
            "dal",
        ]
    )
    def test_dal_select2_check_all_fails_on_select2_installed(self):
        self.assertFalse(dal_select2_check_all())

    def test_dal_select2_check_all_passes(self):
        self.assertTrue(dal_select2_check_all())

    def test_dal_select2_system_check_fails(self):
        with mock.patch.dict("sys.modules", {"dal": None}):
            errors = dal_select2_system_check(apps.get_app_configs())
            self.assertEqual(len(errors), 1)
            self.assertIsInstance(errors[0], Warning)
            self.assertEqual(errors[0].id, "wagtailinventory.W001")

        with override_settings(INSTALLED_APPS=[]):
            errors = dal_select2_system_check(apps.get_app_configs())
            self.assertEqual(len(errors), 1)
            self.assertIsInstance(errors[0], Warning)
            self.assertEqual(errors[0].id, "wagtailinventory.W001")
