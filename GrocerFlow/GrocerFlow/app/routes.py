import csv
import io
from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file
from flask_login import login_required

from . import db
from .models import Product, Category, Supplier, StockTransaction
from .forms import CategoryForm, SupplierForm, ProductForm, StockTxForm

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    return redirect(url_for("main.dashboard"))

@main_bp.route("/dashboard")
@login_required
def dashboard():
    total_products = Product.query.count()
    low_stock = Product.query.filter(Product.reorder_level > 0, Product.stock <= Product.reorder_level).order_by(Product.stock.asc()).limit(10).all()
    recent_txs = StockTransaction.query.order_by(StockTransaction.tx_date.desc()).limit(10).all()
    total_categories = Category.query.count()
    total_suppliers = Supplier.query.count()
    return render_template(
        "dashboard.html",
        total_products=total_products,
        total_categories=total_categories,
        total_suppliers=total_suppliers,
        low_stock=low_stock,
        recent_txs=recent_txs
    )

# ---- Categories ----
@main_bp.route("/categories")
@login_required
def categories():
    q = request.args.get("q", "").strip()
    query = Category.query
    if q:
        query = query.filter(Category.name.ilike(f"%{q}%"))
    items = query.order_by(Category.name.asc()).all()
    return render_template("categories/list.html", items=items, q=q)

@main_bp.route("/categories/new", methods=["GET", "POST"])
@login_required
def category_new():
    form = CategoryForm()
    if form.validate_on_submit():
        name = form.name.data.strip()
        if Category.query.filter_by(name=name).first():
            flash("Category already exists.", "warning")
        else:
            db.session.add(Category(name=name))
            db.session.commit()
            flash("Category created.", "success")
            return redirect(url_for("main.categories"))
    return render_template("categories/form.html", form=form, title="New Category")

@main_bp.route("/categories/<int:cat_id>/edit", methods=["GET", "POST"])
@login_required
def category_edit(cat_id):
    item = Category.query.get_or_404(cat_id)
    form = CategoryForm(obj=item)
    if form.validate_on_submit():
        name = form.name.data.strip()
        exists = Category.query.filter(Category.name == name, Category.id != item.id).first()
        if exists:
            flash("Another category already has that name.", "warning")
        else:
            item.name = name
            db.session.commit()
            flash("Category updated.", "success")
            return redirect(url_for("main.categories"))
    return render_template("categories/form.html", form=form, title="Edit Category")

@main_bp.route("/categories/<int:cat_id>/delete", methods=["POST"])
@login_required
def category_delete(cat_id):
    item = Category.query.get_or_404(cat_id)
    if item.products:
        flash("Cannot delete category that has products. Remove products first.", "danger")
    else:
        db.session.delete(item)
        db.session.commit()
        flash("Category deleted.", "success")
    return redirect(url_for("main.categories"))

# ---- Suppliers ----
@main_bp.route("/suppliers")
@login_required
def suppliers():
    q = request.args.get("q", "").strip()
    query = Supplier.query
    if q:
        query = query.filter(Supplier.name.ilike(f"%{q}%"))
    items = query.order_by(Supplier.name.asc()).all()
    return render_template("suppliers/list.html", items=items, q=q)

@main_bp.route("/suppliers/new", methods=["GET", "POST"])
@login_required
def supplier_new():
    form = SupplierForm()
    if form.validate_on_submit():
        name = form.name.data.strip()
        if Supplier.query.filter_by(name=name).first():
            flash("Supplier already exists.", "warning")
        else:
            item = Supplier(
                name=name,
                phone=form.phone.data.strip() if form.phone.data else None,
                email=form.email.data.strip() if form.email.data else None,
                address=form.address.data.strip() if form.address.data else None,
            )
            db.session.add(item)
            db.session.commit()
            flash("Supplier created.", "success")
            return redirect(url_for("main.suppliers"))
    return render_template("suppliers/form.html", form=form, title="New Supplier")

