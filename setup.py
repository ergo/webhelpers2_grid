from setuptools import setup, find_packages
import sys
setup(name='webhelpers2_grid',
      version='0.1',
      description=""" HTML Grid system that helps generating HTML tables (or other structures) for data presentation, supports ordering,
sorting columns, and has customizable looks
      """,
      author='Marcin Lulek',
      author_email='info@webreactor.eu',
      license='BSD',
      packages=find_packages(),
      zip_safe=True,
      include_package_data=True,
      package_data={
        '': ['*.txt', '*.rst', '*.ini','*.css'],
        'webhelpers2_grid': ['stylesheets/*.css'],
        },
      test_suite='webhelpers2_grid.tests',
      install_requires=['webhelpers2']
      )