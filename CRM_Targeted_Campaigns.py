import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

st.set_page_config(page_title="CRM Retention Dashboard", layout="wide")

st.title("🎯 CRM Campaign Targeting Dashboard")
st.markdown("Target: Reduce churn rate to **25%** by end of 2025.")

uploaded_file = st.file_uploader("📤 Upload Churn Campaign Excel File", type=["xlsx"])

if uploaded_file:
    try:
        xls = pd.ExcelFile(uploaded_file)

        # Show available sheets
        st.sidebar.header("Sheet Selection")
        sheet_names = xls.sheet_names
        selected_sheet = st.sidebar.selectbox("Choose sheet to analyze:", sheet_names)

        df = pd.read_excel(xls, selected_sheet)

        st.subheader(f"📊 Data Preview — {selected_sheet}")
        st.dataframe(df)

        # Detect churn column candidates
        numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
        churn_cols = [col for col in numeric_columns if 'churn' in col.lower() or 'rate' in col.lower()]

        if churn_cols:
            churn_col = st.selectbox("Select churn-related metric to visualize:", churn_cols)

            # KPI card
            current_rate = df[churn_col].mean()
            delta = round(current_rate - 25, 2)
            st.metric(label="📉 Average Churn Rate", value=f"{current_rate:.2f}%", delta=f"{delta:+.2f}%")

            # Plot
            fig, ax = plt.subplots()
            df[churn_col].plot(kind="hist", bins=15, ax=ax)
            ax.set_title("Churn Rate Distribution")
            ax.set_xlabel("Churn Rate (%)")
            st.pyplot(fig)
        else:
            st.warning("⚠️ No churn-related columns detected. Please check your Excel sheet.")

        # Optional: Download cleaned version
        with BytesIO() as b_io:
            df.to_excel(b_io, index=False)
            st.download_button("📥 Download Cleaned Data", b_io.getvalue(), file_name="cleaned_campaign_data.xlsx")

    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
else:
    st.info("Upload your Excel campaign file to begin.")
