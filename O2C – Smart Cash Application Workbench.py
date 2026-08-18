import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="SAP Cash Application", layout="wide")
st.title("🏦 SAP Order-to-Cash (O2C) Smart Cash Application Workbench")
st.caption("Question 1: Auto-Match Payments to Open Invoices (Clearing Flow)")
st.write("---")

# 2. Key Performance Indicators
st.subheader("📊 Live Reconciliation KPIs")
col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
with col_kpi1:
    st.metric(label="Cash-Application Rate", value="75.0%", delta="+5.2% (AI Assisted)")
with col_kpi2:
    st.metric(label="Days Sales Outstanding (DSO)", value="34 Days", delta="-4 Days (Dropped)")
with col_kpi3:
    st.metric(label="Unapplied-Cash Backlog", value="Rs. 3,40,000", delta="Requires Review", delta_color="inverse")

st.write("---")

# 3. Data Set Generation (No empty lists!)
st.subheader("📋 Invoices vs. Incoming Bank Wire Matches")

payment_ids = ["PMT-901", "PMT-902", "PMT-903"]
customer_names = ["Tata Motors Ltd", "Reliance Retail Inc.", "Kiran Elec."]
amounts_received = [50000, 120000, 44500]
closest_invoices = ["INV-4401 (Tata Motors)", "INV-4402 (Reliance)", "INV-4403 (Kiran Electronics)"]
invoice_values = [50000, 120000, 45000]

sap_orders = {
    "Payment ID": payment_ids,
    "Customer (Bank Wire Name)": customer_names,
    "Bank Amount Received (INR)": amounts_received,
    "Closest Open Invoice Bill": closest_invoices,
    "Invoice Bill Value (INR)": invoice_values
}
df = pd.DataFrame(sap_orders)

# Grounded AI / Match Engine Function
def run_fuzzy_matching(row):
    if row["Bank Amount Received (INR)"] == row["Invoice Bill Value (INR)"]:
        return "🟢 EXACT MATCH (Auto-Posted)"
    elif abs(row["Bank Amount Received (INR)"] - row["Invoice Bill Value (INR)"]) <= 500:
        return "🟡 FUZZY MATCH (Fee Difference/Review Required)"
    return "🔴 UNMATCHED BACKLOG"

df["Matching Engine Status"] = df.apply(run_fuzzy_matching, axis=1)
st.dataframe(df, use_container_width=True)

# 4. Process Validation and Actions
st.write("---")
st.subheader("🛠️ Unmatched Review & Processing Panel")

selected_pmt = st.selectbox("Select Payment ID to manually clear:", ["PMT-903 (Kiran Elec.)"])
target_invoice = st.selectbox("Link to Open Invoice Document:", ["INV-4403 - Kiran Electronics (Value: Rs. 45,000)"])
reconciliation_note = st.text_input("Enter accountant reconciliation notes (Mandatory):")

col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    if st.button("📝 Post & Clear Match (F-28)", type="primary"):
        if not reconciliation_note:
            st.warning("⚠️ Validation Error: You cannot post this clearing document without entering an accounting reason note.")
        else:
            st.success(f"Success! Payment {selected_pmt} linked to invoice. SAP FI ledger updated.")
with col_btn2:
    if st.button("❌ Flag to Dispute Queue"):
        st.error(f"Payment {selected_pmt} routed to Customer Dispute Desk. Notice transmitted to Sales Cloud.")
