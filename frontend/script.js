// ============================================================
// SMART LOAN AI - FRONTEND JAVASCRIPT
// ============================================================

const API_URL = "http://127.0.0.1:8000/predict";


// ============================================================
// SECTION NAVIGATION
// ============================================================

function showSection(sectionId) {

    const sections = document.querySelectorAll(".page-section");

    sections.forEach(function (section) {
        section.classList.remove("active-section");
    });

    const selectedSection = document.getElementById(sectionId);

    if (selectedSection) {
        selectedSection.classList.add("active-section");
    }


    // Update active sidebar item

    const navItems = document.querySelectorAll(".nav-item");

    navItems.forEach(function (item) {
        item.classList.remove("active");
    });

    navItems.forEach(function (item) {

        const text = item.innerText.toLowerCase();

        if (
            sectionId === "dashboard" &&
            text.includes("dashboard")
        ) {
            item.classList.add("active");
        }

        if (
            sectionId === "prediction" &&
            text.includes("new prediction")
        ) {
            item.classList.add("active");
        }

        if (
            sectionId === "history" &&
            text.includes("prediction history")
        ) {
            item.classList.add("active");
        }
    });


    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });

    // Reset form whenever New Prediction is opened
    if (sectionId === "prediction") {
        const loanForm = document.getElementById("loanForm");

        if (loanForm) {
            loanForm.reset();
        }
    }

    // Refresh history

    if (sectionId === "history") {
        displayHistory();
    }


    // Refresh dashboard

    if (sectionId === "dashboard") {
        updateDashboardStatistics();
    }


    // When opening a fresh prediction page,
    // hide the historical result banner.

    if (sectionId === "prediction") {

        const historicalBanner =
            document.getElementById("historicalResultBanner");

        if (historicalBanner) {
            historicalBanner.classList.add("hidden");
        }
    }
}



// ============================================================
// NUMBER FORMATTER
// ============================================================

function formatNumber(value) {

    if (
        value === null ||
        value === undefined ||
        value === ""
    ) {
        return "0";
    }

    return Number(value).toLocaleString("en-IN");
}



// ============================================================
// SAVE PREDICTION TO HISTORY
// ============================================================

function savePredictionToHistory(result, inputData) {

    let history = JSON.parse(
        localStorage.getItem("loanPredictionHistory") || "[]"
    );


    const historyItem = {

        date: new Date().toLocaleString(),

        input: inputData,

        loan_decision:
            result.loan_decision,

        approval_probability:
            result.approval_probability,

        rejection_probability:
            result.rejection_probability,

        risk_score:
            result.risk_score,

        risk_level:
            result.risk_level,

        financial_ratios:
            result.financial_ratios,

        risk_factors:
            result.risk_factors,

        financial_strengths:
            result.financial_strengths,

        recommendations:
            result.recommendations,

        priority_actions:
            result.priority_actions
    };


    history.push(historyItem);


    // Keep only latest 20 predictions

    if (history.length > 20) {
        history = history.slice(-20);
    }


    localStorage.setItem(
        "loanPredictionHistory",
        JSON.stringify(history)
    );
}



// ============================================================
// DISPLAY PREDICTION RESULTS
// ============================================================

