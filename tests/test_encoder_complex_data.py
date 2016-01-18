#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import

from textwrap import dedent

from future.utils import PY2

import pureyaml
from tests.utils import PY34, PY35


def dump(data):
    text = pureyaml.dump(data)
    # print('\n' + text)
    return text


def test_dump__travis_yaml(tmpdir):
    """:type tmpdir: py._path.local.LocalPath"""
    # noinspection SpellCheckingInspection
    secure_block = (  # :off
        'ndFpfTvPZN8SfvduvS4567k1TqYl7L7lRxxEPjmRzg3OgzMgCHRMO/uCrce5i8TkxTWL'
        'W82ArNvBZnTkRzGyChKfoNzKwukgrJACOibc6cPgNBPpuDpZTb7X6hZixSs9VBsMwL9T'
        'kQfImq3Q2uSnW7tBrHYKEIOXeCmKzomI3RYxWoxOlrAP7TqUjxyw/Ax5pOdjODDEMOjB'
        'Z8qRcrRD/n/JyAQrNVtaEaMkauTPbvJ86vG8mDPLzD3c2PFK1qAOimcJb5izM9y9kent'
        '/muLfjeruBxwYGrqAkQnWM0KUqMbfZ9sxMO0hgMZs3p2fldTyANC9bRu65XLW3qseHs9'
        'NTbbdgAZMlsXU9WxzvxTyibvMGHODyps/Ra9NkgRZJC9NLsabuw42P3AVfQjhih/dwn0'
        'DjRU+DlNyY291CazPjSWP4hLBAp72hhv1sGQD33sY3ERx5XPXyeb1B32s3l94bpdPwzO'
        'Hf3MIHAs4Uj32mToi0699lp749PQ4o0Jb2WF0P8vh+vlOJNVM+51vO5CmEj2cF7rJcrb'
        'n+T68gmlvqcYCt3q5gCn+4iBhzGCqeDxlDU1jgC9T/9V4Q+qyAEv/wtYDduoe4R1WGWO'
        'lqSxr8k6Tr92CjI1TXbJUP3N3V0pNYayUJDIIvjWy7T/10xRhMaRhBM88XDJh7QBpcZT'
        'KJo='
    )  # :on
    data = {  # :off
        'env': [
            'TOXENV=py26',
            'TOXENV=py27',
            'TOXENV=py33',
            'TOXENV=py34',
            'TOXENV=py35',
            'TOXENV=pypy',
            'TOXENV=docs'
        ],
        'language': 'python',
        'script': ['tox -e $TOXENV'],
        'python': ['3.5'],
        'after_success': ['coveralls'],
        'install': ['pip install tox coveralls'],
        'deploy': {
            True: {
                'repo': 'bionikspoon/pureyaml',
                'condition': '$TOXENV == py34',
                'tags': True
            },
            'password': {
                'secure': secure_block
            },
            'distributions': 'sdist bdist_wheel',
            'user': 'bionikspoon',
            'provider': 'pypi'
        }
    }  # :on
    if PY34 or PY35:
        expected = dedent("""
            python:
            - '3.5'
            after_success:
            - coveralls
            install:
            - pip install tox coveralls
            env:
            - TOXENV=py26
            - TOXENV=py27
            - TOXENV=py33
            - TOXENV=py34
            - TOXENV=py35
            - TOXENV=pypy
            - TOXENV=docs
            script:
            - tox -e $TOXENV
            deploy:
              true:
                condition: $TOXENV == py34
                tags: true
                repo: bionikspoon/pureyaml
              provider: pypi
              distributions: sdist bdist_wheel
              password:
                secure: {secure_block}
              user: bionikspoon
            language: python
        """)[1:].format(secure_block=secure_block)
    elif PY2:
        expected = dedent("""
            env:
            - TOXENV=py26
            - TOXENV=py27
            - TOXENV=py33
            - TOXENV=py34
            - TOXENV=py35
            - TOXENV=pypy
            - TOXENV=docs
            language: python
            script:
            - tox -e $TOXENV
            python:
            - '3.5'
            after_success:
            - coveralls
            install:
            - pip install tox coveralls
            deploy:
              true:
                repo: bionikspoon/pureyaml
                condition: $TOXENV == py34
                tags: true
              password:
                secure: {secure_block}
              distributions: sdist bdist_wheel
              user: bionikspoon
              provider: pypi
        """)[1:].format(secure_block=secure_block)
    else:
        expected = dedent("""
            install:
            - pip install tox coveralls
            env:
            - TOXENV=py26
            - TOXENV=py27
            - TOXENV=py33
            - TOXENV=py34
            - TOXENV=py35
            - TOXENV=pypy
            - TOXENV=docs
            language: python
            script:
            - tox -e $TOXENV
            python:
            - '3.5'
            after_success:
            - coveralls
            deploy:
              true:
                repo: bionikspoon/pureyaml
                condition: $TOXENV == py34
                tags: true
              password:
                secure: {secure_block}
              distributions: sdist bdist_wheel
              user: bionikspoon
              provider: pypi
        """)[1:].format(secure_block=secure_block)

    actual = dump(data)
    assert actual == expected

    with tmpdir.join('temp.yml').open('w') as f:
        pureyaml.dump(data, f)

    with tmpdir.join('temp.yml').open() as f:
        actual = f.read()

    assert actual == expected
