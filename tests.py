import unittest as ut
from Poker import *

class PokerhandTest(ut.TestCase):
    pass

class CardValueTests(ut.TestCase):
    def testCorrectValue(self):
        self.assertTrue(card_value("4")>card_value("2"))
        self.assertEquals(card_value('A'),14)
        self.assertEquals(card_value('T'),10)

class HandValueTests(ut.TestCase):
    def testInequalities(self):
        self.assertGreater(hand_value(["5C", "QD", "2D", "AC", "9C"]), hand_value(["QC", "KD", "TD", "9C", "8C"]), msg="Unexpected inequality")
