# modules/data_loader.py

import pandas as pd

def load_csv(file):
    """
    Load CSV and clean basic fields
    Expected columns: date, merchant, amount, time (optional)
    """
    df = pd.read_csv(file)

    # Standardize column names
    df.columns = df.columns.str.lower().str.strip()

    # Convert date
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # Convert amount
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')

    # Lowercase merchant names
    df['merchant'] = df['merchant'].str.lower()

    # Drop invalid rows
    df = df.dropna(subset=['date', 'merchant', 'amount'])

    return df


def add_manual_entry(df, date, merchant, amount):
    """
    Add a new manual transaction
    """
    new_row = pd.DataFrame({
        'date': [pd.to_datetime(date)],
        'merchant': [merchant.lower()],
        'amount': [float(amount)]
    })

    df = pd.concat([df, new_row], ignore_index=True)
    return df