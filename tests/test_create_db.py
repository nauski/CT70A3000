"""Unit tests for create_db (table creation and admin seeding)."""
import sqlite3


def test_tables_are_created(test_db):
    """All 4 tables should exist after create_db runs."""
    from db import get_db

    with get_db() as (con, cur):
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = {row[0] for row in cur.fetchall()}

    assert "employee" in tables
    assert "supplier" in tables
    assert "category" in tables
    assert "product" in tables


def test_admin_seeded_on_empty_db(test_db):
    """A default admin user should be created when employee table is empty."""
    from db import get_db
    import create_db

    # create_db runs its function at module level on first import,
    # which already seeds the admin into our test db.
    # calling it again should be safe (idempotent).
    create_db.create_db()

    with get_db() as (con, cur):
        cur.execute("SELECT * FROM employee WHERE email='admin@ims.com'")
        admin = cur.fetchone()

    assert admin is not None
    assert admin[1] == "Admin"       # name
    assert admin[8] == "Admin"       # utype


def test_admin_not_duplicated(test_db):
    """Running create_db twice should not create duplicate admin users."""
    import create_db

    create_db.create_db()
    create_db.create_db()

    from db import get_db
    with get_db() as (con, cur):
        cur.execute("SELECT COUNT(*) FROM employee WHERE email='admin@ims.com'")
        count = cur.fetchone()[0]

    assert count == 1, "admin should only be seeded once"
