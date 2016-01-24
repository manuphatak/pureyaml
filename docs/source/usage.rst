.. highlight:: python

=====
Usage
=====

To use pureyaml in a project::

    import pureyaml

    >>> import pureyaml
    >>> from textwrap import dedent
    >>> from pprint import pprint
    >>> text = dedent("""
    ...     marvel:
    ...     - iron man
    ...     - the hulk
    ...     - captain america
    ...     dc:
    ...     - batman
    ...     - the joker
    ...     - superman
    ... """)[1:]

    >>> pprint(pureyaml.load(text))
    {'dc': ['batman', 'the joker', 'superman'],
     'marvel': ['iron man', 'the hulk', 'captain america']}

    >>> print(pureyaml.dump(pureyaml.load(text)))
    dc:
    - batman
    - the joker
    - superman
    marvel:
    - iron man
    - the hulk
    - captain america
