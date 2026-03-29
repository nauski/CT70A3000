"""Integration tests for product CRUD lifecycle."""


def test_add_product(test_db):
    """Should be able to insert a product and retrieve it."""
    from db import get_db

    with get_db() as (con, cur):
        cur.execute("INSERT INTO category(name) VALUES(?)", ("Electronics",))
        cur.execute("INSERT INTO supplier(name,contact,desc) VALUES(?,?,?)", ("TechCorp", "555-0100", "Supplier"))
        cur.execute(
            "INSERT INTO product(Category,Supplier,name,price,qty,status) VALUES(?,?,?,?,?,?)",
            ("Electronics", "TechCorp", "Laptop", "999.99", "50", "Active")
        )
        con.commit()

    with get_db() as (con, cur):
        cur.execute("SELECT * FROM product WHERE name='Laptop'")
        product = cur.fetchone()

    assert product is not None
    assert product[3] == "Laptop"
    assert product[4] == "999.99"
    assert product[5] == "50"
    assert product[6] == "Active"


def test_update_product(test_db):
    """Should be able to update a product's price and quantity."""
    from db import get_db

    with get_db() as (con, cur):
        cur.execute(
            "INSERT INTO product(Category,Supplier,name,price,qty,status) VALUES(?,?,?,?,?,?)",
            ("Electronics", "TechCorp", "Laptop", "999.99", "50", "Active")
        )
        con.commit()
        pid = cur.lastrowid

    with get_db() as (con, cur):
        cur.execute("UPDATE product SET price=?, qty=? WHERE pid=?", ("899.99", "45", pid))
        con.commit()

    with get_db() as (con, cur):
        cur.execute("SELECT price, qty FROM product WHERE pid=?", (pid,))
        row = cur.fetchone()

    assert row[0] == "899.99"
    assert row[1] == "45"


def test_delete_product(test_db):
    """Should be able to delete a product and confirm it's gone."""
    from db import get_db

    with get_db() as (con, cur):
        cur.execute(
            "INSERT INTO product(Category,Supplier,name,price,qty,status) VALUES(?,?,?,?,?,?)",
            ("Electronics", "TechCorp", "Mouse", "29.99", "200", "Active")
        )
        con.commit()
        pid = cur.lastrowid

    with get_db() as (con, cur):
        cur.execute("DELETE FROM product WHERE pid=?", (pid,))
        con.commit()

    with get_db() as (con, cur):
        cur.execute("SELECT * FROM product WHERE pid=?", (pid,))
        result = cur.fetchone()

    assert result is None


def test_product_duplicate_name_detected(test_db):
    """The app checks for duplicate product names before inserting.

    This test verifies the detection query works.
    """
    from db import get_db

    with get_db() as (con, cur):
        cur.execute(
            "INSERT INTO product(Category,Supplier,name,price,qty,status) VALUES(?,?,?,?,?,?)",
            ("Electronics", "TechCorp", "Laptop", "999.99", "50", "Active")
        )
        con.commit()

    # check for duplicate (same logic as product.py add method)
    with get_db() as (con, cur):
        cur.execute("SELECT * FROM product WHERE name=?", ("Laptop",))
        existing = cur.fetchone()

    assert existing is not None, "duplicate detection should find the existing product"
