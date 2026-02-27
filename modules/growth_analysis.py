# modules/growth_analysis.py

import pandas as pd

def week_over_week_growth(df):
    """
    Compare last 7 days vs previous 7 days food spending
    """

    df = df.sort_values("date")

    # Filter only food transactions
    food_df = df[df['is_food'] == True]

    if len(food_df) < 14:
        return 0

    last_date = food_df['date'].max()

    last_week = food_df[
        food_df['date'] >= last_date - pd.Timedelta(days=7)
    ]

    previous_week = food_df[
        (food_df['date'] < last_date - pd.Timedelta(days=7)) &
        (food_df['date'] >= last_date - pd.Timedelta(days=14))
    ]

    last_week_total = last_week['amount'].sum()
    previous_week_total = previous_week['amount'].sum()

    if previous_week_total == 0:
        return 0

    growth_percentage = ((last_week_total - previous_week_total) /
                         previous_week_total) * 100

    return round(growth_percentage, 2)