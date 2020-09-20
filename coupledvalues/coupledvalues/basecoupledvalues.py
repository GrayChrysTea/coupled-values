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
from coupledvalues.errors import *


class BaseCoupledValues(object):
    """
    Base CoupledValues class. All CoupledValues implementations are inherited
    from this class.
    """

    ### ~~~~~~~~~~~~~~~~~~~~~~~~~~ CREATE rud ~~~~~~~~~~~~~~~~~~~~~~~~~~ ###

    def __init__(self, error_mode=ERROR_ON):
        if error_mode not in {ERROR_OFF, ERROR_ON}:
            raise ValueError("error_mode must be ERROR_ON or ERROR_OFF")
        self._pairs = []
        self._error_mode = error_mode

    def _push_pair(self, pair):
        if self._clashes(pair):
            raise ClashingError(
                f"{pair} clashes with another pair in the set"
            )
        self._pairs.append(pair)
        return None

    def _push_pairs(self, pairs):
        for pair in pairs:
            self._push_pair(pair)
        return None

    ### ~~~~~~~~~~~~~~~~~~~~~~~~~~ c READ ud ~~~~~~~~~~~~~~~~~~~~~~~~~~~ ###

    def _contains(self, key):
        for pair in self._pairs:
            if pair.has(key):
                return True
        return False

    def _get_pair(self, key):
        for pair in self._pairs:
            if pair.has(key):
                return pair
        if self._error_mode == ERROR_ON:
            raise KeyError(f"{key} does not exist in the set")
        else:
            return None

    def _has(self, pair):
        for existing_pair in self._pairs:
            if existing_pair.is_similar_to(pair):
                return True
        return False

    def _iterate_pairs(self):
        for pair in self._pairs:
            yield pair

    def _iterate_values(self):
        for pair in self._pairs:
            yield pair.first, pair.second

    # - ## ~~~~~~~~~~~~~~~~~~~ VALIDATION SECTION ~~~~~~~~~~~~~~~~~~~ ##

    def _clashes(self, pair):
        if self._has(pair):
            return True
        for existing_pair in self._pairs:
            if pair.clashes_with(existing_pair):
                return True
        return False

    def _validate_all(self):
        for pair in self._pairs:
            if self._clashes(pair):
                return False
        return True

    ### ~~~~~~~~~~~~~~~~~~~~~~~~~ cr UPDATE d ~~~~~~~~~~~~~~~~~~~~~~~~~~ ###

    def _update(self, key, value):
        if key == value:
            raise ValueError(f"key cannot be the same as value")
        pair = self._get_pair(key)
        if pair is None:
            raise KeyError(f"{key} does not exist")
        if self._contains(value):
            raise ClashingError(f"{value} is already in the set.")
        pair.modify(key, value)
        return None

    def _add_or_update(self, key, value):
        new_pair = CoupledPair(key, value)
        if self._clashes(new_pair):
            self._update(key, value)
        else:
            self._push_pair(new_pair)

    ### ~~~~~~~~~~~~~~~~~~~~~~~~~~ cru DELETE ~~~~~~~~~~~~~~~~~~~~~~~~~~ ###

    def _remove_and_get_pair(self, key):
        for pair in self._pairs:
            if pair.has(key):
                old_pair = pair
                self._pairs.remove(pair)
                return old_pair
        if self._error_mode == ERROR_ON:
            raise KeyError(f"{key} does not exist in the set")
        else:
            return None

    def _remove_and_get_counterpart(self, key):
        for pair in self._pairs:
            if pair.has(key):
                old_value = pair.counterpart(key)
                self._pairs.remove(pair)
                return old_value
        if self._error_mode == ERROR_ON:
            raise KeyError(f"{key} does not exist in the set")
        else:
            return None

    def _clear(self):
        self._pairs.clear()
        return None
