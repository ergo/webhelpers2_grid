from __future__ import print_function

import os
from collections import namedtuple

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

from webhelpers2_grid import Grid, ListGrid
from webhelpers2.html import HTML
from webhelpers2.html.tags import link_to

DemoRow = namedtuple("DemoRow", "group_name options id foo")

test_data = [
    {"group_name": "foo", "options": "lalala", "id": 1},
    {"group_name": None, "options": "lalala2", "id": 2},
    {"group_name": "foo3", "options": "lalala3", "id": 3},
    {"group_name": "foo4", "options": "lalala4", "id": 4},
]

test_obj_data = [
    DemoRow(
        group_name="obj {}".format(r["group_name"]),
        options=r["options"],
        id=r["id"] * 2,
        foo="X",
    )
    for r in test_data
]

mixed_type_data = test_data + test_obj_data

list_data = [
    [1, "a", 3, "c", 5],
    [11, "aa", 33, "cc", 55],
    [111, "aaa", 333, "ccc", 555],
]


def url(urlpath, **params):
    """ Dummy url generator """
    return urlpath + "?" + urlencode(params)


# grids are shared with demo renderer


def get_basic_grid():
    return Grid(mixed_type_data, columns=["_numbered", "group_name", "options"])


def get_custom_column_grid():
    class CustomGrid(Grid):
        def __init__(self, *args, **kwargs):
            super(CustomGrid, self).__init__(*args, **kwargs)
            self.labels["options"] = "FOOBAAR"
            self.column_formats["options"] = self.options_td

        def options_td(self, col_num, i, item):
            u = url(
                "/tickets/view", ticket_id=item.id, y=self.additional_kw["context"]["y"]
            )
            a = link_to(item.options, u)
            return HTML.td(a)

    g = CustomGrid(
        test_obj_data,
        columns=["_numbered", "group_name", "options", "ffff"],
        context={"x": "context var", "y": 99},
    )
    return g


def get_order_shift_grid():
    g = Grid(test_data, columns=["_numbered", "group_name", "options"], start_number=10)
    return g


def get_direction_aware_grid():
    """
    order direction demo
    """

    class GridWithUrlGenerator(Grid):
        def generate_header_link(self, column_number, column, label_text):
            """ This handles generation of link and then decides to call
            self.default_header_ordered_column_format
            or
            self.default_header_column_format
            based on if current column is the one that is used for sorting or not
            """

            # implementation START #
            # this will handle possible URL generation

            # dummy get object, assume options is currently selected
            # normally this will be something like request.GET.mixed()
            GET_copy = {"order_col": "options", "order_dir": "asc"}

            self.order_column = GET_copy.pop("order_col", None)
            self.order_dir = GET_copy.pop("order_dir", None)

            if column == self.order_column and self.order_dir == "asc":
                new_order_dir = "dsc"
            else:
                new_order_dir = "asc"

            GET_copy["order_col"] = column
            GET_copy["order_dir"] = new_order_dir

            href = self.url_generator("https://google.com", **GET_copy)

            label_text = HTML.tag("a", href=href, c=label_text)
            # implementation END #

            if column == self.order_column:
                return self.default_header_ordered_column_format(
                    column_number, column, label_text
                )
            else:
                return self.default_header_column_format(
                    column_number, column, label_text
                )

    g = GridWithUrlGenerator(
        test_data,
        columns=["_numbered", "group_name", "options"],
        order_column="options",
        order_direction="asc",
        exclude_ordering=["_numbered"],
        url_generator=url,
    )
    return g


def get_list_grid():
    """
    basic demo
    """

    g = ListGrid(
        list_data, columns=[1, 3, 2, 0], column_labels=["One", "Three", "Two", "Zero"]
    )
    return g


def test_basic_grid():
    grid = get_basic_grid()
    rendered = str(grid)

def test_order_shift_grid():
    grid = get_order_shift_grid()
    rendered = str(grid)


def test_custom_columns():
    grid = get_custom_column_grid()
    rendered = str(grid)


def test_direction_aware_grid():
    grid = get_direction_aware_grid()
    rendered = str(grid)


def test_list_grid():
    grid = get_direction_aware_grid()
    rendered = str(grid)
