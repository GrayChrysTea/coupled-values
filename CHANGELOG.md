# `coupled-values.py` Changelog

## 0.0.1

1. Implement `BaseCoupledValues` class with basic underlying functions.
2. Implement basic custom error types.
    - `CoupledValuesError`: Base Error, inherits from `Exception`.
    - `AlreadyInCoupledValuesError`: When a pair, or a part of the pair is
        already in a `CoupledValues` object.
3. Implement pairs (`Pair`)

## 0.1.0-rc1

1. Find the value of one partner in a pair with the value of its counterpart.
2. Check whether a `CoupledValues` is a subset of another `CoupledValues`
    object.

## 0.1.0-rc2

1. Update the value of one partner in a pair with the value of its counterpart.
2. Check whether two `CoupledValues` objects are equal to each other.
