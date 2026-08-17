import streamlit as st
import pandas as pd

st.set_page_config(page_title="P2P Three-Way Match", layout="wide")

st.title("Vegetable Supplier - Three-Way Match Checker")
st.caption("P2P Scenario: Restaurant chain catching PO vs Goods Receipt vs Invoice mismatches")

# ---------- STEP 1: SEED DATA ----------
# Fake sample data — like a small SAP purchase table.
# PO Qty = what we ordered, GR Qty = what actually arrived, Invoice Qty = what supplier billed us

if "orders" not in st.session_state:
    st.session_state.orders = pd.DataFrame([
        {"PO Number": "PO501", "Supplier": "Green Farms Co",  "PO Qty (crates)": 10, "GR Qty (crates)": 8,  "Invoice Qty (crates)": 10},
        {"PO Number": "PO502", "Supplier": "Fresh Veg Suppliers", "PO Qty (crates)": 15, "GR Qty (crates)": 15, "Invoice Qty (crates)": 15},
        {"PO Number": "PO503", "Supplier": "Green Farms Co",  "PO Qty (crates)": 20, "GR Qty (crates)": 18, "Invoice Qty (crates)": 20},
        {"PO Number": "PO504", "Supplier": "Daily Harvest Ltd", "PO Qty (crates)": 12, "GR Qty (crates)": 12, "Invoice Qty (crates)": 14},
    ])

df = st.session_state.orders.copy()

# ---------- STEP 2: FLAG MISMATCHES ----------
# Simple check: if GR Qty or Invoice Qty is different from PO Qty, it's a mismatch

def check_match(row):
    if row["GR Qty (crates)"] == row["PO Qty (crates)"] == row["Invoice Qty (crates)"]:
        return "Matched"
    else:
        return "Mismatch - Needs Review"

df["Match Status"] = df.apply(check_match, axis=1)

# ---------- STEP 3: SHOW TABLE ----------
st.subheader("Purchase Orders - Three-Way Match Status")
st.dataframe(df, use_container_width=True)

st.info("Part 1 done: data + auto mismatch flagging. Next step: filter to show ONLY mismatches, and add an action button.")