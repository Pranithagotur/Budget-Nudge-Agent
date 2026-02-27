# modules/categorization.py

def detect_food_merchants(df):
    """
    Mark transactions that are food delivery
    """
    food_keywords = ["swiggy", "zomato"]

    df['is_food'] = df['merchant'].apply(
        lambda x: any(keyword in x for keyword in food_keywords)
    )

    return df