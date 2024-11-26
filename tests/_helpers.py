from importlib import import_module
import sys

import pytest

wrapped_libraries = ["numpy", "paddle"]
all_libraries = wrapped_libraries + []

# `sparse` added array API support as of Python 3.10.
# if sys.version_info >= (3, 10):
#     all_libraries.append('sparse')

def import_(library, wrapper=False):
    if library == 'cupy':
        pytest.importorskip(library)
    if wrapper:
        if 'jax' in library:
            # JAX v0.4.32 implements the array API directly in jax.numpy
            # Older jax versions use jax.experimental.array_api
            jax_numpy = import_module("jax.numpy")
            if not hasattr(jax_numpy, "__array_api_version__"):
                library = 'jax.experimental.array_api'
        elif library.startswith('sparse'):
            library = 'sparse'
        else:
            library = 'array_api_compat.' + library

    if library == 'paddle':
        xp = import_module(library)
        xp.asarray = xp.to_tensor
        return xp

    return import_module(library)
