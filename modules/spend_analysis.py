# modules/spend_analysis.py

import pandas as pd


def monthly_aggregation(df):
    df['month'] = df['date'].dt.month
    return df.groupby('month')['amount'].sum()


def calculate_food_summary(df):
    food_df = df[df['is_food'] == True]

    total_food_spend = food_df['amount'].sum()
    order_count = len(food_df)

    return food_df, total_food_spend, order_count


def threshold_check(total_spend, limit):
    return total_spend > limit


def vendor_dependency(food_df):
    if len(food_df) == 0:
        return 0, None

    vendor_counts = food_df['merchant'].value_counts()
    top_vendor = vendor_counts.idxmax()
    ratio = vendor_counts.max() / len(food_df)

    return ratio, top_vendor


def late_night_detector(df):
    if 'time' not in df.columns:
        return 0

    df['hour'] = pd.to_datetime(df['time'], errors='coerce').dt.hour
    late_orders = df[(df['is_food']) & (df['hour'] >= 22)]

    if len(df[df['is_food']]) == 0:
        return 0

    ratio = len(late_orders) / len(df[df['is_food']])
    return ratio


def spending_anomaly(food_df):
    if len(food_df) == 0:
        return pd.DataFrame()

    avg = food_df['amount'].mean()
    anomalies = food_df[food_df['amount'] > avg * 2]

    return anomalies


def project_month_end(food_df):
    if len(food_df) == 0:
        return 0

    days_so_far = food_df['date'].dt.day.max()
    current_total = food_df['amount'].sum()

    projected_total = (current_total / days_so_far) * 30
    return round(projected_total, 2)