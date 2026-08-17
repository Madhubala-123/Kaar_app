import streamlit as st
import pandas as pd

st.set_page_config(page_title="P2P Three-Way Match", layout="wide")

st.title("Vegetable Supplier - Three-Way Match Checker")
st.caption("P2P Scenario: Restaurant chain catching PO vs Goods Receipt vs Invoice mismatches")

# ---------- STEP 1: SEED DATA ----------
if "orders" not in st.session_state:
    st.session_state.orders = pd.DataFrame([
        {"PO Number": "PO501", "Supplier": "Green Farms Co",     "PO Qty (crates)": 10, "GR Qty (crates)": 8,  "Invoice Qty (crates)": 10, "Status": "Open"},
        {"PO Number": "PO502", "Supplier": "Fresh Veg Suppliers","PO Qty (crates)": 15, "GR Qty (crates)": 15, "Invoice Qty (crates)": 15, "Status": "Open"},
        {"PO Number": "PO503", "Supplier": "Green Farms Co",     "PO Qty (crates)": 20, "GR Qty (crates)": 18, "Invoice Qty (crates)": 20, "Status": "Open"},
        {"PO Number": "PO504", "Supplier": "Daily Harvest Ltd",  "PO Qty (crates)": 12, "GR Qty (crates)": 12, "Invoice Qty (crates)": 14, "Status": "Open"},
    ])

df = st.session_state.orders.copy()

# ---------- STEP 2: MATCH STATUS ----------
def check_match(row):
    if row["GR Qty (crates)"] == row["PO Qty (crates)"] == row["Invoice Qty (crates)"]:
        return "Matched"
    return "Mismatch"

df["Match Status"] = df.apply(check_match, axis=1)

# ---------- STEP 3: AI SEVERITY (grounded on the actual gap, not random) ----------
def ai_severity(row):
    if row["Match Status"] == "Matched":
        return "-"
    gap = abs(row["Invoice Qty (crates)"] - row["GR Qty (crates)"])
    if gap >= 3:
        return "HIGH - Large quantity gap"
    else:
        return "LOW - Minor gap, quick check"

df["AI Severity"] = df.apply(ai_severity, axis=1)

# ---------- STEP 4: KPI ROW ----------
st.subheader("Key Numbers")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Purchase Orders", len(df))
with col2:
    st.metric("Mismatches Found", (df["Match Status"] == "Mismatch").sum())
with col3:
    st.metric("High Severity Cases", (df["AI Severity"] == "HIGH - Large quantity gap").sum())

st.write("---")

# ---------- STEP 5: FILTER VIEW ----------
st.subheader("Purchase Orders")
view_choice = st.radio("Show:", ["All Orders", "Only Mismatches"], horizontal=True)

if view_choice == "Only Mismatches":
    display_df = df[df["Match Status"] == "Mismatch"]
else:
    display_df = df

st.dataframe(display_df, width='stretch')

st.write("---")

# ---------- STEP 6: ACTION PANEL ----------
st.subheader("Action Panel")

mismatch_ids = df[df["Match Status"] == "Mismatch"]["PO Number"].tolist()

if mismatch_ids:
    selected_po = st.selectbox("Select a mismatched PO to act on:", mismatch_ids)
    note = st.text_input("Add a note (why reviewed / escalated):")

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("Mark as Reviewed", type="primary"):
            if not note:
                st.warning("Please add a note before marking as reviewed.")
            else:
                idx = st.session_state.orders[st.session_state.orders["PO Number"] == selected_po].index
                st.session_state.orders.loc[idx, "Status"] = "Reviewed"
                st.success(f"{selected_po} marked as Reviewed.")
    with col_b:
        if st.button("Escalate to Finance"):
            idx = st.session_state.orders[st.session_state.orders["PO Number"] == selected_po].index
            st.session_state.orders.loc[idx, "Status"] = "Escalated"
            st.error(f"{selected_po} escalated to Finance team for supplier follow-up.")
else:
    st.success("No mismatches currently - all orders are clean.")
