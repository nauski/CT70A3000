"""Integration tests for login authentication flow.

These tests are gated behind the LOGIN feature flag.
They will be skipped if LOGIN is not in enabled_features.txt.
"""
import pytest


@pytest.mark.feature("LOGIN")
def test_valid_login_returns_user(test_db):
    """Correct email + password should return the user record."""
    from db import get_db

    # insert a test user
    with get_db() as (con, cur):
        cur.execute(
            "INSERT INTO employee(name,email,gender,contact,dob,doj,pass,utype,address,salary) VALUES(?,?,?,?,?,?,?,?,?,?)",
            ("Test User", "test@ims.com", "Male", "1234567890", "", "", "secret123", "Employee", "Test", "1000")
        )
        con.commit()

    # simulate login query (same as login.py does)
    with get_db() as (con, cur):
        cur.execute("SELECT * FROM employee WHERE email=? AND pass=?", ("test@ims.com", "secret123"))
        user = cur.fetchone()

    assert user is not None
    assert user[1] == "Test User"
    assert user[8] == "Employee"


@pytest.mark.feature("LOGIN")
def test_wrong_password_returns_none(test_db):
    """Wrong password should return no user."""
    from db import get_db

    with get_db() as (con, cur):
        cur.execute(
            "INSERT INTO employee(name,email,gender,contact,dob,doj,pass,utype,address,salary) VALUES(?,?,?,?,?,?,?,?,?,?)",
            ("Test User", "test@ims.com", "Male", "1234567890", "", "", "secret123", "Employee", "Test", "1000")
        )
        con.commit()

    with get_db() as (con, cur):
        cur.execute("SELECT * FROM employee WHERE email=? AND pass=?", ("test@ims.com", "wrongpassword"))
        user = cur.fetchone()

    assert user is None


@pytest.mark.feature("LOGIN")
def test_nonexistent_email_returns_none(test_db):
    """Email that doesn't exist should return no user."""
    from db import get_db

    with get_db() as (con, cur):
        cur.execute("SELECT * FROM employee WHERE email=? AND pass=?", ("nobody@ims.com", "anything"))
        user = cur.fetchone()

    assert user is None


@pytest.mark.feature("LOGIN")
def test_admin_role_is_preserved(test_db):
    """Login should correctly return the user's role for access control."""
    from db import get_db

    with get_db() as (con, cur):
        cur.execute(
            "INSERT INTO employee(name,email,gender,contact,dob,doj,pass,utype,address,salary) VALUES(?,?,?,?,?,?,?,?,?,?)",
            ("Admin User", "admin@test.com", "Female", "9999999999", "", "", "adminpass", "Admin", "HQ", "5000")
        )
        con.commit()

    with get_db() as (con, cur):
        cur.execute("SELECT * FROM employee WHERE email=? AND pass=?", ("admin@test.com", "adminpass"))
        user = cur.fetchone()

    assert user is not None
    assert user[8] == "Admin"
