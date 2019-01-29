from django_test import TestCase

from dbaas.utils.DynCompare import DynCompare


# from django.test import TestCase


class DynCompareTestCase(TestCase):
  def test_dyn_compare_lth(self):
    self.assertTrue(DynCompare(1, '<', 2))
