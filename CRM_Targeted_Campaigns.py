import streamlit as st
import pandas as pd
from io import BytesIO
import datetime

st.set_page_config(page_title="CRM Churn Campaign Planner", layout="wide")

st.title("📊 CRM Campaign Targeting Dashboard")

uploaded_file = st.file_uploader("📤 Upload Churn Campaign Excel File", type=["xlsx"])
campaign_history = st.session_state.get("campaign_history", [])

SEGMENT_TIERS = {
    "A": 1500,
    "B": 1000,
    "C": 500,
    "D": 0
}

def calculate_segment(value):
    for seg, threshold in SEGMENT_TIERS.items():
        if value >= threshold:
            return seg
    return "D"

def suggested_promo(seg):
    return {
        "A": "No Promo",
        "B": "EGP 100",
        "C": "EGP 150",
        "D": "EGP 200"
    }.get(seg, "EGP 200")

def basket_cap(seg):
    return {
        "A": 1800,
        "B": 1500,
        "C": 1000,
        "D": 500
    }.get(seg, 500)

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df["Segment"] = df["Last_Order_Value"].apply(calculate_segment)
    df["Suggested_Promo"] = df["Segment"].apply(suggested_promo)
    df["Target_Basket_Cap"] = df["Segment"].apply(basket_cap)

    st.subheader("📋 Full Campaign Data with Segment & Promo Suggestions")
    st.dataframe(df)

    target_customers = df[df["Last_Order_Date"] < pd.to_datetime("today") - pd.to_timedelta("60d")]

    st.subheader("🎯 Recommended Targeting Summary by Store & Segment")

    summary = (
        target_customers.groupby(["Store", "Segment"])
        .size()
        .reset_index(name="Customers_To_Target")
        .sort_values(by=["Segment", "Customers_To_Target"], ascending=[True, False])
    )

    # Estimate order increase (fake logic here - adjust to match real uplift data)
    orders_increase = (
        target_customers.groupby("Store")
        .size()
        .reset_index(name="Targetable_Customers")
    )
    orders_increase["Est_Order_Increase_%"] = orders_increase["Targetable_Customers"] * 2  # simple placeholder

    st.dataframe(summary)
    st.subheader("📈 Estimated Order Impact by Store")
    st.dataframe(orders_increase)

    st.subheader("📤 Download Target Customer List")
    to_download = target_customers[[
        "Customer_ID", "Store", "Last_Order_Date", "Last_Order_Value", "Segment", "Suggested_Promo", "Target_Basket_Cap"
    ]]
    buffer = BytesIO()
    to_download.to_excel(buffer, index=False)
    st.download_button("📥 Download Excel for CRM Team", data=buffer.getvalue(),
                       file_name="Target_Customers_List.xlsx")

    # Update campaign history
    if st.button("✅ Update Campaign History"):
        df["Campaign_Updated_At"] = datetime.datetime.now()
        campaign_history.append(df)
        st.session_state["campaign_history"] = campaign_history
        st.success("Campaign history updated!")

    if campaign_history:
        st.subheader("🕘 Campaign History")
        history_df = pd.concat(campaign_history)
        st.dataframe(history_df)
