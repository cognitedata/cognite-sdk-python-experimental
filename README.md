
<a href="https://cognite.com/">
    <img src="https://github.com/cognitedata/cognite-python-docs/blob/master/img/cognite_logo.png" alt="Cognite logo" title="Cognite" align="right" height="80" />
</a>

Cognite Python SDK Experimental Extensions
==========================================
[![Release Status](https://github.com/cognitedata/cognite-sdk-python-experimental/workflows/release/badge.svg)](https://github.com/cognitedata/cognite-sdk-python-experimental/actions)
[![Build Status](https://github.com/cognitedata/cognite-sdk-python-experimental/workflows/test_and_build/badge.svg)](https://github.com/cognitedata/cognite-sdk-python-experimental/actions)
[![Documentation Status](https://readthedocs.com/projects/cognite-sdk-experimental/badge/?version=latest)](https://cognite-sdk-experimental.readthedocs-hosted.com/en/latest/)
[![PyPI version](https://badge.fury.io/py/cognite-sdk-experimental.svg)](https://pypi.org/project/cognite-sdk-experimental/)
[![tox](https://img.shields.io/badge/tox-3.6%2B-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![codecov](https://codecov.io/gh/cognitedata/cognite-sdk-python/branch/master/graph/badge.svg)](https://codecov.io/gh/cognitedata/cognite-sdk-python)

This is an extensions package to the [Cognite Python SDK](https://github.com/cognitedata/cognite-sdk-python)
 for developers testing features in development in Cognite Data Fusion (CDF). 

## Quickstart
Import a client with:

```python
from cognite.experimental import CogniteClient
```
The resulting client object will contain all normal SDK functionality
in addition to experimental extensions.

Note that Asset functionality currently points to playground due to typing,
 if needed use `client.assets_v1` to force the use of the v1 endpoints.

## Documentation
* [Experimental SDK Extensions Documentation](https://cognite-sdk-experimental.readthedocs-hosted.com/en/latest/)
* [Examples for using the contextualization endpoints](CONTEXTUALIZATION.md)
* [SDK Documentation](https://cognite-docs.readthedocs-hosted.com/en/latest/)
* [API Documentation](https://doc.cognitedata.com/)
* [Cognite Developer Documentation](https://docs.cognite.com/dev/)

## Installation
To install this package:
```bash
$ pip install cognite-sdk-experimental
```

