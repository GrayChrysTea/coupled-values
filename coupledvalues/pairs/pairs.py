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

def create_pair(pair):
    """
    Create a Pair with a tuple or list with at least 2 values.

    Parameters
    ----------
    pair : tuple or list
        Pair, must have at least 2 values. The pair created will consist of the
        first 2 items in the tuple or list
    
    Raises
    ------
    IndexError
        If pair doesn't have at least 2 items
    
    Returns
    -------
    Pair
        Pair object
    """
    return Pair(pair[0], pair[1])


def create_pairs_with_list(list_of_pairs):
    """
    Create pairs from a list or tuple of array-like objects with at least 2
    items in each object

    Parameters
    ----------
    list_of_pairs : list or tuple of list or tuple
    
    Raises
    ------
    IndexError
        If pair doesn't have at least 2 items
    
    TypeError
        If list_of_pairs is not a list or tuple
    
    Returns
    -------
    list of Pair
    """
    return [
        Pair(pair[0], pair[1])
        for pair in list_of_pairs
    ]


def create_pairs_with_dict(dict_of_pairs):
    """
    Create pairs from a dictionary.

    Parameters
    ----------
    dict_of_pairs : dict
        The keys and values need not be unique when using create_pairs_with_dict
        but when you initialize a new CoupledValues object, you need to make
        sure that all values are unique
    
    Raises
    ------
    IndexError
        If pair doesn't have at least 2 items
    
    TypeError
        If list_of_pairs is not a dictionary
    
    Returns
    -------
    list of Pair
    """
    return [
        Pair(key, value)
        for key, value in dict_of_pairs.items()
    ]


def create_pairs(pairs):
    """
    Compiled function for creating a list of Pairs. This function will create
    the list of pairs depending on the datatype of the argument passed to
    the parameter called `pairs`.

    Parameters
    ----------
    pairs : tuple or list of tuple or dict

    Raises
    ------
    TypeError
        If pairs is not a tuple, list or dict
    
    Returns
    -------
    list of pairs
    """
    if type(pairs) == tuple:
        return [create_pair(tuple)]
    elif type(pairs) == list:
        return create_pairs_with_list(pairs)
    elif type(pairs) == dict:
        return create_pairs_with_dict(pairs)
    else:
        raise TypeError("pairs must be encapsulated in a tuple, list or dict")


class Pair(object):
    """
    Pair object
    """
    def __init__(self, first, second):
        if first == second:
            raise ValueError("first and second must be unique")
        self.first, self.second = first, second

    
    def has(self, value):
        return value == self.first or value == self.second

    
    def is_similar_to(self, pair):
        if (
            pair.first == self.first and pair.second == self.second or
            pair.second == self.first and pair.first == self.second
            ):
            return True
        

    def __eq__(self, pair):
        return self.is_similar_to(pair)

    
    def __contains__(self, value):
        return self.has(value)
    

    def __str__(self):
        return f"Pair({self.first}, {self.second})"
    

    def __repr__(self):
        return f"Pair({self.first}, {self.second})"
    

    def other(self, key):
        if key == self.first:
            return self.second
        elif key == self.second:
            return self.first
        raise ValueError(f"this pair does not have {key}")


    def edit(self, key, value):
        if not self.has(key):
            raise ValueError(f"this pair does not have {key}")
        if value == key:
            raise ValueError(f"value cannot be equal to key")
        if key == self.first:
            self.second = value
        else:
            self.first = value
