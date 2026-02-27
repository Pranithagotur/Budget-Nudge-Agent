# modules/addiction_score.py

def calculate_addiction_score(order_count,
                               total_food_spend,
                               total_spend,
                               late_ratio,
                               vendor_ratio,
                               projected_spend,
                               limit):

    # Frequency weight (30)
    freq_score = min(order_count * 2, 30)

    # Food % weight (30)
    if total_spend == 0:
        spend_score = 0
    else:
        food_percent = (total_food_spend / total_spend) * 100
        spend_score = min(food_percent, 30)

    # Late night weight (20)
    late_score = late_ratio * 20

    # Vendor dependency weight (10)
    vendor_score = vendor_ratio * 10

    # Projection weight (10)
    projection_score = 10 if projected_spend > limit else 0

    total_score = freq_score + spend_score + late_score + vendor_score + projection_score

    return round(total_score, 2)
def financial_health_index(addiction_score):
    """
    Financial Health Index (100 - addiction score)
    Higher is better
    """
    fhi = 100 - addiction_score
    return round(fhi, 2)