# Hospital Management Dashboard using Streamlit

import streamlit as st
import pandas as pd
import plotly.express as px
import psycopg2
from sqlalchemy import create_engine

# --------------------------------------------
# 1. Data Connection & Queries (5 Points)
# --------------------------------------------


# Database connection parameters
host = 'db.kjgvvqzpfqhcgsixmeol.supabase.co'
database = 'postgres'
user = 'postgres'
password = 'Helloshubham@123'
port = '5432'

engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}')

# Queries:

# Query 1: Billing Status Distribution
billing_status_query = pd.read_sql("""
SELECT PaymentStatus, COUNT(*) AS Counts
FROM Billing
GROUP BY PaymentStatus
""", engine)

# Query 2: Appointments per Doctor (using Doctor Name)
appointments_per_doctor_query = pd.read_sql("""
SELECT d.Name AS doctorname, COUNT(a.AID) AS appointments
FROM Appointment a
JOIN Doctor d ON a.DID = d.DID
GROUP BY d.Name
ORDER BY appointments DESC
""", engine)

# Query 3: Lab Reports Over Time (ReportDate on X-axis)
lab_reports_over_time_query = pd.read_sql("""
SELECT ReportDate::DATE AS reportdate, COUNT(*) AS reports
FROM LabReports
GROUP BY reportdate
ORDER BY reportdate
""", engine)

# Query 4: Patient Gender Distribution
gender_distribution_query = pd.read_sql("""
SELECT Gender, COUNT(*) AS Counts
FROM Patient
GROUP BY Gender
""", engine)

# --------------------------------------------
# 2. Dashboard Design (3 Points)
# --------------------------------------------

st.title('🏥 Hospital Management System Dashboard')

# Section: Billing Payment Status
st.header('Billing Payment Status Distribution')
pie_chart = px.pie(billing_status_query, names='paymentstatus', values='counts', title='Billing Status')
st.plotly_chart(pie_chart)
st.write("**Insight:** Billing payments are fairly balanced among 'Paid', 'Pending', and 'Rejected', indicating an opportunity to further improve the payment clearance process.")

# Section: Appointments per Doctor (Using Doctor Name)
st.header('Top Doctors by Appointments')
bar_chart = px.bar(appointments_per_doctor_query.head(10), x='doctorname', y='appointments', title='Top 10 Doctors by Number of Appointments')
st.plotly_chart(bar_chart)
st.write("**Insight:** Most doctors have a relatively low number of appointments, suggesting distributed workload across doctors rather than high specialization.")

# Section: Lab Reports Over Time
st.header('Lab Reports Submitted Over Time')
line_chart = px.line(lab_reports_over_time_query, x='reportdate', y='reports', title='Lab Reports Trend Over Time')
st.plotly_chart(line_chart)
st.write("**Insight:** Lab report submissions show fluctuations over time but maintain consistency overall, implying stable operational activity with occasional spikes.")

# Section: Patient Gender Distribution
st.header('Patient Gender Ratio')
second_pie_chart = px.pie(gender_distribution_query, names='gender', values='counts', title='Gender Distribution among Patients')
st.plotly_chart(second_pie_chart)
st.write("**Insight:** The hospital serves a diverse patient population across different genders, highlighting equitable healthcare access to all demographics.")

# --------------------------------------------
# 3. Summary Insights (2 Points)
# --------------------------------------------

st.markdown("---")
st.subheader('Summary of Insights')

st.write("1. Billing payments are fairly balanced among 'Paid', 'Pending', and 'Rejected', indicating an opportunity to further improve the payment clearance process.")
st.write("2. Most doctors have a relatively low number of appointments, suggesting distributed workload across doctors rather than high specialization.")
st.write("3. Lab report submissions show fluctuations over time but maintain consistency overall, implying stable operational activity with occasional spikes.")
st.write("4. Gender distribution among patients is quite even across Male, Female, and Other categories, highlighting equitable healthcare access to all demographics.")

# End of Dashboard
