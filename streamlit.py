import streamlit as st
import pandas as pd
import plotly.express as px
import time
from sqlalchemy import create_engine

# Start the auto-refresh loop in a separate thread
st.set_page_config(page_title="Dashboard",page_icon="🌍",layout="wide",)
st.subheader("🔔  Analytics Dashboard")
st.markdown("##")
theme_plotly = None # None or streamlit
# Style
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

    # Load your datasets and perform any necessary updates here
    data1 = pd.read_excel('ACM AND RESPECTIVE TEAM LEADERS (1) (7).xlsx')
    data2 = pd.read_excel('https://analytics.collections.co.ke/public/question/e4a43b9a-6a22-403b-af41-ac8d8c8c693a.xlsx')

    # Your data processing logic here
    engine = create_engine('postgresql://Onyinge_254:Nyamira2021#@localhost:5432/pi')
    # Render the updated content
    st.markdown("Last updated at: " + time.ctime())


# Create a sidebar
st.sidebar.image("IMAGE/i-logo.png",width=100,caption="Developed and Maintained by: Nehemiah: +254717205956")
st.sidebar.header("Filters")

# Add a checkbox to hide/show the merged and resulting dataset
show_merged_dataset = st.sidebar.checkbox("Show Merged and Resulting Dataset", value=True)       
if show_merged_dataset:
    # Merge the datasets based on matching 'acmname'
    merged_data = data1.merge(data2, left_on='acmname', right_on=data2.columns[0], how='left')

    # Replace 'N/A' with 0
    merged_data = merged_data.fillna(0)

    # Create a new DataFrame with specific columns
    resulting_data = merged_data[['acmname', 'TEAM LEADER', 'TARGET', 'callsmade', 'spoketo', 'ptpscreated', 'ptpamount', 'name']]
   
    with st.expander("Tabular"):
    # Display the resulting DataFrame
    #st.header("Acms Productivity")
     st.dataframe(resulting_data)
total_callsmade = resulting_data['callsmade'].sum()

# Calculate and display total target
total_target = resulting_data['TARGET'].sum()

# Calculate and display total ptpscreated
total_ptpscreated = resulting_data['ptpscreated'].sum()

# Calculate and display the total active acmname (with more than 0 callsmade)
total_active_acmname = resulting_data[resulting_data['callsmade'] > 0]['acmname'].nunique()

# Create a layout with 5 columns
total1, total2, total3, total4, total5 = st.columns(5, gap='large')

# Display the metrics with icons
with total1:
    st.info('ACMS',icon="📌")
    st.metric("Active_acms",f"{total_active_acmname:,.0f}")

with total2:
    st.info('TARGET',icon="📌")
    st.metric("daily_target", f"{total_target:,.0f}")

with total3:
    st.info('FILES WORKED',icon="📌")
    st.metric("total_calls_made", f"{total_callsmade:,.0f}")

with total4:
    st.info('PRODUCTIVE',icon="📌")
    st.metric("total_ptps_created", f"{total_ptpscreated:,.0f}")

 # Create a bar graph of team leaders with total callsmade
# Calculate the total count of acmname assigned to each TEAM LEADER
team_leader_counts = resulting_data.groupby('TEAM LEADER')['acmname'].count().reset_index()
team_leader_counts = team_leader_counts.rename(columns={'acmname': 'Total Acms'})

# Calculate the total count of active acmname for each TEAM LEADER
team_leader_active_acms = resulting_data[resulting_data['callsmade'] > 0].groupby('TEAM LEADER')['acmname'].count().reset_index()
team_leader_active_acms = team_leader_active_acms.rename(columns={'acmname': 'Active Acms'})

# Calculate the total ptpscreated for each TEAM LEADER
team_leader_ptpscreated = resulting_data.groupby('TEAM LEADER')['ptpscreated'].sum().reset_index()

# Merge the data into a single DataFrame
team_leader_summary = team_leader_counts.merge(team_leader_active_acms, on='TEAM LEADER')
team_leader_summary = team_leader_summary.merge(team_leader_ptpscreated, on='TEAM LEADER')

# Create a pie chart showing the percentage of callsmade per name
# Group data by 'name' and sum 'callsmade'
name_callsmade = resulting_data.groupby('name')['callsmade'].sum().reset_index()

# Create a 3D donut chart (a 3D pie chart with a hole)
fig_pie = px.pie(name_callsmade, names='name', values='callsmade', title="BRANCH PERFORMANCE", hole=0.4)
fig_pie.update_layout(width=400, height=300) 

# Create a layout with two columns to align the plots
col1, col2 = st.columns(2)


# Display the summary table in the first column
with col1:
    st.table(team_leader_summary)


# Display the pie chart in the second column
with col2:
    st.plotly_chart(fig_pie)

    while True:
        # Call the update_dashboard function to refresh the content
        
        # Sleep for 5 seconds to control the update frequency
        time.sleep(10)
        # Rerun the Streamlit app to update the content
        st.experimental_rerun()