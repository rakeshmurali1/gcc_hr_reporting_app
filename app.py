
import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime

st.title("🧾 GCC HR Reporting Application")

# Section 1: Executive Summary
st.header("1. Executive Summary")
report_period = st.text_input("Report Period (e.g., Q2 2025)")
reporting_date = st.date_input("Reporting Date", value=datetime.today())
total_headcount = st.number_input("Total Headcount", min_value=0)
total_attrition = st.text_input("Total Attrition Rate (YTD)")
key_highlights = st.text_area("Key Highlights (one per line)")

# Export to Excel
if st.button("📤 Generate Excel Report"):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')

    summary_df = pd.DataFrame({
        "Field": ["Report Period", "Reporting Date", "Total Headcount", "Attrition Rate (YTD)", "Key Highlights"],
        "Value": [report_period, reporting_date.strftime("%d-%m-%Y"), total_headcount, total_attrition, key_highlights.replace("\n", "; ")]
    })
    summary_df.to_excel(writer, index=False, sheet_name='Executive Summary')

    writer.close()
    st.download_button(
        label="📥 Download HR Report Excel",
        data=output.getvalue(),
        file_name=f"GCC_HR_Report_{datetime.today().strftime('%Y%m%d')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
