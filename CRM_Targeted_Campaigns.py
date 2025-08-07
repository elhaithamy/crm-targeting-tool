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

    # Standardize column names (remove leading/trailing spaces, handle case sensitivity)
    df.columns = df.columns.str.strip()

    expected_columns = [
        "Customer_ID", "Campaign_Name", "Store", "Campaign_Start_Date",
        "Campaign_End_Date", "Last_Order_Date", "Last_Order_Value",
        "Used_Promo_Code", "Notes"
    ]

    missing_cols = [col for col in expected_columns if col not in df.columns]
    if missing_cols:
        st.error(f"❌ Missing required columns: {missing_cols}")
        st.stop()

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

    # Count orders during campaign (set to 1 if converted, you can enhance this logic later)
    df["Orders_Count_During_Campaign"] = df["Converted"].apply(lambda x: 1 if x else 0)

    targeted_df = df.copy()
    non_converted_df = df[~df["Converted"]].copy()

    st.subheader("🎯 Non-Converted Customers")
    preview_cols = [
        col for col in ["Customer_ID", "Store", "Segment", "Recommended_Target_Basket",
                        "Campaign_Name", "Notes"]
        if col in non_converted_df.columns
    ]
    st.dataframe(non_converted_df[preview_cols])

    st.subheader("📊 Conversion & Promo Usage Summary")
    summary = df.groupby("Converted").agg({
        "Customer_ID": "count",
        "Used_Promo_Code": lambda x: x.fillna(False).sum()
    }).rename(columns={"Customer_ID": "Customer Count", "Used_Promo_Code": "Promo Code Used"})
    st.dataframe(summary)

    # Download helpers
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

import matplotlib.pyplot as plt

# Chart Data Preparation
total_targeted = len(df)
total_converted = df["Converted"].sum()
promo_code_used = df["Used_Promo_Code"].fillna(False).sum()

chart_labels = ["Targeted", "Converted", "Promo Used"]
chart_values = [
    total_targeted,
    total_converted,
    promo_code_used
]

# Convert to percentages
percentages = [round((v / total_targeted) * 100, 1) for v in chart_values]

# Plotting
fig, ax = plt.subplots()
bars = ax.bar(chart_labels, percentages)

# Add % labels on top of each bar
for bar, pct in zip(bars, percentages):
    height = bar.get_height()
    ax.annotate(f"{pct}%", xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 5), textcoords="offset points",
                ha='center', va='bottom')

ax.set_ylim(0, 100)
ax.set_ylabel("Percentage")
ax.set_title("🎯 Campaign Performance Metrics (%)")

st.pyplot(fig)

