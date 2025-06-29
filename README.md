## Simple Clinic Flask App

This is a simple Flask application for collecting patient data. It includes basic form validation, SQLite integration, and a confirmation page upon successful submission.

---

## How to Run This App

1. **Create a virtual environment:**

   ```bash
    python -m venv venv
    source venv/bin/activate      # macOS/Linux
    venv\Scripts\activate         # Windows

   ```

2. **Install Dependencies:**

   ```bash
    pip install -r requirements.txt

   ```

3. **Run the flask app**

   ```bash
    python app.py

   ```

4. **Open your browser and go to**

   ```bash
    http://127.0.0.1:5000

   ```

The database file (patients.db) will be created automatically when the app runs for the first time.

## Add-On Questions & Answers

### 1. Explain how your app handles form validation. What happens if a required field is missing or the date is in the future?

In the `/submit` route, the app first checks if any of the fields — first name, last name, date of birth, or therapist name — are empty. If any are missing, an error message is shown above the form and the submitted values are preserved so the user doesn’t have to re-enter everything.

For the date of birth, I validate that it's in the past using Python’s `datetime` module. If the user enters a future date or an invalid format, another specific error message is shown. These validations ensure that bad data doesn’t get saved to the database while keeping the user experience clear and simple.

---

### 2. If we wanted to extend the app to support therapist logins, how would you structure that?

To support logins, I would add basic authentication using Flask’s session system, and store therapist accounts in a separate `therapists` table with `username`, `hashed_password`, and possibly a `role`.

**Here’s how I’d structure it:**

- Create a login route (`/login`) that checks submitted credentials against the DB.
- Use Werkzeug to hash passwords securely.
- Store the logged-in therapist’s ID in the session so we can tie future submissions to them if needed.
- Add a logout route to clear the session.

**For organization, I’d break the app into blueprints:**

- `auth.py` for login/logout
- `main.py` for the current patient form and confirmation

This keeps things modular and more scalable if the app grows.

If security becomes more important (e.g., for production), I’d move toward Flask-Login or Flask-Security for more robust session handling and permission management.

---

### 3. How would you deploy this app to a HIPAA-compliant cloud environment?

Deploying to a HIPAA-compliant environment means protecting data both in transit and at rest, and ensuring access control is strictly enforced.

**Here’s how I’d approach it:**

- Use a provider like AWS or Azure that offers HIPAA-eligible services.
- Host the app behind a secure reverse proxy (e.g., Nginx), served via HTTPS with TLS certificates.
- Store the database in a managed, encrypted volume (like AWS RDS or EBS with encryption enabled).
- Add authentication (see #2), limit access to only authorized users, and apply role-based permissions.
- Enable logging and monitoring with alerts for suspicious activity.
- Set up automatic backups of the database and enable audit trails.
- Use environment variables for secrets (not hard-coded), and rotate them regularly.
- If storing any PHI (Protected Health Information), ensure Business Associate Agreements (BAAs) are in place with all providers involved.

I’d also make sure to follow the Minimum Necessary Rule and not store or expose any more patient data than required for the task.

---

### 4. Where would you place the code that initializes the database and why?

I placed the `init_db()` function directly in `app.py` and call it right before starting the Flask server. This keeps the setup simple and self-contained, which is ideal for a mini-project.

In a larger app, I’d separate it into a utility module like `db_utils.py` or `models.py` and possibly create a CLI command or startup script to initialize or migrate the database. But since this app only has one table and a short setup time, calling `init_db()` on app launch was the most straightforward and readable solution.
