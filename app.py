
import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime
import matplotlib.pyplot as plt
from PIL import Image

st.set_page_config(page_title="GCC HR Reporting | SRKay", layout="wide", page_icon="🧾")

# Branding: Logo
col1, col2 = st.columns([1, 9])
with col1:
    logo = Image.open("SRKay logo.png")
    st.image(logo, width=100)
with col2:
    st.title("SRKay | GCC HR Reporting Dashboard")

# Section 1: Executive Summary
st.header("1. Executive Summary")
report_period = st.text_input("Report Period (e.g., Q2 2025)", "Q2 2025")
reporting_date = st.date_input("Reporting Date", value=datetime.today())
total_headcount = st.number_input("Total Headcount", min_value=0, value=158)
total_attrition = st.text_input("Total Attrition Rate (YTD)", "8.2")
key_highlights = st.text_area("Key Highlights (one per line)",
    '''Highest hiring in Data Engineering vertical (32 new hires)
Reduction in voluntary attrition by 2.1% QoQ
Employee engagement score increased to 79%
Average tenure improved from 2.1 to 2.6 years
80% of exit interviews completed within 5 days
Launched Manager Development Bootcamp across all functions''')

# Section 2: Skill Mix
st.header("2. Skill Mix")
skill_mix = {"Data Engineering": 32, "Data Science": 22, "DevOps": 18, "Cybersecurity": 12, "Product Mgmt": 10, "Others": 18}
skill_labels = list(skill_mix.keys())
skill_sizes = list(skill_mix.values())
fig1, ax1 = plt.subplots()
ax1.pie(skill_sizes, labels=skill_labels, autopct='%1.1f%%', startangle=90)
ax1.axis('equal')
st.pyplot(fig1)

# Section 3: Role Mix
st.header("3. Role Mix")
role_mix = {"ICs": 94, "Team Leads": 30, "Mid Managers": 18, "Leadership": 10, "Support": 6}
role_df = pd.DataFrame(list(role_mix.items()), columns=["Role", "Count"])
st.bar_chart(role_df.set_index("Role"))

# Section 4: Tenure Distribution
st.header("4. Tenure Distribution")
tenure = {"<1 yr": 40, "1-3 yrs": 56, "3-5 yrs": 35, ">5 yrs": 27}
tenure_df = pd.DataFrame(list(tenure.items()), columns=["Tenure", "Count"])
st.bar_chart(tenure_df.set_index("Tenure"))

# Section 5: Engagement Trend
st.header("5. Engagement Trend (Last 4 Quarters)")
quarters = ["Q3'24", "Q4'24", "Q1'25", "Q2'25"]
engagement_scores = [71, 75, 77, 79]
fig2, ax2 = plt.subplots()
ax2.plot(quarters, engagement_scores, marker='o')
ax2.set_ylabel("Engagement %")
ax2.set_title("Employee Engagement Index")
st.pyplot(fig2)

# Export to Excel
if st.button("📤 Generate Excel Report"):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')

    summary_df = pd.DataFrame({
        "Field": ["Report Period", "Reporting Date", "Total Headcount", "Attrition Rate (YTD)", "Key Highlights"],
        "Value": [report_period, reporting_date.strftime("%d-%m-%Y"), total_headcount, total_attrition, key_highlights.replace("\n", "; ")]
    })
    summary_df.to_excel(writer, index=False, sheet_name='Executive Summary')

    skill_df = pd.DataFrame(skill_mix.items(), columns=["Skill Domain", "Headcount"])
    skill_df.to_excel(writer, index=False, sheet_name='Skill Mix')

    role_df.to_excel(writer, index=False, sheet_name='Role Mix')
    tenure_df.to_excel(writer, index=False, sheet_name='Tenure Distribution')
    pd.DataFrame({"Quarter": quarters, "Engagement Score": engagement_scores}).to_excel(writer, index=False, sheet_name='Engagement Trend')

    writer.close()
    st.download_button(
        label="📥 Download HR Report Excel",
        data=output.getvalue(),
        file_name=f"GCC_HR_Report_{datetime.today().strftime('%Y%m%d')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
