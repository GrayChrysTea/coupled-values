#
# MIT License
#
# Copyright(c) 2020 GrayChrysTea
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files(the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and / or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

import coupledvalues as cv
import unittest

class TestPairs(unittest.TestCase):
    def test_init_pair(self):
        pair = cv.create_pair(("k1", "v2"))
        self.assertEqual(str(pair), "Pair(k1, v2)")
        self.assertEqual(pair.first, "k1")
        self.assertEqual(pair.second, "v2")
        self.assertIn("k1", pair)
        self.assertIn("v2", pair)
    
    def test_init_pair_non_unique(self):
        self.assertRaises(ValueError, cv.create_pair, ("item", "item"))
    
    def test_init_pair_with_list(self):
        pairs = cv.create_pairs_with_list([("k2", "v2"), ("k3", "v3")])
        self.assertTrue(True)
    
    def test_init_pair_with_dict(self):
        pairs = cv.create_pairs_with_dict({"k4": "v4", "k5": "v5"})
        self.assertTrue(True)
    
    def test_pair_contains(self):
        pair = cv.Pr("k6", "v6")
        self.assertIn("k6", pair)
        self.assertIn("v6", pair)
    
    def test_pair_equals(self):
        pair_a = cv.Pr("k7", "v7")
        pair_b = cv.Pr("k7", "v7")
        pair_c = cv.Pr("k7", "v6")
        self.assertEqual(pair_a, pair_b)
        self.assertNotEqual(pair_a, pair_c)
    
    def test_pair_get_other(self):
        pair = cv.Pr("k8", "v8")
        self.assertEqual(pair.other("k8"), "v8")
        self.assertEqual(pair.other("v8"), "k8")
    
    def test_pair_edit(self):
        pair = cv.Pr("k9", "v9")
        self.assertRaises(ValueError, pair.edit, "k10", "v11")
        self.assertRaises(ValueError, pair.edit, "k9", "k9")
        pair.edit("k9", "v10")
        self.assertEqual(pair.first, "k9")
        self.assertEqual(pair.second, "v10")


if __name__ == "__main__":
    unittest.main()
