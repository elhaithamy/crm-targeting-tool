import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Churn Campaign Tool", layout="wide")

st.title("📉 CRM Churn Campaign Management Dashboard")
st.write("Goal: Reduce churn rate to 25% by identifying and targeting low-activity segments.")

st.sidebar.header("📤 Upload Churn Campaign Excel File")
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

            st.subheader("📊 Full Campaign Data with Calculated Segment & Promo Suggestion")
            st.dataframe(df)

            # Filter & summarize by store and segment
            st.subheader("🏬 Recommended Targeting Summary by Store & Segment")

            grouped = (
                df.groupby(["Store", "Segment"])
                .agg(
                    Customers=("Customer_ID", "count"),
                    Avg_Last_Order_Value=("Last_Order_Value", "mean")
                )
                .reset_index()
                .sort_values(by=["Store", "Segment"])
            )

            st.dataframe(grouped)

            st.success("✅ Analysis complete. Use this data to launch targeted campaigns.")

    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
else:
    st.info("📄 Please upload an Excel file with the required columns to get started.")
