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

from ..errors import *
from .auxes import *
from ..pairs import *

class BaseCoupledValues(object):
    """
    CoupledValues interface class

    All CoupledValues classes are derived from this class.

    Parameters
    ----------
    None

    Attributes
    ----------
    _pairs : list
        All the pairs this coupled values object has
    """
    def __init__(self):
        self._pairs = []

    
    def __str__(self):
        return f"coupledvalues.BaseCoupledValues({self._pairs})"
    

    def __repr__(self):
        return f"coupledvalues.BaseCoupledValues({self._pairs})"


    def _get_firsts(self):
        return [pair.first for pair in self._pairs]
    

    def _enumerate_get_firsts(self):
        for index in range(len(self._pairs)):
            yield index, self._pairs[index].first
    
    
    def _enumerate_get_seconds(self):
        for index in range(len(self._pairs)):
            yield index, self._pairs[index].second
    

    def _get_seconds(self):
        return [pair.second for pair in self._pairs]
    

    def _combine_firsts_and_seconds(self, intersperse=True):
        if intersperse:
            return self._intersperse_pair_values()
        else:
            return self._separate_pair_values()


    def _intersperse_pair_values(self):
        result = []
        for pair in self._pairs:
            result.append(pair.first)
            result.append(pair.second)
        return result


    def _separate_pair_values(self):
        return self._get_firsts() + self._get_seconds()


    def _find_index_with_first(self, first, show_error=True):
        firsts = self._get_firsts()
        try:
            index = firsts.index(first)
        except ValueError as e:
            if not show_error:
                return -1
            raise ValueError(f"{first} does not exist")
        else:
            return index


    def _find_index_with_second(self, second, show_error=True):
        seconds = self._get_seconds()
        try:
            index = seconds.index(second)
        except ValueError as e:
            if not show_error:
                return -1
            raise ValueError(f"{second} does not exist")
        else:
            return index

    
    def _find_index_with_single(self, single_value, show_error=True):
        for index in range(len(self._pairs)):
            if self._pairs[index].has(single_value):
                return index
        if show_error:
            raise ValueError(f"{single_value} does not exist")
        else:
            return -1
    

    def _find_index_with_pair(self, pair, show_error=False):
        for index in range(len(self._pairs)):
            if self._pairs[index].is_similar_to(pair):
                return True
        if show_error:
            raise ValueError(f"{pair} does not exist")
        else:
            return -1
    

    def _get_pair_with_first(self, first, show_error=True):
        index = self._find_index_with_first(first=first, show_error=show_error)
        if index == -1:
            return None
        else:
            return self._pairs[index]
    

    def _get_pair_with_second(self, second, show_error=True):
        index = self._find_index_with_second(
            second=second,
            show_error=show_error
        )
        if index == -1:
            return None
        else:
            return self._pairs[index]
    

    def _get_pair_with_single(self, single_value, show_error=True):
        index = self._find_index_with_single(
            single_value=single_value,
            show_error=show_error
        )
        if index == -1:
            return None
        else:
            return self._pairs[index]
    

    def _has(self, other_pair):
        for pair in self._pairs:
            if other_pair.is_similar_to(pair):
                return True
        return False
    

    def _is_subset_of(self, coupled_values):
        for pair in self._pairs:
            if not coupled_values._has(pair):
                return False
        return True
    

    def _is_similar_to(self, coupled_values):
        return all(
            [
                self._is_subset_of(coupled_values),
                coupled_values._is_subset_of(self)
            ]
        )
    

    def _update_pair(self, index, pair):
        self._pairs[index] = pair
    

    def _append_pair(self, pair):
        self._pairs.append(pair)

    
    def _append_or_update_pair(self, pair):
        index = self._find_index_with_single(
            single_value=pair.first,
            show_error=False
        )
        if index != -1:
            self._update_pair(index, pair)
            return None
        index = self._find_index_with_single(
            single_value=pair.second,
            show_error=False
        )
        if index != -1:
            self._update_pair(index, pair)
            return None
        self._append_pair(pair)

    
    def _strict_append_values(self, pairs=[], ignore_typing=False):
        temp_coupled_values = BaseCoupledValues()
        temp_coupled_values_pairs = []
        temp_coupled_values_pairs.extend(self._pairs)
        temp_coupled_values._pairs = temp_coupled_values_pairs
        if type(pairs) not in (list, tuple):
            raise TypeError(
                "pairs must be in a list or tuple when you use "
                + "self._strict_append_values"
            )
        for pair in pairs:
            if type(pair) != Pair:
                if ignore_typing:
                    continue
                raise TypeError(
                    "each pair in the list must be encapsulated as a "
                        + "coupledvalues.Pair"
                )
            if temp_coupled_values._contains(pair.first):
                raise AlreadyInCoupledValuesError(
                    f"your coupled values already has {pair.first}"
                )
            if temp_coupled_values._contains(pair.second):
                raise AlreadyInCoupledValuesError(
                    f"your coupled values already has {pair.second}"
                )
            temp_coupled_values._pairs.append(pair)
        self._pairs = temp_coupled_values._pairs
        del temp_coupled_values


    def _lenient_append_values(self, pairs=[], ignore_typing=False):
        temp_coupled_values = BaseCoupledValues()
        temp_coupled_values_pairs = []
        temp_coupled_values_pairs.extend(self._pairs)
        temp_coupled_values._pairs = temp_coupled_values_pairs
        if type(pairs) not in (list, tuple):
            raise TypeError(
                "pairs must be in a list or tuple when you use "
                + "self._lenient_append_values"
            )
        for pair in pairs:
            if type(pair) != Pair:
                if ignore_typing:
                    continue
                raise TypeError(
                    "each pair in the list must be encapsulated as a tuple."
                )
            if temp_coupled_values._contains(pair.first):
                index = temp_coupled_values._find_index_with_first(
                    first=pair.first, show_error=False
                )
                self._pairs[index] = pair
                continue
            if temp_coupled_values._contains(pair.second):
                index = temp_coupled_values._find_index_with_second(
                    second=pair.second, show_error=False
                )
                self._pairs[index] = pair
                continue
            temp_coupled_values._pairs.append(pair)
        self._pairs = temp_coupled_values._pairs
        del temp_coupled_values


    def _append_values(
            self,
            pairs=[],
            replace=False,
            ignore_typing=False
        ):
        if type(pairs) != list:
            raise TypeError(
                "pairs must be a list when you use "
                + "self._append_values"
            )
        if replace:
            self._lenient_append_values(pairs=pairs)
        else:
            self._strict_append_values(pairs=pairs)


    def _initialize_values(
            self,
            initial_values=[],
            replace=False,
            ignore_typing=False
        ):
        if type(initial_values) != list:
            raise TypeError(
                "initial_values must be a list when you use "
                    + "self._initialize_values"
            )
        self._pairs = []
        self._append_values(
            pairs=initial_values,
            replace=replace,
            ignore_typing=ignore_typing
        )
    

    def _pop_with_single(self, single_value):
        index = self._find_index_with_single(single_value)
        return self._pairs.pop(index)
    

    def _pop_with_pair(self, pair):
        return self._pairs.remove(pair)

    
    def _contains(self, value):
        if type(value) == Pair:
            return self._has(value)
        else:
            index = self._find_index_with_single(
                single_value=value,
                show_error=False
            )
            if index == -1:
                return False
            return True
