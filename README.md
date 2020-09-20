# `coupled-values.py`

## Version 1.0.0

## **Description**

`CoupledValues` are a type of Pythonic dictionaries where in each pair of 2 values in a set, one value can be referred to by using the value of its counterpart (the `key`). However, unlike dictionaries or other hash mappings, both values in the pair can be used as the `key`.

## **Installation**

To use `coupled-values.py`, download the `.tar.gz` zip file. Next, unzip with the following command:

```shell
    $mkdir coupled-values-1.x
    $tar -xvzf coupled-values.tar.gz -C coupled-values-1.x
```

Next cd into the new directory to set up the package.

```shell
    $cd coupled-values-1.x/coupled-values-1.<semver-version-number>
```

And then install by doing:

```shell
    $python3 setup.py build
    $python3 setup.py sdist
    # ^^^ Only needed if you don't intend to install package as a Python egg
    $python3 setup.py install
    $pip install dist/coupled-values-1.<semver-version-number>.tar.gz
    # ^^^ Only needed if you don't intend to install package as a Python egg
```

And you are all set!

## **Usage**

In a normal dictionary, you might, for example, be able to do this:

```python
    >>> my_dictionary = {"a": "b"}
    >>> print(my_dictionary["a"])
    'b'
    >>> print(my_dictionary["b"]) # KeyError
```

*Snippet 1*

But with `CoupledValues`, you are able to do this:

```python
    >>> my_coupledvalues = CoupledValues(init_values={"a": "b"})
    >>> print(my_coupledvalues["a"])
    'b'
    >>> print(my_coupledvalues["b"])
    'a'
```

*Snippet 2*

The implications of this is that you are not allowed to have 2 pairs that have 2 similar values in any of their constituent objects. For example, this is allowed:

```python
    >>> from string import ascii_lowercase as abc
    >>> my_dictionary = {abc[i-1]: abc[i] for i in range(1, 26, 2)}
    # {'a': 'b', 'c': 'd', 'e': 'f', ...}
    >>> my_coupledvalues = CoupledValues(init_values=my_dictionary)
    # Since all values inside the dictionary is unique, this CoupledValues set
    # is valid
```

*Snippet 3*

However, this is not allowed:

```python
    >>> my_dictionary = {"a": "b", "b": "c"}
    >>> my_coupledvalues = CoupledValues(init_values=my_dictionary)
    # ClashingError since not all values inside the dictionary are unique
```

*Snippet 4*

By preventing you from adding 2 pairs with the same values, you are able to access 2 unique values with 2 unique keys. This strict requirement for uniqueness makes `CoupledValues` like sets of tuples, but contained in a specially-made class.

With that said, many of the functionalities of dictionaries are preserved as you can use `__getitem__` and `__setitem__` to access the values inside your `CoupledValues` set, as in:

```python
    # Snippet 3
    >>> print(my_coupledvalues["a"])
    'b'
    >>> print(my_coupledvalues["z"])
    'y'
    >>> my_coupledvalues["y"] = "Z"
    >>> print(my_coupledvalues["z"]) # KeyError
    >>> print(my_coupledvalues["Z"])
    'y'
```

*Snippet 5*

In addition, other operands have been configured to allow pairs to be added to your `CoupledValues` set by doing the following:

```python
    >>> my_coupledvalues = CoupledValues(init_values=[])
    # ^^^ Initialize empty CoupledValues
    >>> my_coupledvalues += CoupledPair("a", "b") # Adding with __iadd__
    >>> my_coupledvalues << ("c", "d") # Adding with __lshift__
    >>> {"e": "f"} >> my_coupledvalues # Adding with __rrshift__
```

*Snippet 6*

As you can see, you can use 3 Python operands to push pairs into your `CoupledValues` set, but you can package your pairs into different containers to initialize or push into your `CoupledValues` set.

To remove a pair, use `CoupledValues.pop(value)` to pop the pair using one of the values in the pair, this will return a the pair's counterpart if it exists but throw `KeyError` if it does not.

## `CoupledPair`

`CoupledPair`s are custom tuples with 2 values that represent a pair. `CoupledPair`s has extra methods that tuples don't. For instance `CoupledPair`s validate your values by making sure both values inside them are not equal. Furthermore, the value of one object in the pair can be returned by using the value of its counterpart using the method `CoupledPair.counterpart(key)`. These methods go hand-in-hand with `CoupledValues` as it enables it to manipulate pairs without creating special methods inside `CoupledValues` to do so, making the source code cleaner.

When you try to add pairs into a `CoupledValues`, they must be in the form of a list of `CoupledPair`s. However, `CoupledValues` can convert any in-built iterable (e.g. list, set, dict, tuple or even another `CoupledValues` set) into a list of `CoupledPair`s by using `create_pairs(values)`.

`create_pairs` does have certain quirks, especially when used on tuples. More info can be found by executing:

```python
    >>> from coupledpairs import make_pairs
    >>> help(make_pairs)
```

## error_mode=ERROR_ON

`error_mode` is a custom setting that you can use to modify the behaviour of `CoupledValues` if an error occurs. This option is set when initializing your `CoupledValues` and the parameter `error_mode` accepts either of 2 options: `ERROR_ON` or `ERROR_OFF`. By default, `ERROR_ON` is used. The list of behaviours it can modify are as follows:

1. When accessing a pair with a key that does not exist, return `None` instead of raising `KeyError`.
2. When removing a pair with a key that does not exist, return `None` instead of raising `KeyError`.
