from db import get_db

def create_db():
    with get_db() as (con, cur):
        cur.execute("CREATE TABLE IF NOT EXISTS employee(eid INTEGER PRIMARY KEY AUTOINCREMENT,name text,email text,gender text,contact text,dob text,doj text,pass text,utype text,address text,salary text)")
        cur.execute("CREATE TABLE IF NOT EXISTS supplier(invoice INTEGER PRIMARY KEY AUTOINCREMENT,name text,contact text,desc text)")
        cur.execute("CREATE TABLE IF NOT EXISTS category(cid INTEGER PRIMARY KEY AUTOINCREMENT,name text)")
        cur.execute("CREATE TABLE IF NOT EXISTS product(pid INTEGER PRIMARY KEY AUTOINCREMENT,Category text, Supplier text,name text,price text,qty text,status text)")
        con.commit()

        # seed default admin if no employees exist yet
        cur.execute("SELECT COUNT(*) FROM employee")
        if cur.fetchone()[0] == 0:
            cur.execute(
                "INSERT INTO employee(name,email,gender,contact,dob,doj,pass,utype,address,salary) VALUES(?,?,?,?,?,?,?,?,?,?)",
                ("Admin", "admin@ims.com", "Male", "0000000000", "", "", "admin123", "Admin", "System", "0")
            )
            con.commit()


create_db()