@main_bp.route("/suppliers/<int:supp_id>/edit", methods=["GET", "POST"])
@login_required
def supplier_edit(supp_id):
    item = Supplier.query.get_or_404(supp_id)
    form = SupplierForm(obj=item)
    if form.validate_on_submit():
        name = form.name.data.strip()
        exists = Supplier.query.filter(Supplier.name == name, Supplier.id != item.id).first()
        if exists:
            flash("Another supplier already has that name.", "warning")
        else:
            item.name = name
            item.phone = form.phone.data.strip() if form.phone.data else None
            item.email = form.email.data.strip() if form.email.data else None
            item.address = form.address.data.strip() if form.address.data else None
            db.session.commit()
            flash("Supplier updated.", "success")
            return redirect(url_for("main.suppliers"))
    return render_template("suppliers/form.html", form=form, title="Edit Supplier")

@main_bp.route("/suppliers/<int:supp_id>/delete", methods=["POST"])
@login_required
def supplier_delete(supp_id):
    item = Supplier.query.get_or_404(supp_id)
    if item.products:
        flash("Cannot delete supplier that has products. Remove products first.", "danger")
    else:
        db.session.delete(item)
        db.session.commit()
        flash("Supplier deleted.", "success")
    return redirect(url_for("main.suppliers"))

# ---- Products ----
def _populate_product_form_choices(form: ProductForm):
    cats = Category.query.order_by(Category.name.asc()).all()
    sups = Supplier.query.order_by(Supplier.name.asc()).all()
    form.category_id.choices = [(0, "— None —")] + [(c.id, c.name) for c in cats]
    form.supplier_id.choices = [(0, "— None —")] + [(s.id, s.name) for s in sups]

@main_bp.route("/products")
@login_required
def products():
    q = request.args.get("q", "").strip()
    only_low = request.args.get("low", "").strip() == "1"
    query = Product.query
    if q:
        query = query.filter((Product.name.ilike(f"%{q}%")) | (Product.sku.ilike(f"%{q}%")))
    if only_low:
        query = query.filter(Product.reorder_level > 0, Product.stock <= Product.reorder_level)
    items = query.order_by(Product.name.asc()).all()
    return render_template("products/list.html", items=items, q=q, only_low=only_low)

@main_bp.route("/products/new", methods=["GET", "POST"])
@login_required
def product_new():
    form = ProductForm()
    _populate_product_form_choices(form)

    if form.validate_on_submit():
        sku = form.sku.data.strip()
        if Product.query.filter_by(sku=sku).first():
            flash("SKU already exists. Use a unique SKU.", "warning")
        else:
            item = Product(
                name=form.name.data.strip(),
                sku=sku,
                unit=form.unit.data.strip(),
                category_id=form.category_id.data or None,
                supplier_id=form.supplier_id.data or None,
                price=form.price.data,
                reorder_level=form.reorder_level.data,
                stock=form.stock.data,
            )
            if item.category_id == 0:
                item.category_id = None
            if item.supplier_id == 0:
                item.supplier_id = None

            db.session.add(item)
            db.session.commit()
            flash("Product created.", "success")
            return redirect(url_for("main.products"))
    return render_template("products/form.html", form=form, title="New Product")

@main_bp.route("/products/<int:prod_id>/edit", methods=["GET", "POST"])
@login_required
def product_edit(prod_id):
    item = Product.query.get_or_404(prod_id)
    form = ProductForm(obj=item)
    _populate_product_form_choices(form)

    # Ensure initial selects are set (use 0 for None)
    if request.method == "GET":
        form.category_id.data = item.category_id or 0
        form.supplier_id.data = item.supplier_id or 0

    if form.validate_on_submit():
        sku = form.sku.data.strip()
        exists = Product.query.filter(Product.sku == sku, Product.id != item.id).first()
        if exists:
            flash("Another product already has that SKU.", "warning")
        else:
            item.name = form.name.data.strip()
            item.sku = sku
            item.unit = form.unit.data.strip()
            item.category_id = form.category_id.data or None
            item.supplier_id = form.supplier_id.data or None
            if item.category_id == 0:
                item.category_id = None
            if item.supplier_id == 0:
                item.supplier_id = None
            item.price = form.price.data
            item.reorder_level = form.reorder_level.data
            # Do not overwrite stock here (stock is adjusted by transactions)
            db.session.commit()
            flash("Product updated.", "success")
            return redirect(url_for("main.products"))
    return render_template("products/form.html", form=form, title="Edit Product")

