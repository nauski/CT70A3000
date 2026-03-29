import pytest
import sqlite3
import tempfile
import os
import sys

# add project root to path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

FEATURES_FILE = os.path.join(os.path.dirname(__file__), "enabled_features.txt")


def load_enabled_features():
    """Read feature flags from enabled_features.txt"""
    if not os.path.exists(FEATURES_FILE):
        return set()
    with open(FEATURES_FILE) as f:
        return {line.strip() for line in f if line.strip()}


ENABLED_FEATURES = load_enabled_features()


def pytest_configure(config):
    config.addinivalue_line("markers", "feature(name): only run if feature is enabled in enabled_features.txt")


def pytest_collection_modifyitems(config, items):
    """Skip tests whose feature marker is not in enabled_features.txt"""
    for item in items:
        feature_markers = [m for m in item.iter_markers(name="feature")]
        for marker in feature_markers:
            feature_name = marker.args[0]
            if feature_name not in ENABLED_FEATURES:
                item.add_marker(pytest.mark.skip(reason=f"feature '{feature_name}' not in enabled_features.txt"))


@pytest.fixture
def test_db(tmp_path, monkeypatch):
    """Provide a temporary database for tests.

    Patches db.DB_PATH so all code that imports from db
    uses the temp database instead of the real one.
    """
    db_path = str(tmp_path / "test_ims.db")

    import db as db_module
    monkeypatch.setattr(db_module, "DB_PATH", db_path)

    # create tables
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS employee(eid INTEGER PRIMARY KEY AUTOINCREMENT,name text,email text,gender text,contact text,dob text,doj text,pass text,utype text,address text,salary text)")
    cur.execute("CREATE TABLE IF NOT EXISTS supplier(invoice INTEGER PRIMARY KEY AUTOINCREMENT,name text,contact text,desc text)")
    cur.execute("CREATE TABLE IF NOT EXISTS category(cid INTEGER PRIMARY KEY AUTOINCREMENT,name text)")
    cur.execute("CREATE TABLE IF NOT EXISTS product(pid INTEGER PRIMARY KEY AUTOINCREMENT,Category text, Supplier text,name text,price text,qty text,status text)")
    con.commit()
    con.close()

    yield db_path
