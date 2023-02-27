from unittest import mock

from django.apps import apps
from django.core.checks import Info, Warning
from django.test import TestCase, override_settings

from wagtailinventory.checks import (
    dal_installed_check,
    dal_present_check,
    dal_select2_installed_check,
    dal_select2_system_check,
)


class WagtailInventoryChecksTestCase(TestCase):
    @mock.patch.dict("sys.modules", {"dal": None})
    def test_dal_present_check_fails(self):
        self.assertFalse(dal_present_check())

    def test_dal_present_check_passes(self):
        self.assertTrue(dal_present_check())

    @override_settings(INSTALLED_APPS=[])
    def test_dal_installed_check_fails(self):
        self.assertFalse(dal_installed_check())

    def test_dal_installed_check_passes(self):
        self.assertTrue(dal_installed_check())

    @override_settings(INSTALLED_APPS=[])
    def test_dal_select2_installed_check_fails(self):
        self.assertFalse(dal_select2_installed_check())

    def test_dal_select2_installed_check_passes(self):
        self.assertTrue(dal_select2_installed_check())

    @override_settings(INSTALLED_APPS=[])
    def test_dal_select2_check_all_fails(self):
        self.assertFalse(dal_select2_installed_check())

    def test_dal_select2_check_all_passes(self):
        self.assertTrue(dal_select2_installed_check())

    def test_dal_select2_system_check_fails(self):
        with mock.patch.dict("sys.modules", {"dal": None}):
            errors = dal_select2_system_check(apps.get_app_configs())
            self.assertEqual(len(errors), 2)
            self.assertIsInstance(errors[0], Info)
            self.assertIsInstance(errors[1], Warning)
            self.assertEqual(errors[0].id, "wagtailinventory.I001")
            self.assertEqual(errors[1].id, "wagtailinventory.W001")

        with override_settings(INSTALLED_APPS=[]):
            errors = dal_select2_system_check(apps.get_app_configs())
            self.assertEqual(len(errors), 3)
            self.assertIsInstance(errors[0], Info)
            self.assertIsInstance(errors[1], Info)
            self.assertIsInstance(errors[2], Warning)
            self.assertEqual(errors[0].id, "wagtailinventory.I002")
            self.assertEqual(errors[1].id, "wagtailinventory.I003")
            self.assertEqual(errors[2].id, "wagtailinventory.W001")
