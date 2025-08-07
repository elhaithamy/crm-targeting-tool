import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="CRM Targeting Tool", layout="wide")
st.title("🧲 CRM Campaign Targeting & Conversion Tool")

uploaded_file = st.file_uploader("📤 Upload Campaign Input Excel File", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Campaign Name input
    campaign_name_input = st.text_input("Enter Campaign Name (for new or updating existing):")

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

    # Targeted customers
    target_df = df[~df["Converted"]].copy()

    st.subheader("🎯 Targeted Customers (Did Not Convert)")
    st.dataframe(target_df[[
        "Customer_ID", "Store", "Segment", "Recommended_Target_Basket",
        "Campaign_Name", "Notes"
    ]])

    st.subheader("📊 Conversion & Promo Usage Summary")
    summary = df.groupby("Converted").agg({
        "Customer_ID": "count",
        "Used_Promo_Code": "sum"
    }).rename(columns={"Customer_ID": "Customer Count", "Used_Promo_Code": "Promo Code Used"})
    st.dataframe(summary)

    # Export
    if st.button("📥 Export Targeted Customers Excel"):
        output_file = f"{campaign_name_input}_Targeted_Customers.xlsx"
        target_df.to_excel(output_file, index=False)
        st.success(f"Targeted customers exported as: {output_file}")

    # Save campaign history
    if st.button("💾 Update Campaign History"):
        # Here you would append to or update a central Excel file/database
        st.success("Campaign history updated (simulation).")
