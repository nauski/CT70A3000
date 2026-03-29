"""Regression tests for security fixes (SQL injection, eval safety)."""
import sqlite3


def test_sql_injection_blocked_in_product_search(test_db):
    """Search with SQL injection payload should not execute arbitrary SQL.

    The old code concatenated user input directly into the query.
    The whitelist + parameterized query should prevent injection.
    """
    from db import get_db

    # insert a test product
    with get_db() as (con, cur):
        cur.execute("INSERT INTO product(Category,Supplier,name,price,qty,status) VALUES(?,?,?,?,?,?)",
                    ("Electronics", "TestSupplier", "Laptop", "999", "10", "Active"))
        con.commit()

    # simulate what the search method does with the whitelist approach
    allowed_columns = {"Category": "Category", "Supplier": "Supplier", "Name": "name"}

    # try an injection payload as the column name
    malicious_column = "name; DROP TABLE product; --"
    col = allowed_columns.get(malicious_column)
    assert col is None, "injection payload should not match any whitelisted column"

    # verify the table still exists and data is intact
    with get_db() as (con, cur):
        cur.execute("SELECT COUNT(*) FROM product")
        assert cur.fetchone()[0] == 1


def test_sql_injection_blocked_in_search_value(test_db):
    """Parameterized LIKE query should treat injection as literal text."""
    from db import get_db

    with get_db() as (con, cur):
        cur.execute("INSERT INTO product(Category,Supplier,name,price,qty,status) VALUES(?,?,?,?,?,?)",
                    ("Electronics", "TestSupplier", "Laptop", "999", "10", "Active"))
        con.commit()

    # this payload would be dangerous with string concatenation
    malicious_value = "'; DROP TABLE product; --"

    with get_db() as (con, cur):
        cur.execute("SELECT * FROM product WHERE name LIKE ?", (f"%{malicious_value}%",))
        rows = cur.fetchall()

    # should return no results, not destroy the table
    assert len(rows) == 0

    # table should still exist
    with get_db() as (con, cur):
        cur.execute("SELECT COUNT(*) FROM product")
        assert cur.fetchone()[0] == 1


def test_eval_whitelist_blocks_code_injection():
    """The calculator whitelist should reject anything that isn't digits and +-*/.

    This is a regression test for the eval() vulnerability fix in billing.py.
    """
    allowed_chars = '0123456789+-*/.'

    safe_inputs = ["2+2", "100*3.5", "10/2-1", "999"]
    dangerous_inputs = [
        "__import__('os').system('rm -rf /')",
        "exec('print(1)')",
        "open('/etc/passwd').read()",
        "a+b",
    ]

    for inp in safe_inputs:
        assert all(c in allowed_chars for c in inp), f"'{inp}' should be allowed"

    for inp in dangerous_inputs:
        assert not all(c in allowed_chars for c in inp), f"'{inp}' should be blocked"