function displayResults(result) {

    const resultsContent =
        document.getElementById("resultsContent");

    if (!resultsContent) {
        return;
    }


    // --------------------------------------------------------
    // GET RESULT DATA
    // --------------------------------------------------------

    const decision =
        result.loan_decision || "Unknown";

    const approval =
        Number(result.approval_probability || 0);

    const rejection =
        Number(result.rejection_probability || 0);

    const riskScore =
        Number(result.risk_score || 0);

    const riskLevel =
        result.risk_level || "Unknown";

    const ratios =
        result.financial_ratios || {};

    const riskFactors =
        result.risk_factors || [];

    const strengths =
        result.financial_strengths || [];

    const recommendations =
        result.recommendations || [];

    const priorityActions =
        result.priority_actions || [];


    // --------------------------------------------------------
    // DECISION SETTINGS
    // --------------------------------------------------------

    const isApproved =
        decision.toLowerCase().trim() === "approved";

    const decisionClass =
        isApproved
            ? "approved"
            : "rejected";

    const decisionIcon =
        isApproved
            ? "✓"
            : "✕";


    // --------------------------------------------------------
    // RISK SETTINGS
    // --------------------------------------------------------

    const riskClass =
        riskLevel
            .toLowerCase()
            .replace(/\s+/g, "-");


    let riskMessage =
        "Your financial profile shows a manageable level of risk.";


    if (riskLevel.toLowerCase() === "low") {

        riskMessage =
            "Your financial profile appears healthy with relatively low financial risk.";

    }

    else if (riskLevel.toLowerCase() === "medium") {

        riskMessage =
            "Your financial profile shows some areas that may need attention before taking additional debt.";

    }

    else if (riskLevel.toLowerCase() === "high") {

        riskMessage =
            "Your financial profile shows significant financial risk that should be addressed.";

    }

    else if (riskLevel.toLowerCase() === "very high") {

        riskMessage =
            "Your financial profile indicates very high financial risk. Careful financial planning is recommended.";

    }


    // --------------------------------------------------------
    // RISK GAUGE
    // --------------------------------------------------------

    const circumference = 251.2;

    const safeRiskScore =
        Math.max(
            0,
            Math.min(100, riskScore)
        );

    const dashOffset =
        circumference -
        (safeRiskScore / 100) * circumference;


    // --------------------------------------------------------
    // RISK FACTORS
    // --------------------------------------------------------

    let riskFactorsHTML = "";

    if (riskFactors.length === 0) {

        riskFactorsHTML = `
            <div class="result-list-item positive">
                ✓ No major risk factors identified
            </div>
        `;

    }

    else {

        riskFactorsHTML =
            riskFactors.map(function (factor) {

                return `
                    <div class="result-list-item negative">
                        ⚠ ${factor}
                    </div>
                `;

            }).join("");

    }


    // --------------------------------------------------------
    // FINANCIAL STRENGTHS
    // --------------------------------------------------------

    let strengthsHTML = "";

    if (strengths.length === 0) {

        strengthsHTML = `
            <div class="result-list-item">
                No specific strengths identified.
            </div>
        `;

    }

    else {

        strengthsHTML =
            strengths.map(function (strength) {

                return `
                    <div class="result-list-item positive">
                        ✓ ${strength}
                    </div>
                `;

            }).join("");

    }


    // --------------------------------------------------------
    // RECOMMENDATIONS
    // --------------------------------------------------------

    let recommendationsHTML = "";

    if (recommendations.length === 0) {

        recommendationsHTML = `
            <div class="result-list-item">
                Your financial profile appears healthy.
            </div>
        `;

    }

    else {

        recommendationsHTML =
            recommendations.map(function (recommendation) {

                return `
                    <div class="result-list-item">
                        💡 ${recommendation}
                    </div>
                `;

            }).join("");

    }


    // --------------------------------------------------------
    // PRIORITY ACTIONS
    // --------------------------------------------------------

    let priorityHTML = "";

    if (priorityActions.length === 0) {

        priorityHTML = `
            <div class="result-list-item positive">
                ✓ No immediate action required.
            </div>
        `;

    }

    else {

        priorityHTML =
            priorityActions.map(function (action) {

                return `
                    <div class="result-list-item">
                        🎯 ${action}
                    </div>
                `;

            }).join("");

    }


    // --------------------------------------------------------
    // BUILD RESULTS PAGE
    // --------------------------------------------------------

    resultsContent.innerHTML = `

        <!-- ==================================================
             ASSESSMENT SUMMARY
             ================================================== -->

        <div class="assessment-summary-card">

            <div class="assessment-summary-icon">
                📋
            </div>

            <div>

                <p class="assessment-summary-label">
                    AI Financial Assessment
                </p>

                <h2>
                    Analysis Summary
                </h2>

                <p class="assessment-summary-text">
                    Your application has been evaluated using
                    the SmartLoan AI prediction and risk
                    assessment system.
                </p>

            </div>

        </div>



        <!-- ==================================================
             LOAN DECISION
             ================================================== -->

        <div class="visual-result-card">

            <div class="visual-decision ${decisionClass}">

                <div class="visual-decision-icon">
                    ${decisionIcon}
                </div>

                <div>

                    <p class="result-label">
                        Loan Decision
                    </p>

                    <h2>
                        ${decision}
                    </h2>

                    <p>
                        ${
                            isApproved
                                ? "Your application appears eligible based on the analyzed financial information."
                                : "Your application does not currently meet the model's approval criteria."
                        }
                    </p>

                </div>

            </div>

        </div>



        <!-- ==================================================
             PROBABILITIES
             ================================================== -->

        <div class="probability-grid">

            <div class="probability-card">

                <div class="probability-header">

                    <span class="probability-title">
                        ✓ Approval Probability
                    </span>

                    <span class="probability-value">
                        ${approval.toFixed(2)}%
                    </span>

                </div>

                <div class="probability-bar">

                    <div
                        class="probability-fill approval-fill"
                        style="width: ${approval}%">
                    </div>

                </div>

                <p class="probability-description">
                    Estimated probability of loan approval
                    from the machine learning model.
                </p>

            </div>



            <div class="probability-card">

                <div class="probability-header">

                    <span class="probability-title">
                        ✕ Rejection Probability
                    </span>

                    <span class="probability-value">
                        ${rejection.toFixed(2)}%
                    </span>

                </div>

                <div class="probability-bar">

                    <div
                        class="probability-fill rejection-fill"
                        style="width: ${rejection}%">
                    </div>

                </div>

                <p class="probability-description">
                    Estimated probability of loan rejection
                    from the machine learning model.
                </p>

            </div>

        </div>



        <!-- ==================================================
             DEFAULT RISK ASSESSMENT
             ================================================== -->

        <div class="visual-result-card risk-visual-card">

            <div class="risk-visual-info">

                <p class="section-eyebrow">
                    Risk Assessment
                </p>

                <h2>
                    🛡️ Default Risk Assessment
                </h2>

                <p>
                    ${riskMessage}
                </p>

                <div class="risk-level-badge ${riskClass}">
                    ${riskLevel} Risk
                </div>

            </div>


            <div class="risk-gauge">

                <svg viewBox="0 0 100 100">

                    <circle
                        class="risk-gauge-bg"
                        cx="50"
                        cy="50"
                        r="40">
                    </circle>


                    <circle
                        class="risk-gauge-progress ${riskClass}"
                        cx="50"
                        cy="50"
                        r="40"
                        stroke-dasharray="${circumference}"
                        stroke-dashoffset="${dashOffset}">
                    </circle>

                </svg>


                <div class="risk-gauge-content">

                    <div class="risk-score-number">
                        ${riskScore.toFixed(0)}
                    </div>

                    <div class="risk-score-label">
                        RISK / 100
                    </div>

                </div>

            </div>

        </div>



        <!-- ==================================================
             FINANCIAL ANALYSIS
             ================================================== -->

        <div class="visual-result-card">

            <div class="result-section-heading">

                <div>

                    <p class="section-eyebrow">
                        Financial Indicators
                    </p>

                    <h2>
                        📊 Financial Analysis
                    </h2>

                </div>

            </div>


            <div class="ratio-grid">

                <div class="ratio-card">

                    <span>
                        Debt-to-Income Ratio
                    </span>

                    <strong>
                        ${Number(
                            ratios.debt_to_income_ratio || 0
                        ).toFixed(3)}
                    </strong>

                </div>


                <div class="ratio-card">

                    <span>
                        Loan-to-Income Ratio
                    </span>

                    <strong>
                        ${Number(
                            ratios.loan_to_income_ratio || 0
                        ).toFixed(3)}
                    </strong>

                </div>


                <div class="ratio-card">

                    <span>
                        Savings-to-Loan Ratio
                    </span>

                    <strong>
                        ${Number(
                            ratios.savings_to_loan_ratio || 0
                        ).toFixed(3)}
                    </strong>

                </div>

            </div>

        </div>



        <!-- ==================================================
             RISK FACTORS
             ================================================== -->

        <div class="visual-result-card">

            <p class="section-eyebrow">
                Risk Indicators
            </p>

            <h2>
                ⚠️ Risk Factors
            </h2>

            <div class="result-list">

                ${riskFactorsHTML}

            </div>

        </div>



        <!-- ==================================================
             FINANCIAL STRENGTHS
             ================================================== -->

        <div class="visual-result-card">

            <p class="section-eyebrow">
                Positive Indicators
            </p>

            <h2>
                💪 Financial Strengths
            </h2>

            <div class="result-list">

                ${strengthsHTML}

            </div>

        </div>



        <!-- ==================================================
             RECOMMENDATIONS
             ================================================== -->

        <div class="visual-result-card">

            <p class="section-eyebrow">
                AI Insights
            </p>

            <h2>
                💡 Smart Recommendations
            </h2>

            <div class="result-list">

                ${recommendationsHTML}

            </div>

        </div>



        <!-- ==================================================
             PRIORITY ACTIONS
             ================================================== -->

        <div class="visual-result-card priority-result-card">

            <p class="section-eyebrow">
                Next Steps
            </p>

            <h2>
                🎯 Priority Actions
            </h2>

            <div class="result-list">

                ${priorityHTML}

            </div>

        </div>

    `;
}



