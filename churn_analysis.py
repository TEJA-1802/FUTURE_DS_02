"""
=============================================================
 CUSTOMER RETENTION & CHURN ANALYSIS
 Future Interns – Data Science & Analytics – Task 2 (2026)
 Intern : Barre Tejaswanth   |   CIN : FIT/MAR26/DS14776
 Dataset: Telco Customer Churn Dataset (Kaggle)

 This script:
   1. Loads & cleans the raw Telco Churn dataset
   2. Engineers features and computes all churn KPIs
   3. Performs cohort, segment & driver analysis
   4. Exports analysis-ready CSVs for Power BI dashboarding
=============================================================
"""

import pandas as pd
import numpy as np
import os

os.makedirs("powerbi_data", exist_ok=True)

# ══════════════════════════════════════════════════════════════════════════════
#  STEP 1 — LOAD & CLEAN
# ══════════════════════════════════════════════════════════════════════════════
print("=" * 60)
print("  STEP 1: Loading & Cleaning Data")
print("=" * 60)

df = pd.read_csv("telco_churn.csv")

print(f"\n  Records loaded  : {len(df):,}")
print(f"  Columns         : {len(df.columns)}")

# Fix TotalCharges — it's stored as string, some rows have blank spaces
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

# How many nulls after conversion?
blanks = df["TotalCharges"].isnull().sum()
print(f"  Blank TotalCharges rows: {blanks} → filling with MonthlyCharges")

# These are new customers (tenure=0), fill with MonthlyCharges
df["TotalCharges"] = df["TotalCharges"].fillna(df["MonthlyCharges"])

# Convert Churn to binary (1 = churned, 0 = retained)
df["Churn_Binary"] = (df["Churn"] == "Yes").astype(int)

# Convert SeniorCitizen from 0/1 to readable labels
df["SeniorCitizen_Label"] = df["SeniorCitizen"].map({0: "Non-Senior", 1: "Senior"})

print(f"  Null values after cleaning: {df.isnull().sum().sum()}")
print(f"  Churn rate: {df['Churn_Binary'].mean()*100:.1f}%")

# ══════════════════════════════════════════════════════════════════════════════
#  STEP 2 — FEATURE ENGINEERING
# ══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("  STEP 2: Feature Engineering")
print("=" * 60)

# Tenure groups (cohorts)
df["Tenure Group"] = pd.cut(
    df["tenure"],
    bins=[0, 6, 12, 24, 36, 48, 60, 72],
    labels=["0-6 mo", "7-12 mo", "13-24 mo", "25-36 mo",
            "37-48 mo", "49-60 mo", "61-72 mo"],
    include_lowest=True
)

# Monthly charges band
df["Charges Band"] = pd.cut(
    df["MonthlyCharges"],
    bins=[0, 35, 65, 95, 120],
    labels=["Low (<$35)", "Mid ($35-65)", "High ($65-95)", "Premium (>$95)"]
)

# Number of services subscribed
service_cols = ["PhoneService","MultipleLines","OnlineSecurity",
                "OnlineBackup","DeviceProtection","TechSupport",
                "StreamingTV","StreamingMovies"]

def count_services(row):
    count = 0
    for col in service_cols:
        if row[col] in ["Yes"]:
            count += 1
    return count

df["Num Services"] = df.apply(count_services, axis=1)
df["Service Band"] = pd.cut(df["Num Services"],
                             bins=[-1,1,3,5,8],
                             labels=["1 service","2-3 services",
                                     "4-5 services","6+ services"])

print(f"  New features added: Tenure Group, Charges Band,")
print(f"  Num Services, Service Band, Churn_Binary")

# ══════════════════════════════════════════════════════════════════════════════
#  STEP 3 — KPI SUMMARY
# ══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("  STEP 3: KPI Summary")
print("=" * 60)

total_customers   = len(df)
churned           = df["Churn_Binary"].sum()
retained          = total_customers - churned
churn_rate        = churned / total_customers * 100
retention_rate    = retained / total_customers * 100
avg_tenure        = df["tenure"].mean()
avg_monthly       = df["MonthlyCharges"].mean()
avg_total         = df["TotalCharges"].mean()
monthly_rev_lost  = df[df["Churn"]=="Yes"]["MonthlyCharges"].sum()
avg_tenure_churned= df[df["Churn"]=="Yes"]["tenure"].mean()
avg_tenure_retained=df[df["Churn"]=="No"]["tenure"].mean()

print(f"\n  Total Customers      : {total_customers:,}")
print(f"  Churned Customers    : {churned:,}")
print(f"  Retained Customers   : {retained:,}")
print(f"  Churn Rate           : {churn_rate:.1f}%")
print(f"  Retention Rate       : {retention_rate:.1f}%")
print(f"  Avg Tenure (all)     : {avg_tenure:.1f} months")
print(f"  Avg Tenure (churned) : {avg_tenure_churned:.1f} months")
print(f"  Avg Tenure (retained): {avg_tenure_retained:.1f} months")
print(f"  Avg Monthly Charges  : ${avg_monthly:.2f}")
print(f"  Monthly Revenue Lost : ${monthly_rev_lost:,.2f}")

