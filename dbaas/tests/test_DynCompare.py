from django.test import TestCase

from dbaas.utils.DynCompare import DynCompare


class DynCompareTestCase(TestCase):
  def test_dyn_compare_lth(self):
    self.assertTrue(DynCompare(1, '<', 2))
