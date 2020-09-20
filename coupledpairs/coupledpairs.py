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


class CoupledPair(object):
    """
    Custom Pair class. CoupledPair has special methods that allow checking for
    clashing with another pair, similarity to another pair, retrieving a value
    in the pair with its counterpart value and modifying it, giving it more
    utility and versatility. These methods are used extensively in the
    implementation of CoupledValues. To learn more, print out the docstring for
    each method with:

        >>> print(help(CoupledPair.<method name>))
    
    Example
    -------

        >>> my_pair = CoupledPair("a", "b") # This is okay
        >>> try:
        ...     another_pair = CoupledPair("c", "c") # Values cannot be the same
        ... except ValueError as e:
        ...     print(e)
        pair values cannot be the same
    
    Parameters
    ----------
    first: object
        First value in a pair. The order does not matter as both objects can be
        used as the key for its paired value
    
    second: object
        Second value in a pair. The order does not matter as both objects can be
        used as the key for its paired value
    
    Raises
    ------
    ValueError
        If first and second are the same
    
    Returns
    -------
    pair: CoupledPair
    """

    ### ~~~~~~~~~~~~~~~~~~~~~~~~~~ CREATE rud ~~~~~~~~~~~~~~~~~~~~~~~~~~ ###

    def __init__(self, first, second):
        if first == second:
            raise ValueError(f"pair values cannot be the same")
        self.first = first
        self.second = second

    ### ~~~~~~~~~~~~~~~~~~~~~~~~~~ c READ ud ~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###

    def __contains__(self, value):
        return self.has(value)

    def __eq__(self, other_pair):
        return self.is_similar_to(other_pair)

    def __repr__(self):
        return self.to_str()

    def __str__(self):
        return self.to_str()

    def clashes_with(self, other_pair):
        """
        Checks if for clashing. If two pairs clash, it means one pair has a
        value that the other pair has. This method is particularly useful for
        CoupledValues as it can be used to ensure that none of the pairs in the
        set have two similar values, preventing accessing pairs by key to be
        erroneous.

        Example
        -------

            >>> pair1 = CoupledPair("a", "b")
            >>> pair2 = CoupledPair("b", "c")
            >>> pair1.clashes_with(pair2)
            True
        
        Parameters
        ----------
        other_pair: CoupledPair
            The other pair you want to check for clashing

        Raises
        ------
        TypeError
            If other_pair is not a CoupledPair object
        
        Returns
        -------
        clashes: bool
            Whether the two pairs clash
        """
        if not isinstance(other_pair, CoupledPair):
            raise TypeError("other_pair must be an instance of CoupledPair")
        conditions = [
            self.has(other_pair.first),
            self.has(other_pair.second)
        ]
        return any(conditions)

    def counterpart(self, key):
        """
        Returns the value of one of the objects in the pair based on the value
        of the other object.

        Example
        -------

            >>> my_pair = CoupledPair("some text", 419)
            >>> my_pair.counterpart(419)
            'some text'
        
        Parameters
        ----------
        key: object
            The value of the other object
        
        Raises
        ------
        KeyError
            If key is not in the pair
        
        Returns
        -------
        counterpart: object
        """
        if key == self.first:
            return self.second
        elif key == self.second:
            return self.first
        else:
            raise KeyError(f"{key} does not exist here")

    def has(self, value):
        """
        Whether a pair has a value.

        Example
        -------

            >>> my_pair = CoupledPair("something", "more things")
            >>> my_pair.has("something")
            True
        
        Parameters
        ----------
        value: object

        Returns
        -------
        bool
        """
        conditions = [
            value == self.first,
            value == self.second
        ]
        return any(conditions)

    def is_similar_to(self, other_pair):
        """
        Whether 2 pairs have the same values.

        Example
        -------
        
            >>> pair1 = CoupledPair("a", "b")
            >>> pair2 = CoupledPair("a", "b")
            >>> pair3 = CoupledPair("b", "c")
            >>> pair1.is_similar_to(pair2)
            True
            >>> pair1.is_similar_to(pair3)
            False
        
        Parameters
        ----------
        other_pair: CoupledPair

        Raises
        ------
        TypeError
            If other_pair is not an instance of CoupledPair
        
        Returns
        -------
        bool
        """
        if not isinstance(other_pair, CoupledPair):
            raise TypeError("other_pair must be an instance of CoupledPair")
        conditions = [
            self.first == other_pair.first and self.second == other_pair.second,
            self.first == other_pair.second and self.second == other_pair.first
        ]
        return any(conditions)

    def setup_str(self):
        """
        Sets up pair values to become a string. If one of the values in the pair
        is a string type, then quotation marks are added around it. This method
        is run before converting a CoupledPair to string.

        Returns
        -------
        (first, second): tuple of values
            Values that have been set up to be converted to string
        """
        first = self.first
        second = self.second
        if type(first) == str:
            first = repr(first)
        if type(second) == str:
            second = repr(second)
        return first, second

    def to_str(self):
        """
        Convert CoupledPair to full string.

        Returns
        -------
        str
        """
        s_str = self.setup_str()
        return f"CoupledPair({s_str[0]}, {s_str[1]})"

    def to_mini_str(self):
        """
        Convert CoupledPair to short string, used by CoupledValues in its own
        to_str method.

        Returns
        -------
        str
        """
        s_str = self.setup_str()
        return f"{s_str[0]}~{s_str[1]}"

    ### ~~~~~~~~~~~~~~~~~~~~~~~~~ cr UPDATE d ~~~~~~~~~~~~~~~~~~~~~~~~~~ ###

    def modify(self, key, value):
        """
        Modify one of the values in the pair by accessing it with the value of
        the other object in the pair.

        Example
        -------

            >>> my_pair = CoupledPair("my key", "oh no this is wrong")
            >>> my_pair.modify("my key", "new value")
            >>> print(my_pair)
            CoupledPair("my key", "new value")
        
        Parameters
        ----------
        key: object
            The value of the key in the pair
        
        value: object
            The new value you want to modify the value of the pair with
        
        Raises
        ------
        KeyError
            If key is not in the pair
        
        ValueError
            If value is the same as key
        
        Returns
        -------
        None
        """
        if key == value:
            raise ValueError("key cannot be the same as value")
        if key == self.first:
            self.second = value
        elif key == self.second:
            self.first = value
        else:
            raise KeyError(f"{key} does not exist")