@main_bp.route("/products/<int:prod_id>/delete", methods=["POST"])
@login_required
def product_delete(prod_id):
    item = Product.query.get_or_404(prod_id)
    if item.transactions:
        flash("Cannot delete product with transactions. Delete transactions first.", "danger")
    else:
        db.session.delete(item)
        db.session.commit()
        flash("Product deleted.", "success")
    return redirect(url_for("main.products"))

@main_bp.route("/products/<int:prod_id>")
@login_required
def product_detail(prod_id):
    item = Product.query.get_or_404(prod_id)
    txs = StockTransaction.query.filter_by(product_id=item.id).order_by(StockTransaction.tx_date.desc()).limit(50).all()
    form = StockTxForm()
    return render_template("products/detail.html", item=item, txs=txs, form=form)

@main_bp.route("/products/<int:prod_id>/transaction", methods=["POST"])
@login_required
def product_transaction(prod_id):
    item = Product.query.get_or_404(prod_id)
    form = StockTxForm()
    if form.validate_on_submit():
        qty = int(form.quantity.data)
        tx_type = form.tx_type.data
        if tx_type == "OUT" and qty > item.stock:
            flash("Not enough stock for Stock Out.", "danger")
            return redirect(url_for("main.product_detail", prod_id=item.id))

        if tx_type == "IN":
            item.stock += qty
        else:
            item.stock -= qty

        tx = StockTransaction(
            product_id=item.id,
            tx_type=tx_type,
            quantity=qty,
            reference=form.reference.data.strip() if form.reference.data else None,
            note=form.note.data.strip() if form.note.data else None,
            tx_date=datetime.utcnow()
        )
        db.session.add(tx)
        db.session.commit()
        flash("Transaction recorded.", "success")
    else:
        flash("Please correct the errors in the transaction form.", "warning")
    return redirect(url_for("main.product_detail", prod_id=item.id))

# ---- Transactions ----
@main_bp.route("/transactions")
@login_required
def transactions():
    q = request.args.get("q", "").strip()
    tx_type = request.args.get("type", "").strip()  # IN/OUT/blank
    query = StockTransaction.query.join(Product)
    if q:
        query = query.filter((Product.name.ilike(f"%{q}%")) | (Product.sku.ilike(f"%{q}%")) | (StockTransaction.reference.ilike(f"%{q}%")))
    if tx_type in ("IN", "OUT"):
        query = query.filter(StockTransaction.tx_type == tx_type)
    items = query.order_by(StockTransaction.tx_date.desc()).limit(500).all()
    return render_template("transactions/list.html", items=items, q=q, tx_type=tx_type)

# ---- Exports ----
@main_bp.route("/export/inventory.csv")
@login_required
def export_inventory():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["SKU", "Product", "Category", "Supplier", "Unit", "Price", "Reorder Level", "Stock"])
    for p in Product.query.order_by(Product.name.asc()).all():
        writer.writerow([
            p.sku,
            p.name,
            p.category.name if p.category else "",
            p.supplier.name if p.supplier else "",
            p.unit,
            p.price,
            p.reorder_level,
            p.stock,
        ])
    mem = io.BytesIO(output.getvalue().encode("utf-8"))
    return send_file(mem, mimetype="text/csv", as_attachment=True, download_name="grocerflow_inventory.csv")

@main_bp.route("/export/transactions.csv")
@login_required
def export_transactions():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Date (UTC)", "Type", "SKU", "Product", "Qty", "Reference", "Note"])
    items = StockTransaction.query.join(Product).order_by(StockTransaction.tx_date.desc()).all()
    for tx in items:
        writer.writerow([
            tx.tx_date.isoformat(sep=" ", timespec="seconds"),
            tx.tx_type,
            tx.product.sku,
            tx.product.name,
            tx.quantity,
            tx.reference or "",
            tx.note or "",
        ])
    mem = io.BytesIO(output.getvalue().encode("utf-8"))
    return send_file(mem, mimetype="text/csv", as_attachment=True, download_name="grocerflow_transactions.csv")