// ============================================================
// DISPLAY HISTORY
// ============================================================

function displayHistory() {

    const historyContent =
        document.getElementById("historyContent");

    if (!historyContent) {
        return;
    }


    const history = JSON.parse(
        localStorage.getItem("loanPredictionHistory") || "[]"
    );


    // ========================================================
    // NO HISTORY
    // ========================================================

    if (history.length === 0) {

        historyContent.innerHTML = `

            <div class="history-icon">
                ◷
            </div>

            <h2>
                No Predictions Yet
            </h2>

            <p>
                Your previous loan analyses will be saved here.
            </p>

            <button
                class="primary-btn"
                onclick="showSection('prediction')">

                Create New Analysis

            </button>

        `;

        return;
    }


    // ========================================================
    // HISTORY HEADER
    // ========================================================

    let historyHTML = `

        <div class="history-header">

            <div>

                <h2>
                    Previous Analyses
                </h2>

                <p class="history-subtitle">
                    Your recent loan prediction records
                </p>

            </div>


            <button
                class="secondary-btn"
                onclick="clearHistory()">

                Clear History

            </button>

        </div>

    `;


    // ========================================================
    // NEWEST PREDICTION FIRST
    // ========================================================

    const reversedHistory =
        [...history].reverse();


    reversedHistory.forEach(function (item, index) {

        const decision =
            (item.loan_decision || "Unknown")
                .toLowerCase()
                .trim();


        const decisionClass =
            decision === "approved"
                ? "approved"
                : "rejected";


        const predictionNumber =
            history.length - index;


        // ----------------------------------------------------
        // INPUT DETAILS
        // ----------------------------------------------------

        const input =
            item.input || {};


        const annualIncome =
            Number(
                input.annual_income || 0
            );


        const loanAmount =
            Number(
                input.loan_amount || 0
            );


        const creditScore =
            Number(
                input.credit_score || 0
            );


        const loanPurpose =
            input.loan_purpose ||
            "Not specified";


        // ----------------------------------------------------
        // HISTORY CARD
        // ----------------------------------------------------

        historyHTML += `

            <div class="history-card">

                <!-- CARD HEADER -->

                <div class="history-card-top">

                    <div>

                        <h3>
                            Prediction ${predictionNumber}
                        </h3>

                        <p>
                            ${item.date || "Date unavailable"}
                        </p>

                    </div>


                    <span
                        class="history-decision ${decisionClass}">

                        ${item.loan_decision || "Unknown"}

                    </span>

                </div>



                <!-- MAIN PREDICTION STATS -->

                <div class="history-stats">

                    <div>

                        <span>
                            Approval Probability
                        </span>

                        <strong>
                            ${Number(
                                item.approval_probability || 0
                            ).toFixed(2)}%
                        </strong>

                    </div>


                    <div>

                        <span>
                            Risk Score
                        </span>

                        <strong>
                            ${Number(
                                item.risk_score || 0
                            ).toFixed(0)}
                            / 100
                        </strong>

                    </div>


                    <div>

                        <span>
                            Risk Level
                        </span>

                        <strong>
                            ${item.risk_level || "Unknown"}
                        </strong>

                    </div>

                </div>



                <!-- APPLICANT / LOAN DETAILS -->

                <div class="history-details">

                    <div class="history-detail-item">

                        <span>
                            Annual Income
                        </span>

                        <strong>
                            ₹${annualIncome.toLocaleString("en-IN")}
                        </strong>

                    </div>


                    <div class="history-detail-item">

                        <span>
                            Loan Amount
                        </span>

                        <strong>
                            ₹${loanAmount.toLocaleString("en-IN")}
                        </strong>

                    </div>


                    <div class="history-detail-item">

                        <span>
                            Credit Score
                        </span>

                        <strong>
                            ${creditScore}
                        </strong>

                    </div>


                    <div class="history-detail-item">

                        <span>
                            Loan Purpose
                        </span>

                        <strong>
                            ${loanPurpose}
                        </strong>

                    </div>

                </div>



                <!-- VIEW DETAILS -->

                <div class="history-card-footer">

                    <button
                        class="history-view-btn"
                        onclick="viewHistoryDetails(${history.length - 1 - index})">

                        View Full Assessment

                        <span>
                            →
                        </span>

                    </button>

                </div>

            </div>

        `;

    });


    historyContent.innerHTML =
        historyHTML;
}



