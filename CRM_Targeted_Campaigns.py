import streamlit as st
import pandas as pd
import datetime
from io import BytesIO

st.set_page_config(page_title="CRM Targeting Tool", layout="wide")
st.title("🧲 CRM Campaign Targeting & Conversion Tool")

# Campaign Name input - Mandatory
campaign_name_input = st.text_input("📝 Enter Campaign Name (required):")

if not campaign_name_input:
    st.warning("⚠️ Please enter a campaign name to proceed.")
    st.stop()

uploaded_file = st.file_uploader("📤 Upload Campaign Input Excel File", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Convert dates
    df["Campaign_Start_Date"] = pd.to_datetime(df["Campaign_Start_Date"])
    df["Campaign_End_Date"] = pd.to_datetime(df["Campaign_End_Date"])
    df["Last_Order_Date"] = pd.to_datetime(df["Last_Order_Date"], errors="coerce")

    # Assign Segment
    def assign_segment(val):
        if pd.isna(val):
            return "Segment D"
        elif val >= 1500:
            return "Segment A"
        elif 1000 <= val < 1500:
            return "Segment B"
        elif 500 <= val < 1000:
            return "Segment C"
        else:
            return "Segment D"

    df["Segment"] = df["Last_Order_Value"].apply(assign_segment)

    # Assign recommended target basket
    df["Recommended_Target_Basket"] = df["Segment"].map({
        "Segment A": 1500,
        "Segment B": 1000,
        "Segment C": 500,
        "Segment D": 500
    })

    # Determine conversion
    def is_converted(row):
        if pd.isna(row["Last_Order_Date"]):
            return False
        return row["Campaign_Start_Date"] <= row["Last_Order_Date"] <= row["Campaign_End_Date"]

    df["Converted"] = df.apply(is_converted, axis=1)

    # Count orders per customer during campaign
    df["Orders_Count_During_Campaign"] = df.apply(
        lambda row: 1 if row["Converted"] else 0, axis=1
    )

    # Targeted customers (all customers in this campaign)
    targeted_df = df.copy()

    # Non-converted customers
    non_converted_df = df[~df["Converted"]].copy()

    st.subheader("🎯 Non-Converted Customers")
    st.dataframe(non_converted_df[[
        "Customer_ID", "Store", "Segment", "Recommended_Target_Basket",
        "Campaign_Name", "Notes"
    ]])

    st.subheader("📊 Conversion & Promo Usage Summary")
    summary = df.groupby("Converted").agg({
        "Customer_ID": "count",
        "Used_Promo_Code": "sum"
    }).rename(columns={"Customer_ID": "Customer Count", "Used_Promo_Code": "Promo Code Used"})
    st.dataframe(summary)

    # Helper function to create Excel download
    def convert_df_to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        output.seek(0)
        return output

    st.download_button(
        label="📥 Download All Targeted Customers (Including Converted)",
        data=convert_df_to_excel(targeted_df),
        file_name=f"{campaign_name_input}_All_Targeted_Customers.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.download_button(
        label="📥 Download Non-Converted Customers Only",
        data=convert_df_to_excel(non_converted_df),
        file_name=f"{campaign_name_input}_Non_Converted_Customers.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
