/* ============================
   STATE
============================ */

const state = {
    data: backendData,
    personality: "supportive"
};

/* ============================
   HERO METRICS UPDATE
============================ */

function updateDashboard() {

    document.getElementById("budgetAmount").textContent =
        state.data.projectedSpend.toLocaleString();

    document.getElementById("totalSpend").textContent =
        state.data.totalSpend.toLocaleString();

    document.getElementById("overspendAmount").textContent =
        Math.max(0, state.data.totalSpend - state.data.projectedSpend).toLocaleString();

    const riskElement = document.getElementById("riskLevel");
    riskElement.textContent = state.data.riskLevel;

    riskElement.className = "";

    if (state.data.riskLevel === "High Risk")
        riskElement.classList.add("risk-high");
    else if (state.data.riskLevel === "Medium Risk")
        riskElement.classList.add("risk-medium");
    else
        riskElement.classList.add("risk-low");

    generateInsight();
}

/* ============================
   INSIGHT ENGINE
============================ */

function generateInsight() {

    const insightText = document.getElementById("insightText");

    if (state.data.addictionScore > 60) {
        insightText.textContent =
            "⚠️ Your food spending behavior indicates high dependency. Consider reducing frequency.";
    } else if (state.data.addictionScore > 40) {
        insightText.textContent =
            "📊 Moderate behavioral risk detected. Small habit changes can improve financial health.";
    } else {
        insightText.textContent =
            "🎯 Excellent control over spending habits. Keep it consistent!";
    }
}

/* ============================
   NUDGE GENERATOR
============================ */

function generateNudge() {

    const personality = document.getElementById("personalitySelector").value;

    let message = "";

    if (state.data.riskLevel === "High Risk") {
        if (personality === "funny")
            message = "Swiggy is not your life partner. Break up before your wallet does.";
        else if (personality === "strict")
            message = "Immediate spending correction required. Reduce food orders.";
        else
            message = "Let's slowly reduce your food delivery frequency. Small steps work!";
    } else {
        message = "You are in control. Keep maintaining discipline.";
    }

    document.getElementById("nudgeMessage").textContent = message;
    document.getElementById("nudgePersonality").textContent = personality;
}

/* ============================
   EVENT LISTENERS
============================ */

document.addEventListener("DOMContentLoaded", () => {

    updateDashboard();

    document
        .getElementById("generateNudgeBtn")
        .addEventListener("click", generateNudge);

});