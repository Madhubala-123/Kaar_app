import streamlit as st
import pandas as pd

# 1. Page Configuration & Layout
st.set_page_config(page_title="SAP O2C Cockpit", layout="wide")
st.title("🏭 SAP Order-to-Cash (O2C) Credit Management Dashboard")
st.caption("Aligned with Chapter 2.1 — Manage Credit / Release (VKM1/VKM3)")
st.write("---")

# 2. Sidebar Navigation
page = st.sidebar.radio("Navigate Menu", ["📋 Pending Sales Orders", "🔍 Customer Master Data"])

# --- PAGE 1: PENDING ORDERS ---
if page == "📋 Pending Sales Orders":
    # Section 2.1 Business KPIs (Displaying metrics at the top)
    st.subheader("📊 Key Performance Indicators (KPIs)")
    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    with col_kpi1:
        st.metric(label="Days Sales Outstanding (DSO)", value="42 Days", delta="-3 Days (Improving)")
    with col_kpi2:
        st.metric(label="On-Time-In-Full (OTIF)", value="94.2%", delta="+1.5%")
    with col_kpi3:
        st.metric(label="Credit Exposure Total", value="₹12,45,000", delta="High Risk Alert", delta_color="inverse")

    st.write("---")

    # SAP Process Flow Table (Representing real SAP objects and statuses)
    st.subheader("📋 Orders Blocked due to Credit Limit Failures")

    # Fixed data dictionary with complete array lists
    sap_orders = {
        "Sales Order (VA01)":,
        "Customer Name": ["Reliance Retail", "Kiran Electronics", "Mahesh Enterprises"],
        "Order Value (INR)":,
        "Available Credit Limit (INR)":,
        "Payment History Delays": ["3 Times", "0 Times", "7 Times"]
    }
    df = pd.DataFrame(sap_orders)

    # Grounded AI Element: Simulating a predictive risk scoring algorithm based on historical data
    def calculate_ai_risk(row):
        if row["Order Value (INR)"] > row["Available Credit Limit (INR)"] and "7" in row["Payment History Delays"]:
            return "🔴 HIGH RISK (Reject Advised)"
        elif row["Order Value (INR)"] > row["Available Credit Limit (INR)"]:
            return "🟡 MEDIUM RISK (Review Needed)"
        return "🟢 SAFE"

    df["AI Decision Support"] = df.apply(calculate_ai_risk, axis=1)
    st.dataframe(df, use_container_width=True)

    # Process Validation and Actions
    st.write("---")
    st.subheader("🛠️ Executive Action Panel")

    selected_order = st.selectbox("Select Sales Order to Process:", df["Sales Order (VA01)"])
    action_reason = st.text_input("Enter business justification for release/rejection:")

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🚀 Override & Release (Create Delivery - VL01N)", type="primary"):
            if not action_reason:
                st.warning("⚠️ Validation Error: You must enter a business justification before overriding credit rules.")
            else:
                st.success(f"Success! Order {selected_order} has been approved. System triggered Delivery document generation.")
    with col_btn2:
        if st.button("❌ Reject & Block Order"):
            st.error(f"Order {selected_order} permanently blocked. Financial Accounting notified.")

# --- PAGE 2: CUSTOMER MASTER DATA ---
elif page == "🔍 Customer Master Data":
    st.subheader("SAP Central Customer Repository")
    search_name = st.text_input("Search Customer Name:")
    if search_name:
        st.success(f"Displaying Master Record for: {search_name}")
        st.json({
            "Customer ID": "CUST_990412",
            "Billing Country": "India",
            "Payment Terms": "NET30 (Pay within 30 days)",
            "Risk Category": "Strategic Partner"
        })
