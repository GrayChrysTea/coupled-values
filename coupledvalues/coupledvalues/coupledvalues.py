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

from .base import BaseCoupledValues
from ..errors import *
from ..pairs import *

class CoupledValues(BaseCoupledValues):
    """
    CoupledValues interface class

    All CoupledValues classes are derived from this class.

    Parameters
    ----------
    initial_values=[] : list, dict, pair or tuple
        Pairs that you would like to initialize the coupled-values with.
        Your initial values must be packaged as a
        1. list of tuples or pairs,
        2. dictionary, or
        3. tuple with 2 values,
        4. or a Pair.
    
    ignore_typing=False : bool
        Whether to ignore erroneous input during introduction of a series of
        new pairs
    
    Raises
    ------
    AlreadyInCoupledValuesError
        If you try to add a pair where one of its values already exist in
        self._pairs

    TypeError
        If you pass a wrong type in

    Attributes
    ----------
    _pairs : list
        All the pairs this coupled values object has
    
    pairs : list
        All the pairs this coupled values object has
    """
    def __init__(self, initial_values=[], ignore_typing=False):
        super().__init__()
        self.ignore_typing = ignore_typing
        if type(initial_values) == list:
            self._initialize_values(initial_values, ignore_typing)
        elif type(initial_values) == dict:
            self._initialize_values(
                create_pairs_with_dict(initial_values),
                ignore_typing
            )
        elif isinstance(initial_values, BaseCoupledValues):
            temp_pairs = []
            temp_pairs.extend(initial_values._pairs)
            self._append_more_pairs(temp_pairs)
        elif type(initial_values) == Pair:
            self._append_pair(initial_values)
        elif type(initial_values) == tuple:
            self._append_pair(Pair(initial_values[0], initial_values[1]))
        else:
            raise TypeError(
                "initial_values must be a list, dict, tuple or coupledvalues.pair"
            )
    

    def _append_more_pairs(self, pairs):
        if type(pairs) == list:
            self._append_values(
                pairs=pairs,
                replace=False,
                ignore_typing=self.ignore_typing
            )
        elif type(pairs) == dict:
            self._append_values(
                pairs=create_pairs_with_dict(pairs),
                replace=False,
                ignore_typing=self.ignore_typing
            )
        elif isinstance(pairs, BaseCoupledValues):
            self._append_values(
                pairs=pairs._pairs,
                replace=False,
                ignore_typing=self.ignore_typing
            )
        elif type(pairs) == Pair:
            self._append_values(
                pairs=[pairs],
                replace=False,
                ignore_typing=self.ignore_typing
            )
        elif type(pairs) == tuple:
            self._append_values(
                pairs=[Pair(pairs[0], pairs[1])],
                replace=False,
                ignore_typing=self.ignore_typing
            )
        else:
            raise TypeError(
                "pair must be a list, dictionary, tuple or coupledvalues.pair"
            )
    

    def __contains__(self, value):
        return self._contains(value)
    

    def __len__(self):
        return len(self._pairs)


    def __add__(self, pairs):
        new_coupled_values = CoupledValues(
            initial_values=self._pairs,
            ignore_typing=False
        )
        new_coupled_values._append_more_pairs(pairs)
        return new_coupled_values


    def __iadd__(self, pairs):
        self._append_more_pairs(pairs)
    

    def __lshift__(self, pairs):
        self._append_more_pairs(pairs)
    

    def __rrshift__(self, pairs):
        self._append_more_pairs(pairs)
    

    def __nonzero__(self):
        return len(self._pairs) > 0
    

    def __eq__(self, other_coupled_values):
        return self._is_similar_to(other_coupled_values)
    

    def __str__(self):
        if len(self._pairs) == 0:
            return "CoupledValues([])"
        output = "CoupledValues([ "
        for pair in self._pairs:
            output += f"{str(pair.first)} ~ {str(pair.second)}, "
        output += "])"
        return output
    

    def __repr__(self):
        return str(self)
    

    def __getitem__(self, key):
        pair = self._get_pair_with_single(key)
        if key == pair.first:
            return pair.second
        else:
            return pair.first
    

    def __setitem__(self, key, value):
        pair = Pair(key, value)
        self._append_or_update_pair(pair)
    

    @property
    def pairs(self):
        return self._pairs
    

    def pop(self, key):
        """
        Pops pairs out with a key to the pair

        Parameters
        ----------
        key
            Key to the pair, can be the first item or second item of the pair
        
        Raises
        ------
        ValueError
            If the key doesn't exist
        
        Returns
        -------
        counterpart
            The counterpart of the key to the pair that has been popped off
        """
        pair = self._pop_with_single(key)
        if key == pair.first:
            return pair.second
        else:
            return pair.first
