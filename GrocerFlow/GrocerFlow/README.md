# GrocerFlow (Web-based Inventory Management System)

GrocerFlow is a lightweight, ready-to-run inventory management system for small grocery shops.

## Features
- Secure login (Flask-Login) with password hashing
- Products CRUD (SKU, category, supplier, price, reorder level, stock)
- Stock IN / Stock OUT transactions (auto-updates product stock)
- Dashboard with key stats and low-stock list
- Search & filter products
- CSV export (inventory + transactions)
- SQLite database (no setup required)

## Quick start

### 0) Open a terminal in the project folder
Make sure you're inside the extracted `GrocerFlow/` folder (the same folder that contains `requirements.txt` and `run.py`).

### 1) Create & activate a virtual environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If activation is blocked, run this once and try again:
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

**Windows (CMD):**
```bat
python -m venv .venv
.venv\Scripts\activate.bat
```

**macOS/Linux (bash/zsh):**
```bash
python -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies
```bash
pip install -r requirements.txt
```

### 3) Configure environment (optional)
Copy `.env.example` to `.env` and edit if you want.
```bash
cp .env.example .env
```

### 4) Run the app
```bash
python run.py
```

Then open:
- http://127.0.0.1:5000

## Default Admin
On the very first run, GrocerFlow automatically creates a default admin account if the database is empty:

- **Username:** admin
- **Password:** admin123

**Important:** Log in and change the password immediately from the profile menu.

## Notes
- The SQLite database file is created under `instance/grocerflow.db`.
- For production, consider running behind a WSGI server (gunicorn/uwsgi) and using a stronger SECRET_KEY.

## License
MIT
