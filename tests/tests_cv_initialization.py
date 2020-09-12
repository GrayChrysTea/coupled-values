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

class TestCVInitialization(unittest.TestCase):
    def test_init_empty_cv(self):
        test_coupledvalues = cv.Cv()
        self.assertEqual(len(test_coupledvalues), 0)
        self.assertEqual(str(test_coupledvalues), "CoupledValues([])")
        self.assertFalse("test key" in test_coupledvalues)
    
    def test_init_cv_with_tuple(self):
        test_coupledvalues_tuple = cv.Cv(("k1", "v1"))
        self.assertEqual(len(test_coupledvalues_tuple), 1)
        self.assertEqual(
            str(test_coupledvalues_tuple),
            "CoupledValues([ k1 ~ v1, ])"
        )
        self.assertTrue("k1" in test_coupledvalues_tuple)
        self.assertTrue("v1" in test_coupledvalues_tuple)
        self.assertTrue(cv.Pr("k1", "v1") in test_coupledvalues_tuple)
        self.assertFalse("k2" in test_coupledvalues_tuple)
    
    def test_init_cv_with_pair(self):
        test_coupledvalues_pair = cv.Cv(cv.Pr("k2", "v2"))
        self.assertEqual(len(test_coupledvalues_pair), 1)
        self.assertEqual(
            str(test_coupledvalues_pair),
            "CoupledValues([ k2 ~ v2, ])"
        )
        self.assertTrue("k2" in test_coupledvalues_pair)
        self.assertTrue("v2" in test_coupledvalues_pair)
        self.assertTrue(cv.Pr("k2", "v2") in test_coupledvalues_pair)
        self.assertFalse("k3" in test_coupledvalues_pair)
    
    def test_init_cv_with_list_of_tuples(self):
        test_coupledvalues_tuple = cv.Cv(
            cv.Cp([("k3", "v3"), ("k4", "v4")])
        )
        self.assertEqual(len(test_coupledvalues_tuple), 2)
        self.assertEqual(
            str(test_coupledvalues_tuple),
            "CoupledValues([ k3 ~ v3, k4 ~ v4, ])"
        )
        self.assertTrue("k3" in test_coupledvalues_tuple)
        self.assertTrue("v4" in test_coupledvalues_tuple)
        self.assertTrue(cv.Pr("k4", "v4") in test_coupledvalues_tuple)
        self.assertFalse("k2" in test_coupledvalues_tuple)
    
    def test_init_cv_with_list_of_pairs(self):
        test_coupledvalues_tuple = cv.Cv([cv.Pr("k3", "v3"), cv.Pr("k4", "v4")])
        self.assertEqual(len(test_coupledvalues_tuple), 2)
        self.assertEqual(
            str(test_coupledvalues_tuple),
            "CoupledValues([ k3 ~ v3, k4 ~ v4, ])"
        )
        self.assertTrue("k3" in test_coupledvalues_tuple)
        self.assertTrue("v4" in test_coupledvalues_tuple)
        self.assertTrue(cv.Pr("k4", "v4") in test_coupledvalues_tuple)
        self.assertFalse("k2" in test_coupledvalues_tuple)
    
    def test_init_cv_with_dict(self):
        test_coupledvalues_tuple = cv.Cv({"k5": "v5"})
        self.assertEqual(len(test_coupledvalues_tuple), 1)
        self.assertEqual(
            str(test_coupledvalues_tuple),
            "CoupledValues([ k5 ~ v5, ])"
        )
        self.assertTrue("k5" in test_coupledvalues_tuple)
        self.assertTrue("v5" in test_coupledvalues_tuple)
        self.assertTrue(cv.Pr("k5", "v5") in test_coupledvalues_tuple)
        self.assertFalse("k2" in test_coupledvalues_tuple)
    
    def test_init_cv_with_non_unique_tuple(self):
        self.assertRaises(ValueError, cv.Cv, ("k6", "k6"))
    
    def test_init_cv_with_non_unique_list_of_tuples(self):
        self.assertRaises(
            cv.AlreadyInCoupledValuesError,
            cv.Cv,
            cv.Cp([("k6", "v6"), ("k7", "v6")])
        )

    def test_init_cv_with_non_unique_list_of_pairs(self):
        self.assertRaises(
            cv.AlreadyInCoupledValuesError,
            cv.Cv,
            [cv.Pr("k6", "v6"), cv.Pr("k7", "v6")]
        )
    
    def test_init_cv_with_non_unique_dict(self):
        self.assertRaises(
            cv.AlreadyInCoupledValuesError,
            cv.Cv,
            {"k6": "v6", "k7": "v6"}
        )


if __name__ == "__main__":
    unittest.main()
