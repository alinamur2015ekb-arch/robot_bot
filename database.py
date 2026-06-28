import aiosqlite
from typing import Optional


DB_NAME = "database.db"

async def init_telem():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS telem(
            id INTEGER PRIMARY KEY,
            temperatura REAL,
            humidity REAL,
            status REAL,
            time_cleaning INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                         )
                         ''')
        

async def create_telem(temperatura, humidity, status):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            INSERT INTO telem (temperatura, humidity, status) 
            VALUES (?, ?, ?)
        """, (temperatura, humidity, status))
        await db.commit()
