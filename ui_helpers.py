from tkinter import *
from tkinter import ttk

def create_treeview(parent, columns):
    """Create a Treeview with scrollbars inside parent frame.

    columns: list of (column_id, heading_text, width) tuples
    Returns the Treeview widget.
    """
    scrolly = Scrollbar(parent, orient=VERTICAL)
    scrollx = Scrollbar(parent, orient=HORIZONTAL)

    col_ids = tuple(c[0] for c in columns)
    tree = ttk.Treeview(parent, columns=col_ids,
                        yscrollcommand=scrolly.set,
                        xscrollcommand=scrollx.set)

    scrollx.pack(side=BOTTOM, fill=X)
    scrolly.pack(side=RIGHT, fill=Y)
    scrollx.config(command=tree.xview)
    scrolly.config(command=tree.yview)

    for col_id, heading, width in columns:
        tree.heading(col_id, text=heading)
        tree.column(col_id, width=width)

    tree["show"] = "headings"
    tree.pack(fill=BOTH, expand=1)
    return tree
