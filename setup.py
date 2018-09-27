from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="webhelpers2_grid",
    version="0.9",
    description=""" HTML Grid renderer that helps generating HTML tables (or other structures) 
      for data presentation, supports ordering, sorting columns, and is very customizable
      """,
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Framework :: Pyramid",
        "Framework :: Django",
        "Framework :: Flask",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
    ],
    author="Marcin Lulek",
    author_email="info@webreactor.eu",
    license="BSD",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    zip_safe=True,
    include_package_data=True,
    package_data={
        "": ["*.txt", "*.rst", "*.ini", "*.css"],
        "webhelpers2_grid": ["stylesheets/*.css"],
    },
    extras_require={
        "dev": ["coverage", "pytest", "tox", "mock", "jinja2"],
        "lint": ["black"],
    },
    test_suite="webhelpers2_grid.tests",
    install_requires=["webhelpers2"],
)
