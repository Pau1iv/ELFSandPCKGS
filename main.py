from fastapi import FastAPI
import sqlite3

app = FastAPI()

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

def is_table_exists(table_name):
    cursor.execute("PRAGMA table_info({})".format(table_name))
    return cursor.fetchall()

@app.post("/package")
async def post_package(toy: str, elf_id: int):
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS packages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                toy TEXT,
                status INTEGER DEFAULT 0,
                elf_id INTEGER
            )
        ''')

    cursor.execute('INSERT INTO packages (name, elf_id) VALUES (?, ?)', (toy, elf_id))
    conn.commit()
    return {"message": "New package has been added to database"}

@app.put("/package")
async def put_package(pack_id: int, status:bool):
    if is_table_exists('packages'):
        cursor.execute('UPDATE packages SET status = ? WHERE id = ?', (int(status), pack_id))
    conn.commit()
    return {"message":"Package has been updated in database"}

@app.get("/package")
async def get_package(pack_id: int):
    mess = "There's no package with that ID"
    if is_table_exists('packages'):
        result = cursor.execute("SELECT * FROM packages WHERE id = ?", (pack_id,))
        mess = str(result.fetchall().__str__())
    conn.commit()
    return {"message": mess}

@app.delete("/package")
async def delete_packages(pack_id: int):
    if is_table_exists('packages'):
        cursor.execute("DELETE FROM packages WHERE id = ?", (pack_id,))
        return {"message": "Package has been deleted"}

@app.post("/elfs")
async def post_elf(elf_name: str):
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS elfs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    leave INTEGER DEFAULT 0,
                    maternity INTEGER DEFAULT 0
                )
            ''')
    cursor.execute('INSERT INTO elfs (name) VALUES (?)', (elf_name,))
    conn.commit()
    return{"message": "New elf has been added to database"}

@app.put("/elfs")
async def put_elf(elf_id: int, leave: bool, maternity: bool):
    if is_table_exists('elfs'):
        cursor.execute('UPDATE elfs SET leave = ? WHERE id = ?', (int(leave), elf_id))
        cursor.execute('UPDATE elfs SET maternity = ? WHERE id = ?', (int(maternity), elf_id))
    conn.commit()
    return {"message": "Information about elf has been updated in database"}

@app.get("/elfs")
async def get_elf(elf_id: int):
    mess = "There's no package with that ID"
    if is_table_exists('elfs'):
        result = cursor.execute("SELECT * FROM elfs WHERE id = ?", (elf_id,))
        mess = str(result.fetchall().__str__())
    conn.commit()

    return {"message": mess}

@app.delete("/elfs")
async def delete_elf(elf_id):
    if is_table_exists('elfs'):
        cursor.execute("DELETE FROM elfs WHERE id = ?", (elf_id,))
        return {"message": "Elf has been deleted from database"}

@app.get("/")
async def test():
    return {"message": "Test"}