// ============================================================
// VIEW HISTORY DETAILS
// ============================================================

function viewHistoryDetails(historyIndex) {

    const history = JSON.parse(
        localStorage.getItem("loanPredictionHistory") || "[]"
    );


    if (
        historyIndex < 0 ||
        historyIndex >= history.length
    ) {

        alert(
            "Unable to open this prediction."
        );

        return;
    }


    const selectedPrediction =
        history[historyIndex];


    // --------------------------------------------------------
    // Display saved prediction
    // --------------------------------------------------------

    displayResults(
        selectedPrediction
    );


    // --------------------------------------------------------
    // Show historical result banner
    // --------------------------------------------------------

    const historicalBanner =
        document.getElementById(
            "historicalResultBanner"
        );


    if (historicalBanner) {

        historicalBanner.classList.remove(
            "hidden"
        );

    }


    // --------------------------------------------------------
    // Open Results page
    // --------------------------------------------------------

    showSection("results");
}



// ============================================================
// CLEAR HISTORY
// ============================================================

function clearHistory() {

    const confirmation =
        confirm(
            "Are you sure you want to clear all prediction history?"
        );


    if (!confirmation) {
        return;
    }


    localStorage.removeItem(
        "loanPredictionHistory"
    );


    displayHistory();

    updateDashboardStatistics();
}



