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


from coupledpairs import *
from coupledvalues.constants import *
from coupledvalues.coupledvalues.basecoupledvalues import BaseCoupledValues
from coupledvalues.errors import *

__all__ = [
    "create_pairs",
    "CoupledValues"
]


def create_pairs(values):
    """
    Functions like make_pairs but also accepts BaseCoupledValues and its
    descendents.

    For more information, do:

        >>> print(help(coupledpairs.make_pairs))

    Parameters
    ----------
    value: CoupledPair, list, set, tuple or dict, BaseCoupledValues

    Returns
    -------
    list of CoupledPair
    """
    if type(values) in {CoupledPair, list, set, tuple, dict}:
        return make_pairs(values)
    elif isinstance(values, BaseCoupledValues):
        return list(values._pairs)
    else:
        raise TypeError(
            "values must be an instance of BaseCoupledValues, CoupledPairs, "
            + "list, tuple or dict"
        )


class CoupledValues(BaseCoupledValues):
    """
    A set of CoupledPair objects with extra functionality.

    Example
    -------

        >>> my_cv = CoupledValues({"a": "b", "c": "d"}, error_mode=ERROR_ON)

    Parameters
    ----------
    init_values: CoupledPair, list, set, tuple or dict, BaseCoupledValues

    error_mode: str = ERROR_ON
        Whether to show error or a placeholder value when running certain
        methods. The only accepted values are:
            coupledvalues.ERROR_ON,
            coupledvalues.ERROR_OFF

    Raises
    ------
    TypeError
        If init_value is not an instance of any of the classes specified under
        Parameters
    
    ValueError
        If error_mode is not coupledvalues.ERROR_ON or coupledvalues.ERROR_OFF
    
    Returns
    -------
    CoupledValues
    """

    ### ~~~~~~~~~~~~~~~~~~~~~~~~~~ CREATE rud ~~~~~~~~~~~~~~~~~~~~~~~~~~ ###

    def __init__(
        self,
        init_values=[],
        error_mode=ERROR_ON
    ):
        super().__init__(error_mode=error_mode)
        self._push_pairs(create_pairs(init_values))

    # - ## ~~~~~~~~~~~~~~~~~ TEMPORARY PUSH SECTION ~~~~~~~~~~~~~~~~~ ##

    def __add__(self, pairs):
        return self.temporary_push(pairs)

    def __radd__(self, pairs):
        return self.temporary_push(pairs)

    def temporary_push(self, pairs):
        """
        Makes a new CoupledValues object with self and another valid set of
        pairs acceptable to create_pairs.
        
        Parameters
        ----------
        pairs: CoupledPair, list, set, tuple or dict, BaseCoupledValues

        Raises
        ------
        ClashingError
            If two of the pairs clash

        Returns
        -------
        new_cv: CoupledValues
        """
        new_cv = CoupledValues()
        new_cv._push_pairs(create_pairs(self))
        new_cv._push_pairs(create_pairs(pairs))
        return new_cv

    # - ## ~~~~~~~~~~~~~~~~~ PERMANENT PUSH SECTION ~~~~~~~~~~~~~~~~~ ##

    def __iadd__(self, pairs):
        self.push(pairs)
        return self

    def __lshift__(self, pairs):
        self.push(pairs)
        return self

    def __rrshift__(self, pairs):
        self.push(pairs)
        return self

    def push(self, pairs):
        """
        Push new pairs into the set.

        Parameters
        ----------
        pairs: CoupledPair, list, set, tuple or dict, BaseCoupledValues

        Raises
        ------
        ClashingError
            If two of the pairs clash

        Returns
        -------
        None
        """
        self._push_pairs(create_pairs(pairs))
        return None

    ### ~~~~~~~~~~~~~~~~~~~~~~~~~~ c READ ud ~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###

    def __contains__(self, key):
        return self.contains(key)

    def __getitem__(self, key):
        return self.get_value(key)

    def __repr__(self):
        return self.to_str()

    def __str__(self):
        return self.to_str()

    def contains(self, key):
        """
        Checks if a key is in one of the pairs in the CoupledValues object.

        Parameters
        ----------
        key: object

        Returns
        -------
        exists: bool
        """
        return self._contains(key)

    def get_value(self, key):
        """
        Get the value of one of the items in a pair with the value of its
        counterpart.

        Example
        -------

            >>> alphabet = "abcdefghijklmnopqrstuvwxyz"
            >>> my_dict = {alphabet[i]: alphabet[i+1] for i in range(0, 25, 2)}
                # Odd letters are paired with even letters
                # i.e. 'a' ~ 'b', 'c' ~ 'd', ...
            >>> my_cv = CoupledValues(my_dict)
            >>> print(my_cv.get_value("b"))
            'a'
        
        Parameters
        ----------
        key: object

        Raises
        ------
        KeyError
            If the key does not exist in the set and error_mode is ERROR_ON
        
        Returns
        -------
        value: object
        """
        pair = self._get_pair(key)
        if pair is None:
            return None
        return pair.counterpart(key)

    def to_str(self):
        """
        Converts CoupledValues to string.

        Returns
        -------
        string
        """
        string = "CoupledValues(["
        for pair in self._pairs:
            string += pair.to_mini_str() + ", "
        string = string[:-2]
        string += "])"
        return string

    ### ~~~~~~~~~~~~~~~~~~~~~~~~~ cr UPDATE d ~~~~~~~~~~~~~~~~~~~~~~~~~~ ###

    def __setitem__(self, key, value):
        self.update(key, value)
        return None

    def update(self, key, value):
        """
        Update a value of one of the pairs with its key. See CoupledPair.modify
        for more information.

        Parameters
        ----------
        key: object
        
        value: object

        Raises
        ------
        KeyError
            If the key does not exist

        ValueError
            If key == value
        
        Returns
        -------
        None
        """
        self._add_or_update(key, value)
        return None

    ### ~~~~~~~~~~~~~~~~~~~~~~~~~~ cru DELETE ~~~~~~~~~~~~~~~~~~~~~~~~~~ ###

    def clear(self):
        """
        Clears the entire set.

        Returns
        -------
        None
        """
        self._clear()

    def pop(self, key):
        """
        Pops one of the pairs by key and return its value.

        Parameters
        ----------
        key: object

        Raises
        ------
        KeyError
            If key does not exist and error_mode is ERROR_ON
        
        Returns
        -------
        value: object
            Popped value, None if key not found and error_mode is ERROR_OFF
        """
        return self._remove_and_get_counterpart(key)
