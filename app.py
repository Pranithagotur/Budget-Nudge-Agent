from flask import Flask, render_template
from plyer import notification
import logging
import os

from modules.data_loader import load_csv
from modules.categorization import detect_food_merchants
from modules.spend_analysis import (
    calculate_food_summary,
    threshold_check,
    vendor_dependency,
    late_night_detector,
    spending_anomaly,
    project_month_end
)
from modules.addiction_score import calculate_addiction_score, financial_health_index
from modules.risk_engine import classify_behavior
from modules.growth_analysis import week_over_week_growth


app = Flask(__name__)

# ======================
# Professional Logging Setup
# ======================

if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

@app.route("/")
def dashboard():
    try:
        file_path = "data.csv"
        df = load_csv(file_path)
        df = detect_food_merchants(df)

        food_df, total_food_spend, order_count = calculate_food_summary(df)
        total_spend = df['amount'].sum()

        vendor_ratio, top_vendor = vendor_dependency(food_df)
        late_ratio = late_night_detector(df)
        anomalies = spending_anomaly(food_df)

        limit = 3000
        projected_spend = project_month_end(food_df)

        addiction_score = calculate_addiction_score(
            order_count,
            total_food_spend,
            total_spend,
            late_ratio,
            vendor_ratio,
            projected_spend,
            limit
        )

        risk_level = classify_behavior(addiction_score)
        growth_percentage = week_over_week_growth(df)
        fhi = financial_health_index(addiction_score)

        logging.info("Dashboard loaded successfully")

        # ===============================
        # Desktop Notification System
        # ===============================

        if total_food_spend > limit:
            notification.notify(
                title="Budget Alert 🚨",
                message=f"You exceeded ₹{limit}. Current spend: ₹{total_food_spend}.",
                timeout=5
            )

        if addiction_score > 60:
            notification.notify(
                title="High Risk Spending ⚠",
                message="Your food delivery dependency is high. Consider reducing orders.",
                timeout=5
            )

        if growth_percentage > 20:
            notification.notify(
                title="Spending Growth Alert 📈",
                message=f"Your spending increased by {growth_percentage}%.",
                timeout=5
            )

        return render_template(
            "dashboard.html",
            total_spend=total_spend,
            food_spend=total_food_spend,
            order_count=order_count,
            vendor_ratio=round(vendor_ratio*100, 2),
            top_vendor=top_vendor,
            late_ratio=round(late_ratio*100, 2),
            projected_spend=projected_spend,
            addiction_score=addiction_score,
            risk_level=risk_level,
            fhi=fhi,
            growth=growth_percentage,
            anomalies=len(anomalies)
        )

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return "Something went wrong. Check logs."


if __name__ == "__main__":
    app.run(debug=True)