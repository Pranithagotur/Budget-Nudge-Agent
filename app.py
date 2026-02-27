from flask import Flask, render_template, request
import pandas as pd
import logging
import os

# ✅ IMPORT NUDGE GENERATOR
from modules.nudge_generator import generate_nudge

app = Flask(__name__)

# ======================
# Logging Setup
# ======================

if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ======================
# 1️⃣ LANDING PAGE
# ======================

@app.route("/")
def landing():
    return render_template("landing.html")


# ======================
# 2️⃣ LOGIN PAGE
# ======================

@app.route("/login")
def login():
    return render_template("login.html")


# ======================
# 3️⃣ DASHBOARD AFTER LOGIN
# ======================

@app.route("/dashboard", methods=["POST"])
def dashboard():

    name = request.form["name"]
    salary = int(request.form["salary"])
    expenses = int(request.form["expenses"])
    emi = int(request.form["emi"])

    total_deductions = expenses + emi
    net_income = salary - total_deductions
    suggested_food_budget = int(net_income * 0.25)

    return render_template(
        "dashboard.html",
        name=name,
        salary=salary,
        total_deductions=total_deductions,
        net_income=net_income,
        suggested_food_budget=suggested_food_budget,
        analysis=False
    )


# ======================
# 4️⃣ FULL ANALYSIS AFTER CSV UPLOAD
# ======================

@app.route("/analyze", methods=["POST"])
def analyze():
    try:

        # User profile data
        name = request.form.get("name")
        salary = int(request.form.get("salary", 0))
        expenses = int(request.form.get("expenses", 0))
        emi = int(request.form.get("emi", 0))

        total_deductions = expenses + emi
        net_income = salary - total_deductions
        suggested_food_budget = int(net_income * 0.25)

        # Food limit + file
        food_limit = int(request.form.get("food_limit", 0))
        file = request.files.get("file")

        if not file:
            return "No file uploaded"

        df = pd.read_csv(file)

        if "amount" not in df.columns:
            return "CSV must contain 'amount' column"

        total_food_spend = df["amount"].sum()
        order_count = len(df)
        projected_spend = round(total_food_spend * 1.2, 2)

        risk_level = "High Risk" if total_food_spend > food_limit else "Low Risk"

        # Default behavioral values
        addiction_score = 0
        late_ratio = 0
        growth = 0

        # ✅ Now matches function definition
        nudge_message = generate_nudge(
    total_food_spend,
    food_limit,
    addiction_score
)

        logging.info("Analysis completed successfully")

        return render_template(
            "dashboard.html",
            name=name,
            salary=salary,
            total_deductions=total_deductions,
            net_income=net_income,
            suggested_food_budget=suggested_food_budget,

            analysis=True,
            total_spend=total_food_spend,
            food_spend=total_food_spend,
            order_count=order_count,
            projected_spend=projected_spend,
            risk_level=risk_level,
            nudge=nudge_message
        )

    except Exception as e:
        logging.error(str(e))
        return str(e)


if __name__ == "__main__":
    app.run(debug=True)