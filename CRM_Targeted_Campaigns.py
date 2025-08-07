import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("📊 CRM Targeted Campaigns Dashboard")

# --- Upload file ---
uploaded_file = st.file_uploader("Upload customer data Excel file", type=["xlsx"])
campaign_name = st.text_input("Enter Campaign Name (required before analysis)")

if uploaded_file and campaign_name:
    df = pd.read_excel(uploaded_file)

    # --- Data Cleaning ---
    df.columns = df.columns.str.strip()
    df["Campaign_Name"] = campaign_name
    df["Last_Order_Date"] = pd.to_datetime(df["Last_Order_Date"], errors='coerce')
    df["Campaign_Date"] = pd.to_datetime(df["Campaign_Date"], errors='coerce')
    df["Days_Since_Last_Order"] = (df["Campaign_Date"] - df["Last_Order_Date"]).dt.days

    # --- Define conversion ---
    df["Is_Converted"] = df["Days_Since_Last_Order"] <= 7
    if "Used_Promo_Code" in df.columns:
        df["Used_Promo_Code"] = df["Used_Promo_Code"].astype(str)
        df["Used_Promo_Code"] = df["Used_Promo_Code"].str.lower().eq("yes")
    else:
        df["Used_Promo_Code"] = False

    st.subheader("📈 Campaign Summary")
    total_targeted = len(df)
    total_converted = df["Is_Converted"].sum()
    total_used_promo = df["Used_Promo_Code"].sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Targeted Customers", total_targeted)
    col2.metric("Converted Customers", total_converted)
    col3.metric("Used Promo Code", total_used_promo)

    # --- Chart ---
    summary_data = pd.DataFrame({
        'Status': ['Targeted', 'Converted', 'Used Promo'],
        'Count': [total_targeted, total_converted, total_used_promo]
    })

    fig, ax = plt.subplots()
    ax.bar(summary_data['Status'], summary_data['Count'])
    ax.set_ylabel("Number of Customers")
    ax.set_title("Campaign Performance Overview")
    st.pyplot(fig)

    # --- Segment-based breakdown ---
    st.subheader("📍 Segment Performance")
    segment_summary = df.groupby("Segment")["Is_Converted"].mean().reset_index()
    segment_summary.columns = ["Segment", "Conversion Rate"]
    st.dataframe(segment_summary)

    # --- Export buttons ---
    targeted_df = df[df["Is_Converted"]]
    non_converted_df = df[~df["Is_Converted"]]

    st.download_button("⬇️ Download Converted Customers", data=targeted_df.to_excel(index=False), file_name="converted_customers.xlsx")
    st.download_button("⬇️ Download Non-Converted Customers", data=non_converted_df.to_excel(index=False), file_name="non_converted_customers.xlsx")

    # --- Store Priority Input ---
    st.subheader("🏪 Store Priorities for Next Round")
    unique_stores = df["Store"].dropna().unique()
    store_priorities = {}
    for store in unique_stores:
        priority = st.selectbox(f"Set priority for {store}", options=[1, 2, 3], key=store)
        store_priorities[store] = priority

    # --- Smart Recommendation Section ---
    st.subheader("🔮 Next Step Recommendations")
    churn_target = 0.25  # 25% recovery goal
    expected_recoveries = int(total_targeted * churn_target)
    st.write(f"🎯 To reach 25% churn recovery, you need to convert at least **{expected_recoveries}** customers.")

    non_converted_df["Priority"] = non_converted_df["Store"].map(store_priorities)

    # Suggest customers from high-priority stores
    prioritized_customers = non_converted_df.sort_values(by=["Priority", "Last_Order_Value"], ascending=[True, False])
    prioritized_customers = prioritized_customers.head(expected_recoveries)

    # Estimate recommended promo value
    def recommend_promo(row):
        if row["Segment"] == "Segment A":
            return 100
        elif row["Segment"] == "Segment B":
            return 75
        elif row["Segment"] == "Segment C":
            return 50
        else:
            return 25

    prioritized_customers["Recommended_Promo"] = prioritized_customers.apply(recommend_promo, axis=1)
    prioritized_customers["Forecasted_Basket"] = prioritized_customers["Last_Order_Value"] + prioritized_customers["Recommended_Promo"]

    st.write("✅ Recommended Customers for Next Round")
    st.dataframe(prioritized_customers[[
        "Customer_ID", "Store", "Segment", "Last_Order_Value", "Recommended_Promo", "Forecasted_Basket"
    ]])

    st.download_button("⬇️ Download Next Round Customer List", data=prioritized_customers.to_excel(index=False), file_name="next_round_customers.xlsx")

else:
    st.warning("📥 Please upload a file and enter a campaign name to continue.")
