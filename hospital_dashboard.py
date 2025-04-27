# Hospital Management System Dashboard 

import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------
# 1. Load Data from CSVs
# --------------------------------------------

# Read CSV files
patient_data = pd.read_csv('patient_data.csv')
appointment_data = pd.read_csv('appointment_data.csv')
billing_data = pd.read_csv('billing_data.csv')
lab_report_data = pd.read_csv('lab_report_data.csv')
doctor_data = pd.read_csv('doctor_data.csv')

# --------------------------------------------
# 2. Dashboard Design
# --------------------------------------------

st.title('🏥 Hospital Management System Dashboard')

# Section: Billing Payment Status
st.header('Billing Payment Status Distribution')
billing_status_counts = billing_data['PaymentStatus'].value_counts().reset_index()
billing_status_counts.columns = ['PaymentStatus', 'Counts']

pie_chart = px.pie(billing_status_counts, names='PaymentStatus', values='Counts', title='Billing Status')
st.plotly_chart(pie_chart)
st.write("**Insight:** Billing payments are fairly balanced among 'Paid', 'Pending', and 'Rejected', indicating an opportunity to further improve the payment clearance process.")

# Section: Appointments per Doctor (Doctor Name instead of ID)
st.header('Top 10 Doctors by Appointments')
appointments_with_doctor = appointment_data.merge(doctor_data, left_on='DID', right_on='DID')
appointments_count = appointments_with_doctor['Name'].value_counts().reset_index()
appointments_count.columns = ['DoctorName', 'Appointments']

bar_chart = px.bar(appointments_count.head(10), x='DoctorName', y='Appointments', title='Top 10 Doctors by Number of Appointments')
st.plotly_chart(bar_chart)
st.write("**Insight:** Certain doctors manage significantly more appointments, indicating specialization or higher patient trust.")

# Section: Lab Reports Submitted Over Time
st.header('Lab Reports Submitted Over Time')
lab_reports_over_time = lab_report_data['ReportDate'].value_counts().reset_index()
lab_reports_over_time.columns = ['ReportDate', 'Reports']
lab_reports_over_time = lab_reports_over_time.sort_values('ReportDate')

line_chart = px.line(lab_reports_over_time, x='ReportDate', y='Reports', title='Lab Reports Trend')
st.plotly_chart(line_chart)
st.write("**Insight:** Lab report submissions fluctuate over time, potentially reflecting seasonal trends or hospital admission patterns.")

# Section: Patient Gender Distribution
st.header('Patient Gender Ratio')
gender_distribution = patient_data['Gender'].value_counts().reset_index()
gender_distribution.columns = ['Gender', 'Counts']

gender_pie_chart = px.pie(gender_distribution, names='Gender', values='Counts', title='Gender Distribution')
st.plotly_chart(gender_pie_chart)
st.write("**Insight:** The hospital serves a diverse patient population across different genders.")

# --------------------------------------------
# 3. Summary Section
# --------------------------------------------

st.markdown("---")
st.subheader('Summary of Insights')
st.write("1. Billing payments are fairly balanced but could be improved for pending and rejected bills.")
st.write("2. Certain doctors are more popular based on appointment counts.")
st.write("3. Lab reports show seasonal trends, with fluctuations over months.")
st.write("4. The gender distribution among patients is fairly even.")

# End of Dashboard