// ============================================================
// DASHBOARD STATISTICS
// ============================================================

function updateDashboardStatistics() {

    const history = JSON.parse(
        localStorage.getItem("loanPredictionHistory") || "[]"
    );


    // ========================================================
    // BASIC COUNTS
    // ========================================================

    const total =
        history.length;


    let approved = 0;
    let rejected = 0;


    history.forEach(function (item) {

        if (!item.loan_decision) {
            return;
        }


        const decision =
            item.loan_decision
                .toLowerCase()
                .trim();


        if (decision === "approved") {

            approved++;

        }

        else if (
            decision === "rejected" ||
            decision === "not approved"
        ) {

            rejected++;

        }

    });



    // ========================================================
    // AVERAGE RISK SCORE
    // ========================================================

    let averageRisk = 0;


    if (history.length > 0) {

        const totalRisk =
            history.reduce(function (sum, item) {

                return sum +
                    Number(
                        item.risk_score || 0
                    );

            }, 0);


        averageRisk =
            totalRisk / history.length;
    }



    // ========================================================
    // UPDATE KPI CARDS
    // ========================================================

    const totalElement =
        document.getElementById(
            "totalPredictions"
        );


    const approvedElement =
        document.getElementById(
            "approvedPredictions"
        );


    const rejectedElement =
        document.getElementById(
            "rejectedPredictions"
        );


    const averageRiskElement =
        document.getElementById(
            "averageRiskScore"
        );


    if (totalElement) {

        totalElement.textContent =
            total;

    }


    if (approvedElement) {

        approvedElement.textContent =
            approved;

    }


    if (rejectedElement) {

        rejectedElement.textContent =
            rejected;

    }


    if (averageRiskElement) {

        averageRiskElement.textContent =
            averageRisk.toFixed(0);

    }



    // ========================================================
    // APPROVAL / REJECTION ANALYTICS
    // ========================================================

    const approvedCountElement =
        document.getElementById(
            "dashboardApprovedCount"
        );


    const rejectedCountElement =
        document.getElementById(
            "dashboardRejectedCount"
        );


    const approvedProgress =
        document.getElementById(
            "approvedProgress"
        );


    const rejectedProgress =
        document.getElementById(
            "rejectedProgress"
        );


    if (approvedCountElement) {

        approvedCountElement.textContent =
            approved;

    }


    if (rejectedCountElement) {

        rejectedCountElement.textContent =
            rejected;

    }


    let approvedPercentage = 0;
    let rejectedPercentage = 0;


    if (total > 0) {

        approvedPercentage =
            (approved / total) * 100;


        rejectedPercentage =
            (rejected / total) * 100;

    }


    if (approvedProgress) {

        approvedProgress.style.width =
            approvedPercentage + "%";

    }


    if (rejectedProgress) {

        rejectedProgress.style.width =
            rejectedPercentage + "%";

    }



    // ========================================================
    // RISK DISTRIBUTION
    // ========================================================

    let lowRisk = 0;
    let mediumRisk = 0;
    let highRisk = 0;
    let veryHighRisk = 0;


    history.forEach(function (item) {

        if (!item.risk_level) {
            return;
        }


        const risk =
            item.risk_level
                .toLowerCase()
                .trim();


        if (risk === "low") {

            lowRisk++;

        }

        else if (risk === "medium") {

            mediumRisk++;

        }

        else if (risk === "high") {

            highRisk++;

        }

        else if (
            risk === "very high" ||
            risk === "very-high"
        ) {

            veryHighRisk++;

        }

    });



    // ========================================================
    // RISK COUNT ELEMENTS
    // ========================================================

    const lowRiskCount =
        document.getElementById(
            "lowRiskCount"
        );


    const mediumRiskCount =
        document.getElementById(
            "mediumRiskCount"
        );


    const highRiskCount =
        document.getElementById(
            "highRiskCount"
        );


    const veryHighRiskCount =
        document.getElementById(
            "veryHighRiskCount"
        );


    if (lowRiskCount) {

        lowRiskCount.textContent =
            lowRisk;

    }


    if (mediumRiskCount) {

        mediumRiskCount.textContent =
            mediumRisk;

    }


    if (highRiskCount) {

        highRiskCount.textContent =
            highRisk;

    }


    if (veryHighRiskCount) {

        veryHighRiskCount.textContent =
            veryHighRisk;

    }



    // ========================================================
    // RISK PROGRESS BARS
    // ========================================================

    const lowRiskProgress =
        document.getElementById(
            "lowRiskProgress"
        );


    const mediumRiskProgress =
        document.getElementById(
            "mediumRiskProgress"
        );


    const highRiskProgress =
        document.getElementById(
            "highRiskProgress"
        );


    const veryHighRiskProgress =
        document.getElementById(
            "veryHighRiskProgress"
        );


    let lowPercentage = 0;
    let mediumPercentage = 0;
    let highPercentage = 0;
    let veryHighPercentage = 0;


    if (total > 0) {

        lowPercentage =
            (lowRisk / total) * 100;

        mediumPercentage =
            (mediumRisk / total) * 100;

        highPercentage =
            (highRisk / total) * 100;

        veryHighPercentage =
            (veryHighRisk / total) * 100;

    }


    if (lowRiskProgress) {

        lowRiskProgress.style.width =
            lowPercentage + "%";

    }


    if (mediumRiskProgress) {

        mediumRiskProgress.style.width =
            mediumPercentage + "%";

    }


    if (highRiskProgress) {

        highRiskProgress.style.width =
            highPercentage + "%";

    }


    if (veryHighRiskProgress) {

        veryHighRiskProgress.style.width =
            veryHighPercentage + "%";

    }



    // ========================================================
    // LATEST PREDICTION
    // ========================================================

    updateLatestPrediction(history);

}



