def clean_amount(value):
    """Clean amount string by removing thousand separators and converting to float."""
    value = value.strip()  # Remove any extra spaces
    if value:  # If value is not empty
        return float(value.replace("'", "").replace(",", "."))
    return 0.0  # Return 0 if the value is empty
