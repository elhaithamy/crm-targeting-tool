import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="CRM Campaign Tracker", layout="wide")

st.title("📈 CRM Campaign Conversion & Promo Tracker")

# Upload campaign input file
campaign_file = st.file_uploader("📥 Upload Campaign Excel File", type=["xlsx"])

# Prompt campaign name before saving
campaign_name_input = st.text_input("📝 Enter Campaign Name to Save or Update History")

if campaign_file:
    df = pd.read_excel(campaign_file)

    # Parse dates
    df['Campaign_Start_Date'] = pd.to_datetime(df['Campaign_Start_Date'], errors='coerce')
    df['Campaign_End_Date'] = pd.to_datetime(df['Campaign_End_Date'], errors='coerce')
    df['Last_Order_Date'] = pd.to_datetime(df['Last_Order_Date'], errors='coerce')

    # Determine if customer converted
    df['Converted'] = df.apply(
        lambda row: pd.notna(row['Last_Order_Date']) and row['Campaign_Start_Date'] <= row['Last_Order_Date'] <= row['Campaign_End_Date'],
        axis=1
    )

    # Count number of orders if customer converted
    order_counts = df[df['Converted']].groupby('Customer_ID').size().reset_index(name='Orders_During_Campaign')
    df = df.merge(order_counts, on='Customer_ID', how='left')
    df['Orders_During_Campaign'] = df['Orders_During_Campaign'].fillna(0).astype(int)

    # Check if promo was used
    df['Used_Promo_Code'] = df['Used_Promo_Code'].astype(str).str.lower().str.strip().isin(['yes', 'y', 'true', '1'])

    # Segment based on Last_Order_Value
    def segment(value):
        if value >= 1500:
            return 'Segment A'
        elif 1000 <= value < 1500:
            return 'Segment B'
        elif 500 <= value < 1000:
            return 'Segment C'
        elif value < 500:
            return 'Segment D'
        return 'Unknown'

    df['Segment'] = df['Last_Order_Value'].apply(segment)

    # Conversion Summary
    st.subheader("📊 Conversion & Promo Usage Summary")
    summary = df.groupby('Store').agg(
        Total_Customers=('Customer_ID', 'count'),
        Converted_Customers=('Converted', lambda x: x.sum()),
        Promo_Used=('Used_Promo_Code', lambda x: x.sum()),
        Avg_Orders_Per_Converted=('Orders_During_Campaign', lambda x: x[x > 0].mean())
    ).reset_index()

    summary['Conversion_Rate (%)'] = (summary['Converted_Customers'] / summary['Total_Customers'] * 100).round(2)
    summary['Promo_Usage_Rate (%)'] = (summary['Promo_Used'] / summary['Total_Customers'] * 100).round(2)

    st.dataframe(summary)

    # Target list
    st.subheader("🎯 Customers Targeted (Filtered by Non-converted)")
    target_df = df[~df['Converted']]
    target_df['Recommended_Target_Basket'] = target_df['Segment'].map({
        'Segment A': 1500,
        'Segment B': 1000,
        'Segment C': 500,
        'Segment D': 500
    })

    st.dataframe(target_df[['Customer_ID', 'Store', 'Segment', 'Recommended_Target_Basket', 'Campaign_Name', 'Notes']])

    # Save campaign history
    if campaign_name_input and st.button("💾 Update Campaign History"):
        filename = f"campaign_history_{campaign_name_input.replace(' ', '_')}.xlsx"
        target_df.to_excel(filename, index=False)
        st.success(f"Campaign history saved as {filename}")

    # Allow download of filtered target list
    @st.cache_data
    def convert_df_to_excel(dataframe):
        from io import BytesIO
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            dataframe.to_excel(writer, index=False)
        return output.getvalue()

    st.download_button(
        label="⬇️ Download Target Customers Excel",
        data=convert_df_to_excel(target_df),
        file_name=f"{campaign_name_input}_Target_Customers.xlsx" if campaign_name_input else "Target_Customers.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
