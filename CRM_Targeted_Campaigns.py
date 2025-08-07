import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
from datetime import datetime

st.set_page_config(page_title="CRM Targeted Campaigns", layout="wide")
st.title("📊 CRM Targeted Campaign Manager")

# Step 1: Upload File
uploaded_file = st.file_uploader("Upload Customer Campaign Excel File", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Validate required columns
    required_columns = [
        "Customer_ID", "Campaign_Name", "Store", "Campaign_Start_Date", "Campaign_End_Date",
        "Last_Order_Date", "Last_Order_Value", "Used_Promo_Code", "Notes"
    ]
    if not all(col in df.columns for col in required_columns):
        st.error(f"❌ Uploaded file must contain the following columns: {', '.join(required_columns)}")
        st.stop()

    # Parse dates
    df["Campaign_Start_Date"] = pd.to_datetime(df["Campaign_Start_Date"], errors='coerce')
    df["Campaign_End_Date"] = pd.to_datetime(df["Campaign_End_Date"], errors='coerce')
    df["Last_Order_Date"] = pd.to_datetime(df["Last_Order_Date"], errors='coerce')

    # Step 2: Campaign Name Input
    campaign_name = st.text_input("Enter Campaign Name (Required to Continue)")
    if not campaign_name:
        st.warning("⚠️ Please enter a campaign name to proceed.")
        st.stop()

    # Filter for current campaign
    campaign_df = df[df["Campaign_Name"] == campaign_name].copy()

    if campaign_df.empty:
        st.error("❌ No data found for the provided campaign name.")
        st.stop()

    # Clean and prepare data
    campaign_df["Used_Promo_Code"] = campaign_df["Used_Promo_Code"].astype(str).str.lower().str.strip()

    # Step 3: Campaign Summary
    st.subheader("📈 Campaign Summary")
    total_targeted = len(campaign_df)
    total_converted = campaign_df["Last_Order_Date"].notna().sum()
    total_used_promo = campaign_df["Used_Promo_Code"].eq("yes").sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("🎯 Total Targeted", total_targeted)
    col2.metric("✅ Converted", total_converted)
    col3.metric("🏷️ Promo Code Used", total_used_promo)

    # Step 4: Conversion Chart
    st.subheader("📊 Conversion & Promo Usage Summary")
    summary_chart = pd.DataFrame({
        "Metric": ["Targeted", "Converted", "Promo Code Used"],
        "Count": [total_targeted, total_converted, total_used_promo]
    })
    fig, ax = plt.subplots()
    ax.bar(summary_chart["Metric"], summary_chart["Count"])
    ax.set_ylabel("# of Customers")
    ax.set_title("Campaign Performance")
    st.pyplot(fig)

    # Step 5: Export Buttons
    st.subheader("📤 Export Lists")
    converted_customers = campaign_df[campaign_df["Last_Order_Date"].notna()]
    non_converted_customers = campaign_df[campaign_df["Last_Order_Date"].isna()]

    def convert_df_to_excel(df):
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        return output.getvalue()

    col1, col2 = st.columns(2)
    with col1:
        st.download_button("Download Converted Customers", data=convert_df_to_excel(converted_customers),
                           file_name=f"converted_customers_{campaign_name}.xlsx")
    with col2:
        st.download_button("Download Non-Converted Customers", data=convert_df_to_excel(non_converted_customers),
                           file_name=f"non_converted_customers_{campaign_name}.xlsx")

    # Step 6: Store Priority Selection
    st.subheader("🏪 Store Prioritization")
    unique_stores = sorted(campaign_df["Store"].dropna().unique())
    store_priorities = {}
    for store in unique_stores:
        store_priorities[store] = st.selectbox(
            f"Set priority for {store}", [1, 2, 3], key=f"priority_{store}"
        )

    # Step 7: Recommendations
    st.subheader("🧠 Next-Step Recommendations")
    target_churn_recovery = 0.25  # 25% recovery goal
    current_recovery = total_converted / total_targeted if total_targeted > 0 else 0
    customers_needed = int((target_churn_recovery * total_targeted) - total_converted)

    store_recommendations = []
    remaining_customers = customers_needed
    for priority_level in [1, 2, 3]:
        for store, priority in store_priorities.items():
            if int(priority) == priority_level:
                store_pool = non_converted_customers[non_converted_customers["Store"] == store]
                store_count = min(len(store_pool), remaining_customers)
                if store_count > 0:
                    forecasted_value = int(store_pool["Last_Order_Value"].fillna(0).mean() * 1.1)
                    store_recommendations.append({
                        "Store": store,
                        "Target_Customers_Next_Round": store_count,
                        "Recommended_Promo": "15%" if forecasted_value < 1000 else "10%",
                        "Forecasted_Basket_Value": forecasted_value
                    })
                    remaining_customers -= store_count
                if remaining_customers <= 0:
                    break
        if remaining_customers <= 0:
            break

    if store_recommendations:
        st.markdown(f"**🎯 To hit a 25% churn recovery, target ~{customers_needed} customers in the next round.**")
        rec_df = pd.DataFrame(store_recommendations)
        st.dataframe(rec_df)

        st.download_button("Download Next Round Target List", data=convert_df_to_excel(rec_df),
                           file_name=f"next_round_targets_{campaign_name}.xlsx")
    else:
        st.info("No available customers left to meet 25% churn recovery goal based on current data.")
