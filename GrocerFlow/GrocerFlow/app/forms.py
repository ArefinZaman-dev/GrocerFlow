from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, FloatField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Optional, NumberRange

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(max=80)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=4, max=128)])
    remember = BooleanField("Remember me")
    submit = SubmitField("Login")

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField("Current password", validators=[DataRequired()])
    new_password = PasswordField("New password", validators=[DataRequired(), Length(min=6, max=128)])
    submit = SubmitField("Update Password")

class CategoryForm(FlaskForm):
    name = StringField("Category name", validators=[DataRequired(), Length(max=120)])
    submit = SubmitField("Save")

class SupplierForm(FlaskForm):
    name = StringField("Supplier name", validators=[DataRequired(), Length(max=120)])
    phone = StringField("Phone", validators=[Optional(), Length(max=40)])
    email = StringField("Email", validators=[Optional(), Length(max=120)])
    address = StringField("Address", validators=[Optional(), Length(max=255)])
    submit = SubmitField("Save")

class ProductForm(FlaskForm):
    name = StringField("Product name", validators=[DataRequired(), Length(max=200)])
    sku = StringField("SKU", validators=[DataRequired(), Length(max=80)])
    unit = StringField("Unit (e.g., pcs, kg)", validators=[DataRequired(), Length(max=40)])
    category_id = SelectField("Category", coerce=int, validators=[Optional()])
    supplier_id = SelectField("Supplier", coerce=int, validators=[Optional()])
    price = FloatField("Unit price", validators=[DataRequired(), NumberRange(min=0)])
    reorder_level = IntegerField("Reorder level", validators=[DataRequired(), NumberRange(min=0)])
    stock = IntegerField("Opening stock", validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField("Save")

class StockTxForm(FlaskForm):
    tx_type = SelectField("Type", choices=[("IN","Stock In"), ("OUT","Stock Out")], validators=[DataRequired()])
    quantity = IntegerField("Quantity", validators=[DataRequired(), NumberRange(min=1)])
    reference = StringField("Reference (optional)", validators=[Optional(), Length(max=120)])
    note = TextAreaField("Note (optional)", validators=[Optional(), Length(max=255)])
    submit = SubmitField("Record Transaction")