# Export KPIs
kpi_df = pd.DataFrame([
    {"Metric": "Total Customers",          "Value": total_customers},
    {"Metric": "Churned Customers",        "Value": churned},
    {"Metric": "Retained Customers",       "Value": retained},
    {"Metric": "Churn Rate %",             "Value": round(churn_rate, 1)},
    {"Metric": "Retention Rate %",         "Value": round(retention_rate, 1)},
    {"Metric": "Avg Tenure (months)",      "Value": round(avg_tenure, 1)},
    {"Metric": "Avg Tenure Churned (mo)",  "Value": round(avg_tenure_churned, 1)},
    {"Metric": "Avg Tenure Retained (mo)", "Value": round(avg_tenure_retained, 1)},
    {"Metric": "Avg Monthly Charges ($)",  "Value": round(avg_monthly, 2)},
    {"Metric": "Monthly Revenue Lost ($)", "Value": round(monthly_rev_lost, 2)},
])
kpi_df.to_csv("powerbi_data/kpi_summary.csv", index=False)
print("\n  ✅  kpi_summary.csv exported")

# ══════════════════════════════════════════════════════════════════════════════
#  STEP 4 — AGGREGATED TABLES FOR POWER BI
# ══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("  STEP 4: Exporting Aggregated Tables for Power BI")
print("=" * 60)

# — 4a. Churn by Contract Type ────────────────────────────────────────────────
contract = (df.groupby("Contract")
              .agg(Total=("customerID","count"),
                   Churned=("Churn_Binary","sum"),
                   Avg_Monthly=("MonthlyCharges","mean"),
                   Avg_Tenure=("tenure","mean"))
              .reset_index())
contract["Churn Rate %"]     = (contract["Churned"] / contract["Total"] * 100).round(1)
contract["Retention Rate %"] = (100 - contract["Churn Rate %"]).round(1)
contract = contract.round(2)
contract.to_csv("powerbi_data/churn_by_contract.csv", index=False)
print(f"  ✅  churn_by_contract.csv       ({len(contract)} rows)")

# — 4b. Churn by Tenure Group (Cohort Analysis) ───────────────────────────────
cohort = (df.groupby("Tenure Group", observed=True)
            .agg(Total=("customerID","count"),
                 Churned=("Churn_Binary","sum"),
                 Avg_Monthly=("MonthlyCharges","mean"),
                 Avg_Total=("TotalCharges","mean"))
            .reset_index())
cohort["Churn Rate %"]     = (cohort["Churned"] / cohort["Total"] * 100).round(1)
cohort["Retention Rate %"] = (100 - cohort["Churn Rate %"]).round(1)
cohort = cohort.round(2)
cohort.to_csv("powerbi_data/cohort_tenure.csv", index=False)
print(f"  ✅  cohort_tenure.csv           ({len(cohort)} rows)")

# — 4c. Churn by Internet Service & Key Features ──────────────────────────────
internet = (df.groupby("InternetService")
              .agg(Total=("customerID","count"),
                   Churned=("Churn_Binary","sum"),
                   Avg_Monthly=("MonthlyCharges","mean"))
              .reset_index())
internet["Churn Rate %"] = (internet["Churned"] / internet["Total"] * 100).round(1)
internet.to_csv("powerbi_data/churn_by_internet.csv", index=False)
print(f"  ✅  churn_by_internet.csv       ({len(internet)} rows)")

# — 4d. Churn by Payment Method ───────────────────────────────────────────────
payment = (df.groupby("PaymentMethod")
             .agg(Total=("customerID","count"),
                  Churned=("Churn_Binary","sum"),
                  Avg_Monthly=("MonthlyCharges","mean"))
             .reset_index())
payment["Churn Rate %"] = (payment["Churned"] / payment["Total"] * 100).round(1)
payment.sort_values("Churn Rate %", ascending=False, inplace=True)
payment.to_csv("powerbi_data/churn_by_payment.csv", index=False)
print(f"  ✅  churn_by_payment.csv        ({len(payment)} rows)")

# — 4e. Churn by Demographics ─────────────────────────────────────────────────
# Gender
gender = (df.groupby("gender")
            .agg(Total=("customerID","count"),
                 Churned=("Churn_Binary","sum"))
            .reset_index())
gender["Churn Rate %"] = (gender["Churned"] / gender["Total"] * 100).round(1)

# Senior Citizen
senior = (df.groupby("SeniorCitizen_Label")
            .agg(Total=("customerID","count"),
                 Churned=("Churn_Binary","sum"))
            .reset_index()
            .rename(columns={"SeniorCitizen_Label":"Segment"}))
