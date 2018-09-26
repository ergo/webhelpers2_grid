"""A helper to make an HTML table from a list of dicts, objects, or sequences.

A set of CSS styles complementing this helper is in
"webhelpers2_grid/html/public/stylesheets/grid.css". To use them, include the
stylesheet in your applcation and set your <table> class to "stylized".

"""

from webhelpers2.html.builder import HTML, literal


GRID_NOT_FOUND = "__GRID_NO_ATTR_FOUND__"


def dummy_value(*args):
    return None


class Grid(object):
    """
    This class is designed to aid programmer in the task of creation of
    tables/grids - structures that are mostly built from datasets.

    """

    def __init__(
        self,
        itemlist,
        columns,
        column_labels=None,
        column_formats=None,
        start_number=1,
        order_column=None,
        order_direction=None,
        request=None,
        url_generator=None,
        exclude_ordering=None,
        **kw
    ):
        """

        :param itemlist: items to render
        :param columns: names used to for column information
        :param column_labels: mapping of column label overrides
        :param column_formats: mapping of callables for column rendering
        :param start_number: number of first item in grid
        :param order_column: column that is being used for ordering
        :param order_direction: [asc|desc] string informing of order direction
        :param request: request object
        :param url_generator: url generator function
        :param kw: additional keyword parameters will be stored as ``additional_kw``
        :return: Grid
        """
        self.labels = column_labels or {}
        self.exclude_ordering = (
            exclude_ordering if exclude_ordering is not None else columns
        )
        self.itemlist = itemlist
        self.columns = columns
        self.column_formats = column_formats or {}
        if "_numbered" in columns:
            self.labels["_numbered"] = "#"
        if "_numbered" not in self.column_formats:
            self.column_formats["_numbered"] = self.numbered_column_format
        self.start_number = start_number
        self.order_dir = order_direction
        self.order_column = order_column
        # backward compatibility with old pylons grid
        if not hasattr(self, "request"):
            self.request = request
        self.url_generator = url_generator
        self.additional_kw = kw

    def calc_row_no(self, i):
        if self.order_dir in ("asc", None):
            return self.start_number + i
        else:
            return self.start_number - i

    def make_headers(self):
        header_columns = []

        for i, column in enumerate(self.columns):
            # let"s generate header column contents
            if column in self.labels:
                label_text = self.labels[column]
            else:
                label_text = column.replace("_", " ").title()
            # handle non clickable columns
            if column in self.exclude_ordering:
                header = self.default_header_column_format(i + 1, column, label_text)
            # handle clickable columns
            else:
                header = self.generate_header_link(i + 1, column, label_text)
            header_columns.append(header)
        return HTML(*header_columns)

    def make_columns(self, i, record):
        columns = []
        row_no = self.calc_row_no(i)
        for col_num, column in enumerate(self.columns):
            if column in self.column_formats:
                r = self.column_formats[column](col_num + 1, row_no, record)
            else:
                r = self.default_column_format(col_num + 1, row_no, record, column)
            columns.append(r)
        return HTML(*columns)

    def __html__(self):
        """ renders the grid """
        records = []
        # first render headers record
        headers = self.make_headers()
        r = self.default_header_record_format(headers)
        records.append(r)
        # now lets render the actual item grid
        for i, record in enumerate(self.itemlist):
            columns = self.make_columns(i, record)
            if hasattr(self, "custom_record_format"):
                r = self.custom_record_format(i + 1, record, columns)
            else:
                r = self.default_record_format(i + 1, record, columns)
            records.append(r)
        return HTML(*records)

    def __str__(self):
        return self.__html__()

    def generate_header_link(self, column_number, column, label_text):
        """ This handles generation of link and then decides to call
        ``self.default_header_ordered_column_format`` 
        or 
        ``self.default_header_column_format`` 
        based on whether current column is the one that is used for sorting.

        """
        # Is the current column the one we're ordering on?
        if column == self.order_column:
            return self.default_header_ordered_column_format(
                column_number, column, label_text
            )
        else:
            return self.default_header_column_format(column_number, column, label_text)

    def default_column_format(self, column_number, i, record, column_name):
        class_name = "c%s" % column_number
        # first try to lookup property
        col_value = getattr(record, column_name, GRID_NOT_FOUND)
        # if this fails lookup via __getattr__
        if col_value is GRID_NOT_FOUND:
            col_value = getattr(record, "get", dummy_value)(column_name)
        return HTML.tag("td", col_value, class_=class_name)

    def numbered_column_format(self, column_number, i, record):
        class_name = "c%s" % column_number
        return HTML.tag("td", i, class_=class_name)

    def default_record_format(self, i, record, columns):
        if i % 2 == 0:
            class_name = "even r%s" % i
        else:
            class_name = "odd r%s" % i
        return HTML.tag("tr", columns, class_=class_name)

    def default_header_record_format(self, headers):
        return HTML.tag("tr", headers, class_="header")

    def default_header_ordered_column_format(
        self, column_number, column_name, header_label
    ):
        dir_char = "&#9650;" if self.order_dir == "asc" else "&#9660;"
        header_label = HTML(
            header_label, HTML.tag("span", literal(dir_char), class_="marker")
        )
        if column_name == "_numbered":
            column_name = "numbered"
        class_name = "c%s ordering %s %s" % (column_number, self.order_dir, column_name)
        return HTML.tag("td", header_label, class_=class_name)

    def default_header_column_format(self, column_number, column_name, header_label):
        if column_name == "_numbered":
            column_name = "numbered"
        if column_name in self.exclude_ordering:
            class_name = "c%s %s" % (column_number, column_name)
            return HTML.tag("td", header_label, class_=class_name)
        else:
            header_label = HTML(header_label, HTML.tag("span", class_="marker"))
            class_name = "c%s ordering %s" % (column_number, column_name)
            return HTML.tag("td", header_label, class_=class_name)


class ObjectGrid(Grid):
    """ Bw. compatibility object
    """


class ListGrid(Grid):
    """ A grid class for a sequence of lists.
    
    This grid class assumes that the rows are lists rather than dicts, and
    uses subscript access to retrieve the column values. Some constructor args
    are also different.

    If ``columns`` is not specified in the constructor, it will examine 
    ``itemlist[0]`` to determine the number of columns, and display them in
    order.  This works only if ``itemlist`` is a sequence and not just an
    iterable.  Alternatively, you can pass an int to specify the number of
    columns, or a list of int subscripts to override the column order.
    Examples::
    
        grid = ListGrid(list_data)
        grid = ListGrid(list_data, columns=4)
        grid = ListGrid(list_data, columns=[1, 3, 2, 0]) 

    ``column_labels`` may be a list of strings. The class will calculate the
    appropriate subscripts for the superclass dict.
    
    """

    def __init__(self, itemlist, columns=None, column_labels=None, *args, **kw):
        """

        :param itemlist:
        :param columns:
        :param column_labels:
        :param args:
        :param kw:
        :return:
        """
        if columns is None:
            columns = range(len(itemlist[0]))
        elif isinstance(columns, int):
            columns = range(columns)
        # The superclass requires the ``columns`` elements to be strings.
        super_columns = [str(x) for x in columns]
        # The superclass requires ``column_labels`` to be a dict.
        super_labels = column_labels
        if isinstance(column_labels, (list, tuple)):
            super_labels = dict(zip(super_columns, column_labels))
        Grid.__init__(self, itemlist, super_columns, super_labels, *args, **kw)

    def default_column_format(self, column_number, i, record, column_name):
        class_name = "c%s" % (column_number)
        return HTML.tag("td", record[int(column_name)], class_=class_name)
