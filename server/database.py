#!/usr/bin/env python3
"""
🦅 EagleFarm Database
SQLite database management
"""

import sqlite3
import threading
from contextlib import contextmanager
from server import config

# Thread-local storage for database connections
_local = threading.local()


def get_db():
    """Get thread-local database connection"""
    if not hasattr(_local, 'db'):
        _local.db = sqlite3.connect(
            config.DATABASE_PATH,
            check_same_thread=False
        )
        _local.db.row_factory = sqlite3.Row
    return _local.db


def init_db():
    """Initialize database tables"""
    db = get_db()
    
    db.execute('''
        CREATE TABLE IF NOT EXISTS flags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            flag TEXT UNIQUE NOT NULL,
            sploit TEXT NOT NULL,
            team TEXT NOT NULL,
            time REAL NOT NULL,
            status TEXT DEFAULT 'QUEUED',
            checksystem_response TEXT,
            UNIQUE(flag)
        )
    ''')
    
    db.execute('''
        CREATE INDEX IF NOT EXISTS idx_status ON flags(status)
    ''')
    
    db.execute('''
        CREATE INDEX IF NOT EXISTS idx_time ON flags(time)
    ''')
    
    db.execute('''
        CREATE INDEX IF NOT EXISTS idx_sploit ON flags(sploit)
    ''')
    
    db.commit()
    print("✅ Database initialized")


def add_flags(flags_data):
    """
    Add flags to database
    flags_data: list of {'flag': str, 'sploit': str, 'team': str}
    Returns: number of new flags added
    """
    import time
    
    db = get_db()
    added = 0
    current_time = time.time()
    
    for item in flags_data:
        try:
            db.execute(
                'INSERT INTO flags (flag, sploit, team, time) VALUES (?, ?, ?, ?)',
                (item['flag'], item['sploit'], item['team'], current_time)
            )
            added += 1
        except sqlite3.IntegrityError:
            # Flag already exists
            pass
    
    db.commit()
    return added


def get_queued_flags(limit=None):
    """Get flags ready for submission"""
    import time
    
    db = get_db()
    current_time = time.time()
    cutoff_time = current_time - config.FLAG_LIFETIME
    
    query = '''
        SELECT * FROM flags 
        WHERE status = 'QUEUED' AND time > ?
        ORDER BY time ASC
    '''
    
    if limit:
        query += f' LIMIT {limit}'
    
    return db.execute(query, (cutoff_time,)).fetchall()


def update_flag_status(flag_id, status, response=None):
    """Update flag submission status"""
    db = get_db()
    db.execute(
        'UPDATE flags SET status = ?, checksystem_response = ? WHERE id = ?',
        (status, response, flag_id)
    )
    db.commit()


def get_stats():
    """Get statistics"""
    db = get_db()
    
    stats = {
        'total': db.execute('SELECT COUNT(*) FROM flags').fetchone()[0],
        'queued': db.execute('SELECT COUNT(*) FROM flags WHERE status = "QUEUED"').fetchone()[0],
        'accepted': db.execute('SELECT COUNT(*) FROM flags WHERE status = "ACCEPTED"').fetchone()[0],
        'rejected': db.execute('SELECT COUNT(*) FROM flags WHERE status = "REJECTED"').fetchone()[0],
    }
    
    return stats


def close_db():
    """Close database connection"""
    if hasattr(_local, 'db'):
        _local.db.close()
        del _local.db