senior["Churn Rate %"] = (senior["Churned"] / senior["Total"] * 100).round(1)
senior["Category"] = "Senior Status"

# Partner
partner = (df.groupby("Partner")
             .agg(Total=("customerID","count"),
                  Churned=("Churn_Binary","sum"))
             .reset_index()
             .rename(columns={"Partner":"Segment"}))
partner["Churn Rate %"] = (partner["Churned"] / partner["Total"] * 100).round(1)
partner["Category"] = "Has Partner"

# Dependents
depend = (df.groupby("Dependents")
            .agg(Total=("customerID","count"),
                 Churned=("Churn_Binary","sum"))
            .reset_index()
            .rename(columns={"Dependents":"Segment"}))
depend["Churn Rate %"] = (depend["Churned"] / depend["Total"] * 100).round(1)
depend["Category"] = "Has Dependents"

demographics = pd.concat([senior, partner, depend], ignore_index=True)
demographics.to_csv("powerbi_data/churn_by_demographics.csv", index=False)
print(f"  ✅  churn_by_demographics.csv   ({len(demographics)} rows)")

# — 4f. Churn by Number of Services ──────────────────────────────────────────
services = (df.groupby("Service Band", observed=True)
              .agg(Total=("customerID","count"),
                   Churned=("Churn_Binary","sum"),
                   Avg_Monthly=("MonthlyCharges","mean"))
              .reset_index())
services["Churn Rate %"] = (services["Churned"] / services["Total"] * 100).round(1)
services.to_csv("powerbi_data/churn_by_services.csv", index=False)
print(f"  ✅  churn_by_services.csv       ({len(services)} rows)")

# — 4g. Churn by Monthly Charges Band ────────────────────────────────────────
charges = (df.groupby("Charges Band", observed=True)
             .agg(Total=("customerID","count"),
                  Churned=("Churn_Binary","sum"),
                  Avg_Tenure=("tenure","mean"))
             .reset_index())
charges["Churn Rate %"] = (charges["Churned"] / charges["Total"] * 100).round(1)
charges.to_csv("powerbi_data/churn_by_charges.csv", index=False)
print(f"  ✅  churn_by_charges.csv        ({len(charges)} rows)")

# — 4h. Master Table (clean, for Power BI relationships & slicers) ────────────
master_cols = [
    "customerID","gender","SeniorCitizen_Label","Partner","Dependents",
    "tenure","Tenure Group","PhoneService","MultipleLines","InternetService",
    "OnlineSecurity","OnlineBackup","DeviceProtection","TechSupport",
    "StreamingTV","StreamingMovies","Contract","PaperlessBilling",
    "PaymentMethod","MonthlyCharges","TotalCharges","Charges Band",
    "Num Services","Service Band","Churn","Churn_Binary"
]
df[master_cols].to_csv("powerbi_data/master_table.csv", index=False)
print(f"  ✅  master_table.csv            ({len(df)} rows — full clean dataset)")

# ══════════════════════════════════════════════════════════════════════════════
#  STEP 5 — KEY FINDINGS
# ══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("  STEP 5: Key Findings & Recommendations")
print("=" * 60)

# Highest churn contract
worst_contract = contract.sort_values("Churn Rate %", ascending=False).iloc[0]
# Highest churn tenure group
worst_cohort   = cohort.sort_values("Churn Rate %", ascending=False).iloc[0]
# Highest churn payment
worst_payment  = payment.iloc[0]
# Highest churn internet
worst_internet = internet.sort_values("Churn Rate %", ascending=False).iloc[0]

print(f"""
  Overall churn rate       : {churn_rate:.1f}% ({churned:,} of {total_customers:,} customers)
  Monthly revenue at risk  : ${monthly_rev_lost:,.0f}/month

  CHURN DRIVERS:
  - Contract type  : {worst_contract['Contract']} has {worst_contract['Churn Rate %']}% churn rate
  - Tenure group   : {worst_cohort['Tenure Group']} customers churn most ({worst_cohort['Churn Rate %']}%)
  - Payment method : {worst_payment['PaymentMethod']} has {worst_payment['Churn Rate %']}% churn rate
  - Internet type  : {worst_internet['InternetService']} service has {worst_internet['Churn Rate %']}% churn rate

  RECOMMENDATIONS:
  1. Offer discounts to convert Month-to-Month customers to annual contracts
  2. Implement a 0-6 month onboarding program — highest churn window
  3. Incentivize auto-pay setup — Electronic check users churn most
  4. Bundle OnlineSecurity + TechSupport for Fiber Optic users
  5. Target senior citizens with dedicated retention campaigns
  6. Offer loyalty rewards at 12, 24 and 36 month milestones
""")

print("=" * 60)
print("  All CSVs saved in powerbi_data/ folder")
print("  Load them into Power BI to build your dashboard")
print("=" * 60)
