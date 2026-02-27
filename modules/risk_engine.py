# modules/risk_engine.py

def classify_behavior(addiction_score):
    """
    Classify user into behavioral risk category
    """

    if addiction_score < 30:
        return "Healthy"
    elif addiction_score < 60:
        return "Moderate Risk"
    elif addiction_score < 80:
        return "High Risk"
    else:
        return "Critical Overspending"