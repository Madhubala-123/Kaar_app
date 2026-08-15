import streamlit as st

st.title("📦 SAP Order-to-Cash Cockpit")
st.write("Welcome, Kaar Tech Evaluators! This is a live preview.")

customer = st.text_input("Enter Customer Name:")
if customer:
    st.success(f"Successfully loaded master data for: {customer}")
