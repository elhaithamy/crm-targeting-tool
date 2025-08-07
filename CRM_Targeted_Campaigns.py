import streamlit as st
import pandas as pd
import numpy as np
import io
import matplotlib.pyplot as plt

st.set_page_config(page_title="CRM Targeted Campaigns", layout="wide")

st.title("📊 CRM Targeted Campaigns Tool")

uploaded_file = st.file_uploader("Upload Campaign Excel File", type=["xlsx"])

campaign_name = st.text_input("Enter Campaign Name (required):")

if uploaded_file and campaign_name.strip():
    df = pd.read_excel(uploaded_file)

    # Convert dates
    df['Last_Order_Date'] = pd.to_datetime(df['Last_Order_Date'], errors='coerce')
    df['Campaign_Start_Date'] = pd.to_datetime(df['Campaign_Start_Date'], errors='coerce')
    df['Campaign_End_Date'] = pd.to_datetime(df['Campaign_End_Date'], errors='coerce')

    # Determine segment
    def assign_segment(value):
        if value >= 1500:
            return "Segment A"
        elif 1000 <= value < 1500:
            return "Segment B"
        elif 500 <= value < 1000:
            return "Segment C"
        else:
            return "Segment D"

    df["Segment"] = df["Last_Order_Value"].apply(assign_segment)

    # Flag conversions
    df["Converted"] = df["Last_Order_Date"] > df["Campaign_Start_Date"]

    # Targeted customers = all uploaded
    total_targeted = len(df)
    total_converted = df["Converted"].sum()
    total_used_promo = df["Used_Promo_Code"].str.lower().eq("yes").sum()

    st.subheader("📈 Campaign Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("🎯 Total Targeted", total_targeted)
    col2.metric("✅ Converted Customers", total_converted)
    col3.metric("🏷️ Used Promo Code", total_used_promo)

    # Summary chart
    summary_data = pd.DataFrame({
        "Status": ["Targeted", "Converted", "Used Promo"],
        "Count": [total_targeted, total_converted, total_used_promo]
    })

    fig, ax = plt.subplots()
    ax.bar(summary_data["Status"], summary_data["Count"])
    ax.set_ylabel("Number of Customers")
    ax.set_title("Campaign Conversion Funnel")
    st.pyplot(fig)

    # --- TARGETED CUSTOMERS ---
    df["Recommended_Target_Basket"] = df["Segment"].map({
        "Segment A": 1800,
        "Segment B": 1300,
        "Segment C": 800,
        "Segment D": 400
    })

    df["Campaign_Name"] = campaign_name

    target_df = df[df["Converted"]]
    non_converted_df = df[~df["Converted"]]

    st.subheader("✅ Converted Customers")
    st.dataframe(target_df[[
        "Customer_ID", "Store", "Segment", "Recommended_Target_Basket",
        "Campaign_Name", "Notes"
    ]])

    st.download_button(
        "⬇️ Export Converted Customers",
        data=target_df.to_excel(index=False, engine="openpyxl"),
        file_name=f"{campaign_name}_Converted_Customers.xlsx"
    )

    st.subheader("❌ Non-Converted Customers")
    st.dataframe(non_converted_df[[
        "Customer_ID", "Store", "Segment", "Recommended_Target_Basket",
        "Campaign_Name", "Notes"
    ]])

    st.download_button(
        "⬇️ Export Non-Converted Customers",
        data=non_converted_df.to_excel(index=False, engine="openpyxl"),
        file_name=f"{campaign_name}_Non_Converted_Customers.xlsx"
    )

    # --- RECOMMENDATIONS SECTION WITH PRIORITY INPUT ---
    st.subheader("🔍 Recommendations for Next Round")

    churn_target = 0.25  # 25% recovery goal

    # Step 1: Ask user to assign priority levels for each store
    st.markdown("### 🏪 Store Prioritization")
    store_list = sorted(non_converted_df["Store"].dropna().unique())
    store_priorities = {}

    for store in store_list:
        store_priorities[store] = st.selectbox(
            f"Set priority for store: {store}",
            options=[1, 2, 3],
            index=0,
            key=f"priority_{store}"
        )

    # Step 2: Assign promo values by segment
    promo_values = {
        "Segment A": 200,
        "Segment B": 150,
        "Segment C": 100,
        "Segment D": 75
    }

    # Step 3: Calculate required conversions
    required_recovery_count = int(np.ceil(total_targeted * churn_target))
    gap = required_recovery_count - total_converted
    st.markdown(f"📉 To hit **25% churn recovery**, you need **{required_recovery_count}** total conversions.")
    st.markdown(f"📌 You still need **{gap} more conversions** from non-converted customers.")

    # Step 4: Suggest customers from prioritized stores
    non_converted_df["Priority"] = non_converted_df["Store"].map(store_priorities)
    prioritized_df = non_converted_df.sort_values(by=["Priority", "Segment"])

    # Add promo and forecasted basket
    prioritized_df["Recommended_Promo"] = prioritized_df["Segment"].map(promo_values)
    prioritized_df["Forecasted_Basket_Value"] = prioritized_df["Recommended_Target_Basket"] + prioritized_df["Recommended_Promo"]

    # Select top N to close the gap
    next_round_df = prioritized_df.head(gap)

    st.markdown("### 🎯 Recommended Customers for Next Round")
    st.dataframe(next_round_df[[
        "Customer_ID", "Store", "Segment", "Priority", "Recommended_Target_Basket",
        "Recommended_Promo", "Forecasted_Basket_Value", "Notes"
    ]])

    st.download_button(
        "⬇️ Download Next Round Target List",
        data=next_round_df.to_excel(index=False, engine="openpyxl"),
        file_name=f"{campaign_name}_Next_Round_Targets.xlsx"
    )
else:
    if uploaded_file and not campaign_name.strip():
        st.warning("⚠️ Please enter a campaign name before proceeding.")
