import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

st.set_page_config(layout="wide", page_title="CRM Targeted Campaigns", initial_sidebar_state="expanded")

st.title("🎯 CRM Targeted Campaign Tool")

# Step 1: Campaign Name input
campaign_name = st.text_input("📌 Enter Campaign Name", max_chars=100)

# Step 2: File Upload
uploaded_file = st.file_uploader("📂 Upload Campaign Excel File", type=["xlsx", "xls"])

if campaign_name and uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)

        # Data Cleaning
        df.columns = df.columns.str.strip()
        df["Used_Promo_Code"] = df["Used_Promo_Code"].fillna(False)
        df["Used_Promo_Code"] = df["Used_Promo_Code"].astype(bool)
        df["Last_Order_Value"] = pd.to_numeric(df["Last_Order_Value"], errors="coerce").fillna(0)

        # Add Segment
        def get_segment(value):
            if value >= 1500:
                return "A"
            elif value >= 1000:
                return "B"
            elif value >= 500:
                return "C"
            else:
                return "D"

        df["Segment"] = df["Last_Order_Value"].apply(get_segment)

        # Conversion Status
        df["Converted"] = df["Last_Order_Date"].notnull()

        # Recommendations
        def recommend_basket(segment):
            return {
                "A": "2500 EGP",
                "B": "1750 EGP",
                "C": "1000 EGP",
                "D": "500 EGP"
            }.get(segment, "500 EGP")

        df["Recommended_Target_Basket"] = df["Segment"].apply(recommend_basket)
        df["Campaign_Name"] = campaign_name

        # Split data
        target_df = df[df["Converted"]]
        non_converted_df = df[~df["Converted"]]

        # Summary
        total_targeted = len(df)
        total_converted = len(target_df)
        total_promo_used = df["Used_Promo_Code"].sum()

        with st.expander("📊 Conversion & Promo Usage Summary", expanded=True):
            st.metric("🎯 Total Targeted", total_targeted)
            st.metric("✅ Converted", total_converted)
            st.metric("💸 Used Promo Code", int(total_promo_used))

            # Bar Chart
            chart_labels = ["Targeted", "Converted", "Promo Used"]
            chart_values = [total_targeted, total_converted, total_promo_used]
            percentages = [round((v / total_targeted) * 100, 1) for v in chart_values]

            fig, ax = plt.subplots(figsize=(6, 4))
            bars = ax.bar(chart_labels, percentages)
            for bar, pct in zip(bars, percentages):
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{pct}%', ha='center', va='bottom')
            ax.set_ylim(0, 100)
            ax.set_ylabel("Percentage")
            ax.set_title("📈 Campaign Performance")
            st.pyplot(fig)

        # Targeted Customers Table
        with st.expander("📋 Converted Customers"):
            st.dataframe(target_df[[
                "Customer_ID", "Store", "Segment", "Recommended_Target_Basket",
                "Campaign_Name", "Last_Order_Value", "Used_Promo_Code", "Notes"
            ]])

            # Download button
            target_excel = BytesIO()
            target_df.to_excel(target_excel, index=False)
            st.download_button("📥 Download Converted Customers", target_excel.getvalue(), file_name="converted_customers.xlsx")

        # Non-Converted Customers Table
        with st.expander("🕳️ Non-Converted Customers"):
            st.dataframe(non_converted_df[[
                "Customer_ID", "Store", "Segment", "Recommended_Target_Basket",
                "Campaign_Name", "Last_Order_Value", "Used_Promo_Code", "Notes"
            ]])

            non_converted_excel = BytesIO()
            non_converted_df.to_excel(non_converted_excel, index=False)
            st.download_button("📥 Download Non-Converted Customers", non_converted_excel.getvalue(), file_name="non_converted_customers.xlsx")
        # 📍 Recommendations Section
        with st.expander("📍 Next Steps Recommendations", expanded=True):
            st.subheader("💡 Suggested Actions")

            conversion_rate = (total_converted / total_targeted) * 100 if total_targeted > 0 else 0
            promo_usage_rate = (total_promo_used / total_targeted) * 100 if total_targeted > 0 else 0

            recommendations = []

            if conversion_rate < 30:
                recommendations.append("🔁 Consider retargeting non-converted customers with a stronger value proposition or reminder.")
            else:
                recommendations.append("✅ Good conversion rate. Consider scaling the campaign or repeating for similar segments.")

            if promo_usage_rate < 15:
                recommendations.append("💬 Low promo code usage — test different incentives or highlight them more clearly in your messages.")
            elif promo_usage_rate > 50:
                recommendations.append("⚠️ High promo code usage — evaluate the impact on profitability and consider limits per customer.")

            if len(non_converted_df) > 0:
                recommendations.append("📞 Trigger follow-up communication for non-converted customers (email/SMS/WhatsApp).")

            if "D" in non_converted_df["Segment"].value_counts():
                recommendations.append("📉 Customers in Segment D may require tailored low-basket incentives or education on higher value benefits.")

            if "A" in target_df["Segment"].value_counts():
                recommendations.append("🏆 Segment A customers responded well — consider loyalty or subscription program promotion.")

            for rec in recommendations:
                st.markdown(f"- {rec}")

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
else:
    st.info("ℹ️ Please enter the campaign name and upload the campaign Excel file to proceed.")
