# 📉 Customer Retention & Churn Analysis
**Future Interns – Data Science & Analytics | Task 2 (2026)**

> **Intern:** Barre Tejaswanth | **CIN:** FIT/MAR26/DS14776

---

## 🎯 Objective
Analyze Telco customer data to identify churn patterns, key retention drivers, and customer lifetime trends — and deliver actionable recommendations to reduce customer loss.

---

## 🛠️ Tools Used
| Tool | Purpose |
|------|---------|
| Python 3 | Data cleaning, feature engineering, churn KPI analysis |
| Pandas & NumPy | Data manipulation and computation |
| Power BI | Interactive retention & churn dashboard |

---

## 📁 Repository Structure
```
FUTURE_DS_02/
├── telco_churn.csv                    ← Raw dataset (7,043 customers)
├── churn_analysis.py                  ← Python: cleaning, KPIs, exports Power BI CSVs
├── files(2)/
│   ├── master_table.csv               ← Full cleaned dataset with engineered features
│   ├── kpi_summary.csv                ← 10 headline KPIs
│   ├── churn_by_contract.csv          ← Churn rate by contract type
│   ├── cohort_tenure.csv              ← Cohort analysis by tenure group
│   ├── churn_by_internet.csv          ← Churn by internet service type
│   ├── churn_by_payment.csv           ← Churn by payment method
│   ├── churn_by_demographics.csv      ← Churn by senior status, partner, dependents
│   ├── churn_by_services.csv          ← Churn by number of services subscribed
│   └── churn_by_charges.csv           ← Churn by monthly charges band
├── dashboard.pbix                     ← Power BI dashboard file
└── README.md
```

---

## 📊 Key Performance Indicators

| Metric | Value |
|--------|-------|
| Total Customers | 7,043 |
| Churned Customers | 1,869 |
| Retained Customers | 5,174 |
| Churn Rate | 26.5% |
| Retention Rate | 73.5% |
| Avg Tenure (Churned) | 18.0 months |
| Avg Tenure (Retained) | 37.6 months |
| Avg Monthly Charges | $64.76 |
| Monthly Revenue at Risk | $139,131 |

---

## 🔍 Key Churn Drivers

### 1. 📋 Month-to-Month Contracts Are the #1 Risk
Month-to-month customers have a **42.7% churn rate** — nearly 3x higher than one-year (11.3%) and 6x higher than two-year contracts (2.8%). Contract type is the single strongest predictor of churn.

### 2. ⏱️ First 6 Months Are the Most Critical
Customers in the 0–6 month tenure group churn at **52.9%** — over half leave before they've been customers for even half a year. Onboarding experience is clearly failing new customers.

### 3. 💳 Electronic Check Payment = Highest Churn
Customers paying via electronic check churn at **45.3%**, nearly double those on automatic bank transfer (16.7%). Friction in payment may be a signal of low commitment.

### 4. 🌐 Fiber Optic Customers Churn More Despite Paying More
Fiber optic internet users churn at **41.9%** — the highest of any internet type — despite paying the highest monthly charges. This indicates a quality or value-for-money issue.

### 5. 👴 Senior Citizens Are a High-Risk Segment
Senior citizens have a significantly higher churn rate than non-seniors, yet represent a segment that likely needs more support and personalized engagement.

### 6. 🔒 More Services = Better Retention
Customers with 6+ services have dramatically lower churn than those with 1–2 services. Service bundling creates switching costs and deepens customer engagement.

---

## ✅ Actionable Recommendations

| Priority | Recommendation | Expected Impact |
|----------|---------------|----------------|
| 🔴 High | Convert Month-to-Month customers to annual contracts with a discount | Reduce churn by up to 30% |
| 🔴 High | Build a 0–6 month onboarding & check-in program | Cut early churn significantly |
| 🟠 Medium | Incentivize auto-pay adoption — reduce electronic check dependency | Lower payment-driven churn |
| 🟠 Medium | Investigate Fiber Optic service quality issues | Reduce premium segment churn |
| 🟠 Medium | Create a Senior Citizen retention program | Protect vulnerable segment |
| 🟡 Low | Offer service bundle upgrades at 12 & 24 month milestones | Increase switching costs |

---

## ▶️ How to Run the Python Analysis

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/FUTURE_DS_02.git
cd FUTURE_DS_02

# 2. Install dependencies
pip install pandas numpy

# 3. Run the analysis — outputs 8 CSVs into powerbi_data/
python churn_analysis.py

# 4. Open Power BI and load files from powerbi_data/
```

---

## 🔗 Program Details
- **Internship:** [Future Interns](https://futureinterns.com)
- **Task Reference:** [DS Task 2 (2026)](https://futureinterns.com/data-science-analytics-task-2-2026/)
- **Dataset:** [Telco Customer Churn – Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)
- **LinkedIn:** [@Future Interns](https://www.linkedin.com/company/future-interns/)

---
*Submitted as part of the Future Interns Data Science & Analytics Internship Program, March 2026.*
