{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyP8+fv71Q36Qq2CrtrZQh4M",
      "include_colab_link": True
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/elhaithamy/crm-targeting-tool/blob/main/CRM_Targeted_Campaigns.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 1,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "77W9pw-ZksN1",
        "outputId": "d56ea968-6439-49dc-8624-8ff3945ee653"
      },
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Collecting streamlit\n",
            "  Downloading streamlit-1.48.0-py3-none-any.whl.metadata (9.5 kB)\n",
            "Requirement already satisfied: pandas in /usr/local/lib/python3.11/dist-packages (2.2.2)\n",
            "Requirement already satisfied: openpyxl in /usr/local/lib/python3.11/dist-packages (3.1.5)\n",
            "Requirement already satisfied: matplotlib in /usr/local/lib/python3.11/dist-packages (3.10.0)\n",
            "Requirement already satisfied: plotly in /usr/local/lib/python3.11/dist-packages (5.24.1)\n",
            "Requirement already satisfied: altair!=5.4.0,!=5.4.1,<6,>=4.0 in /usr/local/lib/python3.11/dist-packages (from streamlit) (5.5.0)\n",
            "Requirement already satisfied: blinker<2,>=1.5.0 in /usr/local/lib/python3.11/dist-packages (from streamlit) (1.9.0)\n",
            "Requirement already satisfied: cachetools<7,>=4.0 in /usr/local/lib/python3.11/dist-packages (from streamlit) (5.5.2)\n",
            "Requirement already satisfied: click<9,>=7.0 in /usr/local/lib/python3.11/dist-packages (from streamlit) (8.2.1)\n",
            "Requirement already satisfied: numpy<3,>=1.23 in /usr/local/lib/python3.11/dist-packages (from streamlit) (2.0.2)\n",
            "Requirement already satisfied: packaging<26,>=20 in /usr/local/lib/python3.11/dist-packages (from streamlit) (25.0)\n",
            "Requirement already satisfied: pillow<12,>=7.1.0 in /usr/local/lib/python3.11/dist-packages (from streamlit) (11.3.0)\n",
            "Requirement already satisfied: protobuf<7,>=3.20 in /usr/local/lib/python3.11/dist-packages (from streamlit) (5.29.5)\n",
            "Requirement already satisfied: pyarrow>=7.0 in /usr/local/lib/python3.11/dist-packages (from streamlit) (18.1.0)\n",
            "Requirement already satisfied: requests<3,>=2.27 in /usr/local/lib/python3.11/dist-packages (from streamlit) (2.32.3)\n",
            "Requirement already satisfied: tenacity<10,>=8.1.0 in /usr/local/lib/python3.11/dist-packages (from streamlit) (8.5.0)\n",
            "Requirement already satisfied: toml<2,>=0.10.1 in /usr/local/lib/python3.11/dist-packages (from streamlit) (0.10.2)\n",
            "Requirement already satisfied: typing-extensions<5,>=4.4.0 in /usr/local/lib/python3.11/dist-packages (from streamlit) (4.14.1)\n",
            "Collecting watchdog<7,>=2.1.5 (from streamlit)\n",
            "  Downloading watchdog-6.0.0-py3-none-manylinux2014_x86_64.whl.metadata (44 kB)\n",
            "\u001b[2K     \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m44.3/44.3 kB\u001b[0m \u001b[31m2.6 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[?25hRequirement already satisfied: gitpython!=3.1.19,<4,>=3.0.7 in /usr/local/lib/python3.11/dist-packages (from streamlit) (3.1.45)\n",
            "Collecting pydeck<1,>=0.8.0b4 (from streamlit)\n",
            "  Downloading pydeck-0.9.1-py2.py3-none-any.whl.metadata (4.1 kB)\n",
            "Requirement already satisfied: tornado!=6.5.0,<7,>=6.0.3 in /usr/local/lib/python3.11/dist-packages (from streamlit) (6.4.2)\n",
            "Requirement already satisfied: python-dateutil>=2.8.2 in /usr/local/lib/python3.11/dist-packages (from pandas) (2.9.0.post0)\n",
            "Requirement already satisfied: pytz>=2020.1 in /usr/local/lib/python3.11/dist-packages (from pandas) (2025.2)\n",
            "Requirement already satisfied: tzdata>=2022.7 in /usr/local/lib/python3.11/dist-packages (from pandas) (2025.2)\n",
            "Requirement already satisfied: et-xmlfile in /usr/local/lib/python3.11/dist-packages (from openpyxl) (2.0.0)\n",
            "Requirement already satisfied: contourpy>=1.0.1 in /usr/local/lib/python3.11/dist-packages (from matplotlib) (1.3.3)\n",
            "Requirement already satisfied: cycler>=0.10 in /usr/local/lib/python3.11/dist-packages (from matplotlib) (0.12.1)\n",
            "Requirement already satisfied: fonttools>=4.22.0 in /usr/local/lib/python3.11/dist-packages (from matplotlib) (4.59.0)\n",
            "Requirement already satisfied: kiwisolver>=1.3.1 in /usr/local/lib/python3.11/dist-packages (from matplotlib) (1.4.8)\n",
            "Requirement already satisfied: pyparsing>=2.3.1 in /usr/local/lib/python3.11/dist-packages (from matplotlib) (3.2.3)\n",
            "Requirement already satisfied: jinja2 in /usr/local/lib/python3.11/dist-packages (from altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit) (3.1.6)\n",
            "Requirement already satisfied: jsonschema>=3.0 in /usr/local/lib/python3.11/dist-packages (from altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit) (4.25.0)\n",
            "Requirement already satisfied: narwhals>=1.14.2 in /usr/local/lib/python3.11/dist-packages (from altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit) (2.0.1)\n",
            "Requirement already satisfied: gitdb<5,>=4.0.1 in /usr/local/lib/python3.11/dist-packages (from gitpython!=3.1.19,<4,>=3.0.7->streamlit) (4.0.12)\n",
            "Requirement already satisfied: six>=1.5 in /usr/local/lib/python3.11/dist-packages (from python-dateutil>=2.8.2->pandas) (1.17.0)\n",
            "Requirement already satisfied: charset-normalizer<4,>=2 in /usr/local/lib/python3.11/dist-packages (from requests<3,>=2.27->streamlit) (3.4.2)\n",
            "Requirement already satisfied: idna<4,>=2.5 in /usr/local/lib/python3.11/dist-packages (from requests<3,>=2.27->streamlit) (3.10)\n",
            "Requirement already satisfied: urllib3<3,>=1.21.1 in /usr/local/lib/python3.11/dist-packages (from requests<3,>=2.27->streamlit) (2.5.0)\n",
            "Requirement already satisfied: certifi>=2017.4.17 in /usr/local/lib/python3.11/dist-packages (from requests<3,>=2.27->streamlit) (2025.7.14)\n",
            "Requirement already satisfied: smmap<6,>=3.0.1 in /usr/local/lib/python3.11/dist-packages (from gitdb<5,>=4.0.1->gitpython!=3.1.19,<4,>=3.0.7->streamlit) (5.0.2)\n",
            "Requirement already satisfied: MarkupSafe>=2.0 in /usr/local/lib/python3.11/dist-packages (from jinja2->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit) (3.0.2)\n",
            "Requirement already satisfied: attrs>=22.2.0 in /usr/local/lib/python3.11/dist-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit) (25.3.0)\n",
            "Requirement already satisfied: jsonschema-specifications>=2023.03.6 in /usr/local/lib/python3.11/dist-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit) (2025.4.1)\n",
            "Requirement already satisfied: referencing>=0.28.4 in /usr/local/lib/python3.11/dist-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit) (0.36.2)\n",
            "Requirement already satisfied: rpds-py>=0.7.1 in /usr/local/lib/python3.11/dist-packages (from jsonschema>=3.0->altair!=5.4.0,!=5.4.1,<6,>=4.0->streamlit) (0.26.0)\n",
            "Downloading streamlit-1.48.0-py3-none-any.whl (9.9 MB)\n",
            "\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m9.9/9.9 MB\u001b[0m \u001b[31m79.0 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[?25hDownloading pydeck-0.9.1-py2.py3-none-any.whl (6.9 MB)\n",
            "\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m6.9/6.9 MB\u001b[0m \u001b[31m98.3 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[?25hDownloading watchdog-6.0.0-py3-none-manylinux2014_x86_64.whl (79 kB)\n",
            "\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m79.1/79.1 kB\u001b[0m \u001b[31m7.0 MB/s\u001b[0m eta \u001b[36m0:00:00\u001b[0m\n",
            "\u001b[?25hInstalling collected packages: watchdog, pydeck, streamlit\n",
            "Successfully installed pydeck-0.9.1 streamlit-1.48.0 watchdog-6.0.0\n"
          ]
        }
      ],
      "source": [
        "pip install streamlit pandas openpyxl matplotlib plotly\n"
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "# app.py\n",
        "import streamlit as st\n",
        "import pandas as pd\n",
        "import plotly.express as px\n",
        "from datetime import datetime\n",
        "\n",
        "st.set_page_config(page_title=\"Churn Recovery Dashboard\", layout=\"wide\")\n",
        "\n",
        "st.title(\"📉 Churn Recovery Campaign Manager\")\n",
        "\n",
        "# Sidebar for file upload\n",
        "st.sidebar.header(\"Upload CRM or Campaign Data\")\n",
        "uploaded_file = st.sidebar.file_uploader(\"Upload Excel\", type=[\"xlsx\", \"csv\"])\n",
        "\n",
        "# Step 1: Data Upload\n",
        "if uploaded_file:\n",
        "    df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith(\".xlsx\") else pd.read_csv(uploaded_file)\n",
        "    st.success(\"Data Uploaded Successfully ✅\")\n",
        "\n",
        "    # Step 2: Show Data\n",
        "    st.subheader(\"Uploaded Data Preview\")\n",
        "    st.dataframe(df.head())\n",
        "\n",
        "    # Step 3: Segment Logic\n",
        "    if \"Basket Value\" in df.columns:\n",
        "        def assign_segment(value):\n",
        "            if value >= 1500:\n",
        "                return \"A\"\n",
        "            elif value >= 1000:\n",
        "                return \"B\"\n",
        "            elif value >= 500:\n",
        "                return \"C\"\n",
        "            else:\n",
        "                return \"D\"\n",
        "        df[\"Segment\"] = df[\"Basket Value\"].apply(assign_segment)\n",
        "        st.dataframe(df[[\"Customer ID\", \"Basket Value\", \"Segment\"]])\n",
        "\n",
        "    # Step 4: Campaign Planner\n",
        "    st.subheader(\"📢 Campaign Planner\")\n",
        "    selected_segment = st.selectbox(\"Choose Segment\", options=[\"A\", \"B\", \"C\", \"D\"])\n",
        "    selected_channel = st.selectbox(\"Choose Channel\", options=[\"SMS\", \"WhatsApp\", \"Call\"])\n",
        "    offer_value = st.number_input(\"Enter Offer Value (EGP)\", value=100)\n",
        "\n",
        "    if st.button(\"Generate Target List\"):\n",
        "        filtered_df = df[df[\"Segment\"] == selected_segment]\n",
        "        st.success(f\"{len(filtered_df)} Customers in Segment {selected_segment}\")\n",
        "        st.download_button(\"📤 Download Target List\", data=filtered_df.to_csv(index=False), file_name=\"target_list.csv\")\n",
        "\n",
        "    # Step 5: Performance Tracker\n",
        "    if \"Conversion Rate\" in df.columns:\n",
        "        st.subheader(\"📊 Campaign Performance\")\n",
        "        fig = px.line(df, x=\"Campaign Date\", y=\"Conversion Rate\", color=\"Segment\", markers=True)\n",
        "        st.plotly_chart(fig, use_container_width=True)\n",
        "\n",
        "    # Step 6: Goal Tracker\n",
        "    st.subheader(\"🎯 Recovery Goal Tracker\")\n",
        "    recovered = df[\"Retained Customers\"].sum() if \"Retained Customers\" in df.columns else 0\n",
        "    approached = df[\"Approached Customers\"].sum() if \"Approached Customers\" in df.columns else 1\n",
        "    recovery_rate = recovered / approached * 100\n",
        "    st.metric(label=\"Current Recovery Rate\", value=f\"{recovery_rate:.2f}%\", delta=f\"{recovery_rate - 25:.2f}% from Goal\")\n",
        "\n",
        "else:\n",
        "    st.warning(\"👈 Upload a CRM or campaign Excel to begin.\")\n",
        "\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "B_sc4IlkopQj",
        "outputId": "d52dc75b-dbe2-452a-e71f-fb083efc6d2c"
      },
      "execution_count": 2,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stderr",
          "text": [
            "2025-08-07 13:05:30.530 WARNING streamlit.runtime.scriptrunner_utils.script_run_context: Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-08-07 13:05:30.537 WARNING streamlit.runtime.scriptrunner_utils.script_run_context: Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-08-07 13:05:30.992 \n",
            "  \u001b[33m\u001b[1mWarning:\u001b[0m to view this Streamlit app on a browser, run it with the following\n",
            "  command:\n",
            "\n",
            "    streamlit run /usr/local/lib/python3.11/dist-packages/colab_kernel_launcher.py [ARGUMENTS]\n",
            "2025-08-07 13:05:30.995 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-08-07 13:05:31.003 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-08-07 13:05:31.004 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-08-07 13:05:31.008 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-08-07 13:05:31.011 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-08-07 13:05:31.013 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-08-07 13:05:31.013 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-08-07 13:05:31.018 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-08-07 13:05:31.023 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-08-07 13:05:31.027 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-08-07 13:05:31.037 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-08-07 13:05:31.050 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-08-07 13:05:31.054 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n",
            "2025-08-07 13:05:31.055 Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode.\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [],
      "metadata": {
        "id": "nkEJ70uQp1Fc"
      },
      "execution_count": null,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "id": "e4f95c08"
      },
      "source": [
        "# Create the project directory and subdirectories\n",
        "!mkdir -p project/data"
      ],
      "execution_count": 3,
      "outputs": []
    },
    {
      "cell_type": "code",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "a6bbafbf",
        "outputId": "74b6aef9-6ac1-4276-ec93-dbdd9505bcdb"
      },
      "source": [
        "%%writefile project/app.py\n",
        "# app.py\n",
        "import streamlit as st\n",
        "import pandas as pd\n",
        "import plotly.express as px\n",
        "from datetime import datetime\n",
        "import os\n",
        "\n",
        "st.set_page_config(page_title=\"Churn Recovery Dashboard\", layout=\"wide\")\n",
        "\n",
        "st.title(\"📉 Churn Recovery Campaign Manager\")\n",
        "\n",
        "# Sidebar for file upload\n",
        "st.sidebar.header(\"Upload CRM or Campaign Data\")\n",
        "uploaded_file = st.sidebar.file_uploader(\"Upload Excel or CSV\", type=[\"xlsx\", \"csv\"])\n",
        "\n",
        "df = None\n",
        "# Load default data if no file is uploaded\n",
        "if uploaded_file is None and os.path.exists(\"project/data/CRM_SMS_Channel.xlsx\"):\n",
        "    try:\n",
        "        df = pd.read_excel(\"project/data/CRM_SMS_Channel.xlsx\")\n",
        "        st.info(\"Loaded default data: CRM_SMS_Channel.xlsx\")\n",
        "    except Exception as e:\n",
        "        st.error(f\"Error loading default Excel file: {e}\")\n",
        "elif uploaded_file:\n",
        "    try:\n",
        "        df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith(\".xlsx\") else pd.read_csv(uploaded_file)\n",
        "        st.success(\"Data Uploaded Successfully ✅\")\n",
        "    except Exception as e:\n",
        "        st.error(f\"Error loading uploaded file: {e}\")\n",
        "\n",
        "\n",
        "if df is not None:\n",
        "    # Step 2: Show Data\n",
        "    st.subheader(\"Uploaded Data Preview\")\n",
        "    st.dataframe(df.head())\n",
        "\n",
        "    # Step 3: Segment Logic\n",
        "    if \"Basket Value\" in df.columns:\n",
        "        st.subheader(\"Segmentation Logic (based on Basket Value)\")\n",
        "        def assign_segment(value):\n",
        "            if pd.isna(value):\n",
        "                return \"Unknown\"\n",
        "            elif value >= 1500:\n",
        "                return \"A\"\n",
        "            elif value >= 1000:\n",
        "                return \"B\"\n",
        "            elif value >= 500:\n",
        "                return \"C\"\n",
        "            else:\n",
        "                return \"D\"\n",
        "        df[\"Segment\"] = df[\"Basket Value\"].apply(assign_segment)\n",
        "        st.dataframe(df[[\"Customer ID\", \"Basket Value\", \"Segment\"]].head())\n",
        "    else:\n",
        "        st.warning(\" 'Basket Value' column not found for segmentation.\")\n",
        "\n",
        "\n",
        "    # Step 4: Campaign Planner\n",
        "    st.subheader(\"📢 Campaign Planner\")\n",
        "\n",
        "    if \"Segment\" in df.columns:\n",
        "        selected_segment = st.selectbox(\"Choose Segment\", options=df[\"Segment\"].unique().tolist())\n",
        "        selected_channel = st.selectbox(\"Choose Channel\", options=[\"SMS\", \"WhatsApp\", \"Call\", \"Email\"]) # Added Email\n",
        "        offer_value = st.number_input(\"Enter Offer Value (EGP)\", value=100)\n",
        "\n",
        "        if st.button(\"Generate Target List\"):\n",
        "            filtered_df = df[df[\"Segment\"] == selected_segment].copy() # Added .copy() to avoid SettingWithCopyWarning\n",
        "            if not filtered_df.empty:\n",
        "                st.success(f\"{len(filtered_df)} Customers in Segment {selected_segment}\")\n",
        "                st.dataframe(filtered_df) # Display the filtered list\n",
        "                st.download_button(\"📤 Download Target List\", data=filtered_df.to_csv(index=False), file_name=f\"target_list_{selected_segment}_{selected_channel}.csv\")\n",
        "            else:\n",
        "                st.info(f\"No customers found in Segment {selected_segment}\")\n",
        "    else:\n",
        "        st.warning(\"Segmentation not available. Cannot use Campaign Planner.\")\n",
        "\n",
        "\n",
        "    # Step 5: Performance Tracker - Expanded based on goal description\n",
        "    st.subheader(\"📊 Campaign Performance Tracker\")\n",
        "\n",
        "    # Placeholder for performance metrics (ROI, AOV, Redemption, etc.)\n",
        "    # This part requires specific columns in the uploaded data, which are not guaranteed.\n",
        "    # Assuming columns like 'Campaign Date', 'Campaign Name', 'Segment', 'Revenue', 'Cost', 'Redemptions', 'Orders'\n",
        "\n",
        "    if all(col in df.columns for col in [\"Campaign Date\", \"Campaign Name\", \"Segment\", \"Revenue\", \"Cost\", \"Redemptions\", \"Orders\"]):\n",
        "        # Example: Calculate ROI\n",
        "        df['ROI'] = ((df['Revenue'] - df['Cost']) / df['Cost']).fillna(0) * 100\n",
        "\n",
        "        # Example: Calculate AOV (Average Order Value)\n",
        "        df['AOV'] = (df['Revenue'] / df['Orders']).fillna(0)\n",
        "\n",
        "        # Example: Calculate Redemption Rate\n",
        "        df['Redemption Rate'] = (df['Redemptions'] / df['Approached Customers']).fillna(0) * 100 if 'Approached Customers' in df.columns else 0\n",
        "\n",
        "        st.dataframe(df[['Campaign Date', 'Campaign Name', 'Segment', 'Revenue', 'Cost', 'ROI', 'AOV', 'Redemption Rate']].head())\n",
        "\n",
        "        # Example: Plot ROI by Campaign and Segment\n",
        "        fig_roi = px.bar(df, x='Campaign Name', y='ROI', color='Segment', barmode='group', title='ROI by Campaign and Segment')\n",
        "        st.plotly_chart(fig_roi, use_container_width=True)\n",
        "\n",
        "        # Example: Plot AOV by Campaign and Segment\n",
        "        fig_aov = px.bar(df, x='Campaign Name', y='AOV', color='Segment', barmode='group', title='AOV by Campaign and Segment')\n",
        "        st.plotly_chart(fig_aov, use_container_width=True)\n",
        "\n",
        "    else:\n",
        "        st.info(\"Performance tracking columns (Campaign Date, Campaign Name, Segment, Revenue, Cost, Redemptions, Orders) not found in the uploaded data. Cannot display performance metrics.\")\n",
        "\n",
        "\n",
        "    # Step 6: Goal Tracker\n",
        "    st.subheader(\"🎯 Recovery Goal Tracker\")\n",
        "\n",
        "    # Assuming 'Retained Customers' and 'Approached Customers' columns exist for this\n",
        "    if \"Retained Customers\" in df.columns and \"Approached Customers\" in df.columns:\n",
        "        recovered = df[\"Retained Customers\"].sum()\n",
        "        approached = df[\"Approached Customers\"].sum()\n",
        "        recovery_rate = (recovered / approached * 100) if approached > 0 else 0\n",
        "\n",
        "        goal_rate = 25 # Define the recovery goal\n",
        "        delta_value = recovery_rate - goal_rate\n",
        "\n",
        "        st.metric(label=\"Current Recovery Rate\", value=f\"{recovery_rate:.2f}%\", delta=f\"{delta_value:.2f}% from Goal\")\n",
        "    else:\n",
        "        st.warning(\" 'Retained Customers' or 'Approached Customers' columns not found for Goal Tracker.\")\n",
        "\n",
        "else:\n",
        "    st.warning(\"👈 Upload a CRM or campaign Excel/CSV to begin, or place a file named 'CRM_SMS_Channel.xlsx' in the 'project/data' folder.\")"
      ],
      "execution_count": 4,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Writing project/app.py\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "e99af905",
        "outputId": "3f26b644-f1ea-4fbd-e416-2e9e02051025"
      },
      "source": [
        "%%writefile project/requirements.txt\n",
        "streamlit\n",
        "pandas\n",
        "openpyxl\n",
        "matplotlib\n",
        "plotly"
      ],
      "execution_count": 5,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Writing project/requirements.txt\n"
          ]
        }
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "c8a8a0d1"
      },
      "source": [
        "I have created the `project` folder and the `app.py` and `requirements.txt` files within it. I have also made the following updates to the `app.py` code based on your goals:\n",
        "\n",
        "- Added handling for both `.xlsx` and `.csv` file uploads.\n",
        "- Added an option to load a default file named `CRM_SMS_Channel.xlsx` from the `project/data` folder if no file is uploaded.\n",
        "- Improved the segmentation logic to handle potential missing values in the \"Basket Value\" column.\n",
        "- Added 'Email' as an option in the Campaign Planner channel selection.\n",
        "- Added `.copy()` when filtering the DataFrame in the Campaign Planner to avoid potential `SettingWithCopyWarning`.\n",
        "- Expanded the Performance Tracker section to include calculations and visualizations for ROI, AOV, and Redemption Rate, assuming the presence of relevant columns in the data.\n",
        "- Added checks in the Performance Tracker and Goal Tracker to inform the user if the necessary columns are missing in the uploaded data.\n",
        "\n",
        "You can now run the Streamlit application from the `project` directory."
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "streamlit run app.py\n"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 106
        },
        "id": "7vSKcTMtp46f",
        "outputId": "a60b0843-056e-4877-ede2-5afa38227799"
      },
      "execution_count": 6,
      "outputs": [
        {
          "output_type": "error",
          "ename": "SyntaxError",
          "evalue": "invalid syntax (ipython-input-507122745.py, line 1)",
          "traceback": [
            "\u001b[0;36m  File \u001b[0;32m\"/tmp/ipython-input-507122745.py\"\u001b[0;36m, line \u001b[0;32m1\u001b[0m\n\u001b[0;31m    streamlit run app.py\u001b[0m\n\u001b[0m              ^\u001b[0m\n\u001b[0;31mSyntaxError\u001b[0m\u001b[0;31m:\u001b[0m invalid syntax\n"
          ]
        }
      ]
    },
    {
      "cell_type": "code",
      "source": [
        "!streamlit run app.py"
      ],
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/"
        },
        "id": "nyOzeeuNrsvc",
        "outputId": "b410e9af-421f-4023-fd2f-878b6a437396"
      },
      "execution_count": 7,
      "outputs": [
        {
          "output_type": "stream",
          "name": "stdout",
          "text": [
            "Usage: streamlit run [OPTIONS] TARGET [ARGS]...\n",
            "Try 'streamlit run --help' for help.\n",
            "\n",
            "Error: Invalid value: File does not exist: app.py\n"
          ]
        }
      ]
    }
  ]
}
