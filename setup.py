from setuptools import setup, find_packages
import sys

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
    ],
    author="Marcin Lulek",
    author_email="info@webreactor.eu",
    license="BSD",
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
