# webhelpers2_grid

HTML Grid renderer that helps generating HTML tables (or other structures) 
      for data presentation, supports ordering, sorting columns, and is very customizable

**DOCUMENTATION**: https://webhelpers-grid2.readthedocs.io

**DEMOS**: http://ergo.github.io/webhelpers_grid2/gh-pages/ (static page)

**BUG TRACKER**: https://github.com/ergo/webhelpers_grid2/issues


Example Usage::

    test_data = [
                 {"group_name": "foo", "options": "lalala", "id":1},
                 {"group_name": "foo2", "options": "lalala2", "id":2},
                 {"group_name": "foo3", "options": "lalala3", "id":3},
                 {"group_name": "foo4", "options": "lalala4", "id":4},
                 ]

    def options_td(col_num, i, item):
        u = url("/tickets/view", ticket_id=item["id"])
        a = link_to(item["options"], u)
        return HTML.td(a)

    g = Grid(test_data, columns=["_numbered", "group_name", "options"])
    g.labels["options"] = 'FOOBAAR'
    g.column_formats["options"] = options_td
    str(g)


webhelpers2_grid is BSD Licensed
