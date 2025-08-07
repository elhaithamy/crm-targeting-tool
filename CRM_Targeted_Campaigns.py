import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Churn Campaign Targeting Tool", layout="wide")
st.title("📊 Churn Campaign Targeting Dashboard")

st.markdown("""
Upload your Excel file containing the churn campaign customer list. 

**Expected Columns:**
- `Customer_ID`
- `Campaign_Name`
- `Segment`
- `Store`
- `Campaign_Date`
- `Last_Order_Date`
- `Last_Order_Value`
- `Notes`

The tool will analyze which customers/stores need re-engagement based on the **Last_Order_Value** and **Last_Order_Date**, and recommend suitable **promo code values** to increase basket size.
""")

# Upload file
uploaded_file = st.file_uploader("📤 Upload Churn Campaign Excel File", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Convert dates
    df['Last_Order_Date'] = pd.to_datetime(df['Last_Order_Date'])
    df['Campaign_Date'] = pd.to_datetime(df['Campaign_Date'])
    df['Days_Since_Last_Order'] = (pd.Timestamp.today() - df['Last_Order_Date']).dt.days

    # Define segments based on Last_Order_Value
    def define_segment(value):
        if value >= 1500:
            return "A"
        elif 1000 <= value < 1500:
            return "B"
        elif 500 <= value < 1000:
            return "C"
        else:
            return "D"

    df['Calculated_Segment'] = df['Last_Order_Value'].apply(define_segment)

    # Promo suggestions
    def suggest_promo(segment):
        if segment == "A":
            return "EGP 0–50 Loyalty Reward"
        elif segment == "B":
            return "EGP 75–100 Upgrade Bonus"
        elif segment == "C":
            return "EGP 100–150 Recovery Push"
        else:
            return "EGP 150–200+ Resurrection Promo"

    df['Suggested_Promo'] = df['Calculated_Segment'].apply(suggest_promo)

    # Prioritize re-targeting
    df['Targeting_Priority'] = df.apply(lambda row: '🎯 High' if row['Calculated_Segment'] in ['C', 'D'] and row['Days_Since_Last_Order'] > 30 else 'Normal', axis=1)

    st.success("✅ Analysis Complete")

    with st.expander("📋 View Full Processed Data"):
        st.dataframe(df)

    with st.expander("🏪 Targeting Summary by Store"):
        summary = df[df['Targeting_Priority'] == '🎯 High'].groupby(['Store', 'Calculated_Segment']).agg({
            'Customer_ID': 'count'
        }).rename(columns={'Customer_ID': 'Target_Customers'}).reset_index()
        st.dataframe(summary)

    with st.expander("⬇️ Download Processed Report"):
        st.download_button("Download Excel", df.to_excel(index=False), file_name="Churn_Targeting_Results.xlsx")

else:
    st.info("👆 Please upload a valid Excel sheet to begin.")
