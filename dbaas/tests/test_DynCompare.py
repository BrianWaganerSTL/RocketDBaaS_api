from django.test import TestCase

from dbaas.utils.DynCompare import DynCompare
from monitor.models import PredicateTypeChoices


class DynCompareTestCase(TestCase):
  def test_dyn_compare_LTH(self):
    self.assertTrue(DynCompare(1, PredicateTypeChoices.LTH, 2))

  def test_dyn_compare_NOT_LTH(self):
    self.assertFalse(DynCompare(2, PredicateTypeChoices.LTH, 2))

  def test_dyn_compare_LTE(self):
    self.assertTrue(DynCompare(2, PredicateTypeChoices.LTE, 2))

  def test_dyn_compare_NOT_LTE(self):
    self.assertFalse(DynCompare(3, PredicateTypeChoices.LTE, 2))

  def test_dyn_compare_GTH(self):
    self.assertTrue(DynCompare(3, PredicateTypeChoices.GTH, 2))

  def test_dyn_compare_NOT_GTH(self):
    self.assertFalse(DynCompare(2, PredicateTypeChoices.GTH, 2))

  def test_dyn_compare_GTE(self):
    self.assertTrue(DynCompare(2, PredicateTypeChoices.GTE, 2))

  def test_dyn_compare_NOT_GTE(self):
    self.assertFalse(DynCompare(1, PredicateTypeChoices.GTE, 2))

  def test_dyn_compare_EQ(self):
    self.assertTrue(DynCompare(2, PredicateTypeChoices.EQ, 2))

  def test_dyn_compare_NOT_EQ(self):
    self.assertFalse(DynCompare(1, PredicateTypeChoices.EQ, 2))

  def test_dyn_compare_NE(self):
    self.assertTrue(DynCompare(1, PredicateTypeChoices.NE, 2))

  def test_dyn_compare_NOT_NE(self):
    self.assertFalse(DynCompare(2, PredicateTypeChoices.NE, 2))
