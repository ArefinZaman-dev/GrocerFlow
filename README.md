````md
# 🛒 GrocerFlow — Web-based Inventory Management System

GrocerFlow is a lightweight, ready-to-run **inventory management web app** designed for small grocery shops.  
Built with **Flask + SQLite**, it helps you manage products, track stock, record stock in/out transactions, and export reports.

---

## 🌟 Overview

GrocerFlow provides a clean and practical inventory workflow with authentication, product management, transaction logging, low-stock alerts, and CSV exports — making it ideal for small businesses and academic projects.

---

## 🚀 Features

### 🔐 Authentication & User Management
- Secure login system (Flask-Login)
- Password hashing and session management
- Profile page with password change option

### 🧾 Product Management
- Add / edit / delete products
- Track:
  - SKU
  - Category
  - Supplier
  - Price
  - Reorder level
  - Stock quantity

### 📦 Inventory Transactions
- Stock **IN / OUT** transactions
- Automatic stock update on each transaction
- Full transaction history

### 📊 Dashboard & Insights
- Key statistics overview
- Low-stock product list (based on reorder level)
- Quick navigation to major modules

### 📤 Export & Reports
- Export inventory report to CSV
- Export transactions report to CSV

---

## 🛠 Technology Stack

### Backend
- **Python** + **Flask**
- **Flask-SQLAlchemy** (ORM)

### Database
- **SQLite** (auto-created)

### Auth & Forms
- **Flask-Login**
- **Flask-WTF**
- **Werkzeug Security** (password hashing)

### Configuration
- **python-dotenv** for environment variables

---

## 📁 Project Structure

```text
GrocerFlow/
├─ app/
│  ├─ __init__.py             # App factory & configuration
│  ├─ models.py               # Database models
│  ├─ routes.py               # Main routes (dashboard, products, transactions, exports)
│  ├─ auth.py                 # Authentication (login/logout/profile)
│  ├─ forms.py                # Flask-WTF forms
│  ├─ seed.py                 # Default admin creation on first run
│  ├─ templates/              # Jinja2 templates
│  └─ static/                 # CSS/JS/images
├─ instance/
│  └─ grocerflow.db           # SQLite DB (auto-created, ignored by git)
├─ .env.example               # Example environment variables
├─ .gitignore
├─ requirements.txt
├─ run.py                     # App entry point
└─ README.md
````

---

## ✅ Requirements

* Python **3.9+**
* pip

---

## 🚀 Installation & Setup

### 1) Clone the Repository

```bash
git clone https://github.com/ArefinZaman-dev/GrocerFlow.git
cd GrocerFlow
```

### 2) Create & Activate Virtual Environment

**Windows (PowerShell):**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3) Install Dependencies

```bash
pip install -r requirements.txt
```

### 4) Setup Environment Variables

Copy the example env file:

**Windows (PowerShell):**

```powershell
copy .env.example .env
```

**macOS / Linux:**

```bash
cp .env.example .env
```

Edit `.env` (recommended to change `SECRET_KEY`).

Example `.env`:

```env
FLASK_ENV=production
SECRET_KEY=change-me-please
DATABASE_URL=sqlite:///grocerflow.db
```

### 5) Run the App

```bash
python run.py
```

Open in browser:
👉 [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🔑 Default Admin Login (First Run)

On the very first run, GrocerFlow automatically creates a default admin account **if the database is empty**:

* **Username:** `admin`
* **Password:** `admin123`

✅ **Important:** Log in and change the password immediately from the **Profile** page.

---

## 📌 Main Pages / Routes

* Dashboard: `/dashboard`
* Categories: `/categories`
* Suppliers: `/suppliers`
* Products: `/products`
* Transactions: `/transactions`
* Export Inventory CSV: `/export/inventory.csv`
* Export Transactions CSV: `/export/transactions.csv`
* Login: `/auth/login`
* Profile (Change Password): `/auth/profile`

---

## 🗃️ Database Notes

* SQLite database is created automatically at:

  * `instance/grocerflow.db`

* You can change database location/type using `DATABASE_URL` in `.env`.

Example (PostgreSQL):

```env
DATABASE_URL=postgresql://user:pass@localhost:5432/grocerflow
```

---

## 🔒 Security Notes

* Do **NOT** upload your `.env` file to GitHub
* Always use a strong `SECRET_KEY` for production
* Change the default admin password immediately

---

## 🌐 Deployment (Simple Production Tips)

For production, run behind a WSGI server (example: **gunicorn**) and a reverse proxy (nginx).

```bash
pip install gunicorn
gunicorn -w 2 -b 0.0.0.0:5000 run:app
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a new branch: `feature/my-feature`
3. Commit your changes
4. Push to your branch
5. Open a Pull Request

---

## 👨‍💻 Developer Info

**Author:** Shaikh Arefin Zaman
**Project Type:** Full Stack (Flask)
**Email:** [arefinzamandev@gmail.com](mailto:arefinzamandev@gmail.com)

---

## 📞 Support

For support, email **[arefinzamandev@gmail.com](mailto:arefinzamandev@gmail.com)** or open an issue in the repository.

---

## 📄 License

This project is open-source and available under the **MIT License**.
You’re free to modify and distribute it with proper credit.

---

## 🙏 Acknowledgments

* Flask community for the framework ecosystem
* SQLAlchemy for database ORM
* Flask-Login for session-based authentication
* Flask-WTF for form handling and validation

```
```
