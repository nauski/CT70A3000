# Architecture

Python/Tkinter desktop app for managing inventory, suppliers, employees, and billing. SQLite for storage, plain text files for bill receipts.

## Structure

```
login.py          Login screen, checks credentials against the employee table
dashboard.py      Main window — summary counts, menu to open the modules below
employee.py       Manage employees (admin only)
supplier.py       Manage suppliers
category.py       Add/delete product categories (no editing)
product.py        Manage products, picks category/supplier from dropdowns
sales.py          Look up past bills
billing.py        Separate billing app — not reachable from the dashboard
db.py             get_db() context manager, returns (connection, cursor)
create_db.py      Creates tables + seeds a default admin on first run
ui_helpers.py     Shared helper for building Treeview tables
```

## How it runs

You launch `dashboard.py`, which shows a login screen first. After logging in (email + password checked against the `employee` table), the login window closes and the dashboard opens. From there you can open any of the management modules, they each pop up as a separate Toplevel window.

`billing.py` is its own thing. It has its own `Tk()` root and you run it directly with `python billing.py`. It's not connected to the dashboard at all.

Logging out tears down the dashboard and brings back the login screen.

## Database

SQLite, stored in `ims.db`. Every module gets a connection through `get_db()` in `db.py` — it's a context manager that hands you a `(Connection, Cursor)` and closes the connection when you're done.

Tables (all created by `create_db.py`):

| Table | PK | Columns |
|-------|----|---------|
| employee | eid | name, email, gender, contact, dob, doj, pass, utype, address, salary |
| supplier | invoice | name, contact, desc |
| category | cid | name |
| product | pid | Category, Supplier, name, price, qty, status |

If the employee table is empty on startup, `create_db.py` inserts a default admin (`admin@ims.com` / `admin123`). The schema creation runs at import time, just importing `create_db` is enough to ensure the tables exist.

Bills are saved as text files in `bill/`, named by invoice number (e.g. `12345678.txt`). The sales module reads those files back to display them.

## UI

Everything is Tkinter. The CRUD modules all look similar: form fields on top, Save/Update/Delete/Clear buttons, and a Treeview table at the bottom. Clicking a row fills in the form. `create_treeview()` in `ui_helpers.py` handles setting up the table columns and scrollbars so each module doesn't have to repeat that.

## Access control

The `utype` column on the employee table is either "Admin" or "Employee". Only admins can open the employee management module — everyone else gets an error dialog. Everything else is open to any logged-in user.

Passwords are stored in plain text. No hashing. No ORM either, it's all raw SQL.
