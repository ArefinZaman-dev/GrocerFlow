from . import db
from .models import User

def ensure_default_admin():
    # Create a default admin if there are no users yet
    if User.query.count() == 0:
        admin = User(username="admin", is_admin=True)
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()
