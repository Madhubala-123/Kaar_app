import streamlit as st
import pandas as pd

# 1. Page Config & Layout Architecture
st.set_page_config(page_title="SAP Cash Application", layout="wide")
st.title("🏦 SAP Record-to-Report (R2R) Smart Cash Application Workbench")
st.caption("Aligned with Chapter 2.3 & 10 — Auto-Match Payments to Open Invoices")
st.write("---")

# 2. Section 10.4 KPI Tiles (Calculated metrics)
st.subheader("📊 Live Reconciliation KPIs")
col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
with col_kpi1:
    st.metric(label="Cash-Application Rate", value="75.0%", delta="+5.2% (AI Assisted)")
with col_kpi2:
    st.metric(label="Days Sales Outstanding (DSO)", value="34 Days", delta="-4 Days (Dropped)")
with col_kpi3:
    st.metric(label="Unapplied-Cash Backlog", value="₹3,40,000", delta="Requires Review", delta_color="inverse")

st.write("---")

# 3. Seeded Data Simulation (Representing incoming data files)
st.subheader("📋 Invoices vs. Incoming Bank Wire Matches")

# Simulated rows from open_invoices.csv and payments.csv
data_matrix = {
    "Payment ID": ["PMT-901", "PMT-902", "PMT-903"],
    "Customer (Bank Wire Name)": ["Tata Motors Ltd", "Reliance Retail Inc.", "Kiran Elec."],
    "Bank Amount Received (INR)":,
    "Closest Open Invoice Bill": ["INV-4401 (Tata Motors)", "INV-4402 (Reliance)", "INV-4403 (Kiran Electronics)"],
    "Invoice Bill Value (INR)": [500000, 120000, 45000]
}
df = pd.DataFrame(data_matrix)

# Grounded AI / Fuzzy Logic Matching Engine
def run_fuzzy_matching(row):
    # Exact Match Rule
    if row["Bank Amount Received (INR)"] == row["Invoice Bill Value (INR)"]:
        return "🟢 EXACT MATCH (Auto-Posted)"
    # Fuzzy Match Rule (Customer paid slightly less due to bank fee deductions)
    elif abs(row["Bank Amount Received (INR)"] - row["Invoice Bill Value (INR)"]) <= 500:
        return "🟡 FUZZY MATCH (Fee Difference/Review Required)"
    return "🔴 UNMATCHED BACKLOG"

df["Matching Engine Status"] = df.apply(run_fuzzy_matching, axis=1)
st.dataframe(df, use_container_width=True)

# 4. Input Validation & Posting Controls
st.write("---")
st.subheader("🛠️ Unmatched Review & Processing Panel")

selected_pmt = st.selectbox("Select Payment ID to manually clear:", ["PMT-903 (Kiran Elec.)"])
target_invoice = st.selectbox("Link to Open Invoice Document:", ["INV-4403 - Kiran Electronics (Value: ₹45,000)"])
reconciliation_note = st.text_input("Enter accountant reconciliation notes (Mandatory):")

col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    if st.button("📝 Post & Clear Match (F-28)", type="primary"):
        # Real input verification rules
        if not reconciliation_note:
            st.warning("⚠️ Validation Error: You cannot post this clearing document without entering an accounting reason note.")
        else:
            st.success(f"Success! Payment {selected_pmt} linked to invoice {target_invoice.split(' ')[0]}. SAP FI ledger updated.")
with col_btn2:
    if st.button("❌ Flag to Dispute Queue"):
        st.error(f"Payment {selected_pmt} routed to Customer Dispute Desk. Notice transmitted to Sales Cloud.")
