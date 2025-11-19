"""
Application Tracker - Tracks job applications in SQLite database
"""

import sqlite3
from datetime import datetime
from typing import List, Dict
import json


class ApplicationTracker:
    """Track job applications in local database"""

    def __init__(self, db_path: str = "data/applications.db"):
        self.db_path = db_path
        self._init_database()

    def _init_database(self):
        """Initialize SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create applications table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_title TEXT,
                company TEXT,
                location TEXT,
                url TEXT,
                source TEXT,
                match_score INTEGER,
                status TEXT,
                applied_date TEXT,
                follow_up_date TEXT,
                notes TEXT
            )
        ''')

        # Create jobs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_title TEXT,
                company TEXT,
                location TEXT,
                url TEXT UNIQUE,
                source TEXT,
                match_score INTEGER,
                date_found TEXT,
                job_data TEXT
            )
        ''')

        conn.commit()
        conn.close()

    def log_application(self, job: Dict, status: str = "applied"):
        """Log a job application"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO applications (job_title, company, location, url, source, match_score, status, applied_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            job.get('title'),
            job.get('company'),
            job.get('location'),
            job.get('url'),
            job.get('source'),
            job.get('match_score', 0),
            status,
            datetime.now().isoformat()
        ))

        conn.commit()
        conn.close()

    def save_jobs(self, matched_jobs: Dict):
        """Save all found jobs to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        for category in matched_jobs:
            for job in matched_jobs[category]:
                try:
                    cursor.execute('''
                        INSERT OR IGNORE INTO jobs (job_title, company, location, url, source, match_score, date_found, job_data)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        job.get('title'),
                        job.get('company'),
                        job.get('location'),
                        job.get('url'),
                        job.get('source'),
                        job.get('match_score', 0),
                        datetime.now().isoformat(),
                        json.dumps(job)
                    ))
                except Exception as e:
                    print(f"Error saving job: {str(e)}")
                    continue

        conn.commit()
        conn.close()

    def get_application_history(self, days: int = 30) -> List[Dict]:
        """Get application history for the last N days"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM applications
            WHERE applied_date >= date('now', '-' || ? || ' days')
            ORDER BY applied_date DESC
        ''', (days,))

        rows = cursor.fetchall()
        conn.close()

        return [self._row_to_dict(row) for row in rows]

    def _row_to_dict(self, row) -> Dict:
        """Convert database row to dictionary"""
        return {
            'id': row[0],
            'job_title': row[1],
            'company': row[2],
            'location': row[3],
            'url': row[4],
            'source': row[5],
            'match_score': row[6],
            'status': row[7],
            'applied_date': row[8],
            'follow_up_date': row[9],
            'notes': row[10]
        }