// ============================================================
// LATEST PREDICTION
// ============================================================

function updateLatestPrediction(history) {

    const latestContent =
        document.getElementById(
            "latestPredictionContent"
        );


    if (!latestContent) {
        return;
    }


    // --------------------------------------------------------
    // NO PREDICTIONS
    // --------------------------------------------------------

    if (
        !history ||
        history.length === 0
    ) {

        latestContent.innerHTML = `

            <div class="latest-empty">

                <div class="latest-empty-icon">
                    📋
                </div>

                <h3>
                    No prediction available
                </h3>

                <p>
                    Create a new loan analysis to see your latest result here.
                </p>

                <button
                    class="primary-btn"
                    onclick="showSection('prediction')">

                    + New Analysis

                </button>

            </div>

        `;

        return;
    }



    // --------------------------------------------------------
    // GET LATEST PREDICTION
    // --------------------------------------------------------

    const latest =
        history[history.length - 1];


    const decision =
        latest.loan_decision ||
        "Unknown";


    const riskLevel =
        latest.risk_level ||
        "Unknown";


    const approval =
        Number(
            latest.approval_probability || 0
        );


    const riskScore =
        Number(
            latest.risk_score || 0
        );


    const decisionClass =
        decision.toLowerCase().trim() === "approved"
            ? "latest-decision-approved"
            : "latest-decision-rejected";


    const riskClass =
        riskLevel
            .toLowerCase()
            .replace(/\s+/g, "-");


    latestContent.innerHTML = `

        <div class="latest-summary">

            <!-- DECISION -->

            <div class="latest-summary-item">

                <span>
                    Loan Decision
                </span>

                <strong class="${decisionClass}">

                    ${decision}

                </strong>

            </div>


            <!-- APPROVAL -->

            <div class="latest-summary-item">

                <span>
                    Approval Probability
                </span>

                <strong>

                    ${approval.toFixed(2)}%

                </strong>

            </div>


            <!-- RISK LEVEL -->

            <div class="latest-summary-item">

                <span>
                    Risk Level
                </span>

                <strong
                    class="latest-risk-${riskClass}">

                    ${riskLevel}

                </strong>

            </div>


            <!-- RISK SCORE -->

            <div class="latest-summary-item">

                <span>
                    Risk Score
                </span>

                <strong>

                    ${riskScore.toFixed(0)} / 100

                </strong>

            </div>

        </div>

    `;
}



