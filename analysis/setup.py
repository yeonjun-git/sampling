from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [
    Extension("core_metric", ['analysis/distribution.py'])
]

setup(
    name='core_metric',
    ext_modules=cythonize(
        extensions,
        compiler_directives={'language_level': "3"}
    )
)