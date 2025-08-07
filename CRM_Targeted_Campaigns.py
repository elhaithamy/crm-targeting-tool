import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Churn Campaign Tool", layout="wide")

st.title("📉 CRM Churn Campaign Management Dashboard")
st.write("Goal: Reduce churn rate to 25% by identifying and targeting low-activity segments.")

st.sidebar.header("📄 Upload Churn Campaign Excel File")
uploaded_file = st.sidebar.file_uploader("Upload your Excel file", type=["xlsx"])

# Define segment logic
def assign_segment(order_value):
    if order_value >= 1500:
        return "A"
    elif order_value >= 1000:
        return "B"
    elif order_value >= 500:
        return "C"
    else:
        return "D"

def suggest_promo(segment):
    return {
        "A": "EGP 50",
        "B": "EGP 75",
        "C": "EGP 100",
        "D": "EGP 150"
    }[segment]

def target_basket_value_cap(segment):
    return {
        "A": 1800,
        "B": 1400,
        "C": 900,
        "D": 600
    }[segment]

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)

        required_columns = [
            "Customer_ID", "Campaign_Name", "Store",
            "Campaign_Date", "Last_Order_Date", "Last_Order_Value", "Notes"
        ]

        if not all(col in df.columns for col in required_columns):
            st.error(f"❌ Missing columns. Expected columns: {', '.join(required_columns)}")
        else:
            df["Segment"] = df["Last_Order_Value"].apply(assign_segment)
            df["Promo_Suggestion"] = df["Segment"].apply(suggest_promo)
            df["Target_Basket_Value"] = df["Segment"].apply(target_basket_value_cap)

            st.subheader("📊 Full Campaign Data with Calculated Segment, Promo Suggestion & Target Basket Value")
            st.dataframe(df)

            # Recommended Targeting Summary
            st.subheader("🏬 Recommended Targeting Summary by Store & Segment")
            grouped = (
                df.groupby(["Store", "Segment"])
                .agg(
                    Customers=("Customer_ID", "count"),
                    Avg_Last_Order_Value=("Last_Order_Value", "mean"),
                    Total_Last_Order_Value=("Last_Order_Value", "sum")
                )
                .reset_index()
                .sort_values(by=["Store", "Segment"])
            )

            st.dataframe(grouped)

            # Prioritized Targeting List
            st.subheader("⬆️ Prioritized Targeting by Store Based on High Basket Potential")
            prioritized = (
                df.groupby("Store")
                .agg(
                    Total_Customers=("Customer_ID", "count"),
                    Avg_Basket_Value=("Last_Order_Value", "mean"),
                    Total_Potential_Revenue=("Target_Basket_Value", "sum")
                )
                .reset_index()
                .sort_values(by="Avg_Basket_Value", ascending=False)
            )

            prioritized["Estimated_Recovery_Success_%"] = prioritized["Avg_Basket_Value"].apply(lambda x: min(95, max(50, round(x / 20))))
            prioritized["Orders_Recovery_Potential_%"] = ((prioritized["Total_Potential_Revenue"] - prioritized["Avg_Basket_Value"] * prioritized["Total_Customers"]) / (prioritized["Avg_Basket_Value"] * prioritized["Total_Customers"])) * 100

            st.dataframe(prioritized)

            st.success("✅ Targeting insights generated. Use them to prioritize and optimize campaign execution.")

    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
else:
    st.info("📄 Please upload an Excel file with the required columns to get started.")
