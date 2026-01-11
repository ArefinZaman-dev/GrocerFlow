from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db

class TimestampMixin:
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

class User(UserMixin, TimestampMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

class Category(TimestampMixin, db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False, index=True)

    def __repr__(self):
        return f"<Category {self.name}>"

class Supplier(TimestampMixin, db.Model):
    __tablename__ = "suppliers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(40), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    address = db.Column(db.String(255), nullable=True)

class Product(TimestampMixin, db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    sku = db.Column(db.String(80), unique=True, nullable=False, index=True)
    unit = db.Column(db.String(40), default="pcs", nullable=False)

    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey("suppliers.id"), nullable=True)

    category = db.relationship("Category", backref=db.backref("products", lazy=True))
    supplier = db.relationship("Supplier", backref=db.backref("products", lazy=True))

    price = db.Column(db.Float, default=0.0, nullable=False)
    reorder_level = db.Column(db.Integer, default=0, nullable=False)
    stock = db.Column(db.Integer, default=0, nullable=False)

    def is_low_stock(self) -> bool:
        return self.reorder_level > 0 and self.stock <= self.reorder_level

class StockTransaction(TimestampMixin, db.Model):
    __tablename__ = "stock_transactions"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False, index=True)
    tx_type = db.Column(db.String(10), nullable=False)  # IN or OUT
    quantity = db.Column(db.Integer, nullable=False)
    reference = db.Column(db.String(120), nullable=True)
    note = db.Column(db.String(255), nullable=True)
    tx_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)

    product = db.relationship("Product", backref=db.backref("transactions", lazy=True, order_by="desc(StockTransaction.tx_date)"))