### ~~~~~~~~~~~~~~~~~~~~~~~~~~ GENERAL FUNCTIONS ~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###

def make_pairs(values):
    """
    Makes a list pairs from an iterable. However, different iterables have
    different behaviours when making a list of pairs.

    If you are trying to make a list of pairs from a CoupledPair,
    the CoupledPair object is wrapped in a list and returned back to you.

    If you are trying to make a list of pairs from a list or set,
    make_pairs loops through the array and forms CoupledPair objects
    recursively.

    If you are trying to make a list of pairs from a tuple,
    the CoupledPair initializer is run and the new CoupledPair object is
    returned in a list.

    If you are trying to make a list of pairs from a dict,
    the items in the dictionary are looped through and CoupledPair instances are
    created. Using a dictionary to create a list of CoupledPair objects is by far
    the safest method.

    Parameters
    ----------
    value: CoupledPair, list, set, tuple or dict

    Returns
    -------
    list of CoupledPair
    """
    if isinstance(values, CoupledPair):
        return [values]
    elif isinstance(values, list) or isinstance(values, set):
        result = []
        for value in values:
            result.extend(make_pairs(value))
        return result
    elif isinstance(values, tuple):
        return [CoupledPair(values[0], values[1])]
    elif isinstance(values, dict):
        result = []
        for key, value in values.items():
            result.append(CoupledPair(key, value))
        return result
    else:
        raise TypeError(
            "make_pairs only accepts CoupledPair, list, set, tuple or dict"
        )