// ============================================================
// FORM SUBMISSION
// ============================================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        const loanForm =
            document.getElementById(
                "loanForm"
            );


        if (!loanForm) {
            return;
        }


        loanForm.addEventListener(
            "submit",
            async function (event) {

                event.preventDefault();


                // =================================================
                // COLLECT FORM DATA
                // =================================================

                const inputData = {

                    age:
                        Number(
                            document.getElementById(
                                "Age"
                            ).value
                        ),

                    employment_status:
                        document.getElementById(
                            "EmploymentStatus"
                        ).value,

                    education_level:
                        document.getElementById(
                            "EducationLevel"
                        ).value,

                    experience:
                        Number(
                            document.getElementById(
                                "Experience"
                            ).value
                        ),

                    home_ownership_status:
                        document.getElementById(
                            "HomeOwnershipStatus"
                        ).value,

                    annual_income:
                        Number(
                            document.getElementById(
                                "AnnualIncome"
                            ).value
                        ),

                    credit_score:
                        Number(
                            document.getElementById(
                                "CreditScore"
                            ).value
                        ),

                    monthly_debt_payments:
                        Number(
                            document.getElementById(
                                "MonthlyDebtPayments"
                            ).value
                        ),

                    savings_account_balance:
                        Number(
                            document.getElementById(
                                "SavingsAccountBalance"
                            ).value
                        ),

                    loan_amount:
                        Number(
                            document.getElementById(
                                "LoanAmount"
                            ).value
                        ),

                    loan_duration:
                        Number(
                            document.getElementById(
                                "LoanDuration"
                            ).value
                        ),

                    loan_purpose:
                        document.getElementById(
                            "LoanPurpose"
                        ).value
                };


                // =================================================
                // VALIDATION
                // =================================================

                for (
                    const key in inputData
                ) {

                    if (

                        inputData[key] === "" ||

                        inputData[key] === null ||

                        Number.isNaN(
                            inputData[key]
                        )

                    ) {

                        alert(
                            "Please fill all fields before prediction."
                        );

                        return;
                    }
                }


                // =================================================
                // BUTTON LOADING
                // =================================================

                const submitButton =
                    loanForm.querySelector(
                        ".analyze-btn"
                    );


                const originalText =
                    submitButton.innerHTML;


                submitButton.disabled =
                    true;


                submitButton.innerHTML =
                    "⏳ Analyzing...";


                // =================================================
                // SEND REQUEST
                // =================================================

                try {

                    const response =
                        await fetch(
                            API_URL,
                            {

                                method: "POST",

                                headers: {

                                    "Content-Type":
                                        "application/json"

                                },

                                body:
                                    JSON.stringify(
                                        inputData
                                    )
                            }
                        );


                    // =================================================
                    // HANDLE API ERROR
                    // =================================================

                    if (!response.ok) {

                        let errorMessage =
                            "Prediction request failed.";


                        try {

                            const errorData =
                                await response.json();


                            errorMessage =
                                errorData.detail ||
                                errorMessage;

                        }

                        catch (jsonError) {

                            console.error(
                                "Could not read API error:",
                                jsonError
                            );

                        }


                        throw new Error(
                            errorMessage
                        );
                    }


                    // =================================================
                    // GET RESULT
                    // =================================================

                    const result =
                        await response.json();


                    console.log(
                        "Prediction Result:",
                        result
                    );


                    // =================================================
                    // IMPORTANT:
                    // THIS IS A NEW PREDICTION
                    // =================================================

                    const historicalBanner =
                        document.getElementById(
                            "historicalResultBanner"
                        );


                    if (historicalBanner) {

                        historicalBanner.classList.add(
                            "hidden"
                        );

                    }


                    // =================================================
                    // DISPLAY RESULT
                    // =================================================

                    displayResults(
                        result
                    );


                    // =================================================
                    // SAVE TO HISTORY
                    // =================================================

                    savePredictionToHistory(
                        result,
                        inputData
                    );


                    // =================================================
                    // UPDATE DASHBOARD
                    // =================================================

                    updateDashboardStatistics();


                    // =================================================
                    // OPEN RESULTS PAGE
                    // =================================================

                    showSection(
                        "results"
                    );

                }


                catch (error) {

                    console.error(
                        "Prediction Error:",
                        error
                    );


                    alert(
                        "Unable to get prediction.\n\n" +
                        error.message
                    );

                }


                finally {

                    submitButton.disabled =
                        false;


                    submitButton.innerHTML =
                        originalText;

                }

            }
        );


        // ========================================================
        // INITIAL PAGE DATA
        // ========================================================

        displayHistory();

        updateDashboardStatistics();

    }
);