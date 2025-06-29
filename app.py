from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

DB_NAME = 'patients.db'


# Initialize DB if not exists
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                dob TEXT NOT NULL,
                therapist_name TEXT NOT NULL
            )
        ''')
        conn.commit()

# Show form
@app.route('/')
def form():
    return render_template('form.html', error=None)

# Handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    first_name = request.form.get('first_name', '').strip()
    last_name = request.form.get('last_name', '').strip()
    dob = request.form.get('dob', '').strip()
    therapist = request.form.get('therapist', '').strip()

    error = None

    # Basic validation
    if not first_name or not last_name or not dob or not therapist:
        error = "All fields are required."
    else:
        try:
            dob_date = datetime.strptime(dob, "%Y-%m-%d")
            if dob_date >= datetime.now():
                error = "Date of birth must be in the past."
        except ValueError:
            error = "Invalid date format. Use YYYY-MM-DD."

    if error:
        return render_template('form.html', error=error,
                               first_name=first_name,
                               last_name=last_name,
                               dob=dob,
                               therapist=therapist)

    # Save to database
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO patients (first_name, last_name, dob, therapist_name)
            VALUES (?, ?, ?, ?)
        ''', (first_name, last_name, dob, therapist))
        conn.commit()

    return render_template('confirmation.html',
                           first_name=first_name,
                           last_name=last_name,
                           dob=dob,
                           therapist=therapist)

import os

# Run
if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

