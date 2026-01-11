def currency(value):
    try:
        return f"{float(value):,.2f}"
    except Exception:
        return value
