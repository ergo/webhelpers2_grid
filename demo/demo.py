from __future__ import print_function

import os
import importlib

from pathlib import Path

# generating demo pages assumes py 3.5+

import_path = Path(__file__).absolute().parent.parent / "tests" / "tests.py"
loader = importlib.machinery.SourceFileLoader("grid_tests", str(import_path))
spec = importlib.util.spec_from_loader(loader.name, loader)
grid_tests = importlib.util.module_from_spec(spec)
loader.exec_module(grid_tests)

from jinja2 import Environment, FileSystemLoader, select_autoescape

jinja_env = Environment(
    loader=FileSystemLoader("."), autoescape=select_autoescape(["html", "xml"])
)

grids_to_render = [
    {
        "name": "Basic demo",
        "description": """
        This table shows a basic grid.
        """,
        "grid": grid_tests.get_basic_grid(),
    },
    {
        "name": "Custom column demo",
        "description": """
        This table shows a grid with a customized column and header label.
        """,
        "grid": grid_tests.get_custom_column_grid(),
    },
    {
        "name": "Order shift demo",
        "description": """
        This table shows a grid with order starting from 10.
        """,
        "grid": grid_tests.get_order_shift_grid(),
    },
    {
        "name": "Header aware of order direction demo",
        "description": """
        This table shows a grid that has a markup indicating order direction.
        Options column has sorting set to "asc" """,
        "grid": grid_tests.get_direction_aware_grid(),
    },
    {
        "name": "List grid demo",
        "description": """This table shows a basic grid generated from 
        lists - it has customized order of columns.""",
        "grid": grid_tests.get_list_grid(),
    },
]


def write_file(dir, filename, content):
    print("... writing '%s'" % filename)
    path = os.path.join(dir, filename)
    f = open(path, "w")
    f.write(content)
    f.close()


def main():
    tmpl = jinja_env.get_template("layout.jinja2")
    for grid_data in grids_to_render:
        rendered = (tmpl.render(**grid_data))
        write_file('../gh-pages', '{}.html'.format(grid_data['name'].replace(' ', '_').lower()), rendered)


if __name__ == "__main__":
    main()
