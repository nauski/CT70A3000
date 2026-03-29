"""Unit tests for the db module (get_db context manager)."""
import sqlite3


def test_get_db_returns_connection_and_cursor(test_db):
    """get_db should yield a working connection and cursor."""
    from db import get_db

    with get_db() as (con, cur):
        assert con is not None
        assert cur is not None
        cur.execute("SELECT 1")
        assert cur.fetchone()[0] == 1


def test_get_db_closes_connection(test_db):
    """Connection should be closed after exiting the with block."""
    from db import get_db

    with get_db() as (con, cur):
        pass

    # trying to use a closed connection should raise
    try:
        con.execute("SELECT 1")
        closed = False
    except Exception:
        closed = True

    assert closed, "connection should be closed after exiting context manager"


def test_get_db_closes_on_exception(test_db):
    """Connection should be closed even if an exception occurs inside the block."""
    from db import get_db

    try:
        with get_db() as (con, cur):
            raise ValueError("test error")
    except ValueError:
        pass

    try:
        con.execute("SELECT 1")
        closed = False
    except Exception:
        closed = True

    assert closed, "connection should be closed even after exception"
