import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt 
import plotly.express as px



st.title("Minger Store Data")

df = pd.read_excel("Cleaned_Data.xlsx")
st.write(df)

#DatePicker
col1,col2 = st.columns((2))
df["Order Date"] = pd.to_datetime(df["Order Date"])

startDate = pd.to_datetime(df["Order Date"]).min()
endDate = pd.to_datetime(df["Order Date"]).max()

with col1:
    date1=pd.to_datetime(st.date_input("Start Date", startDate))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date",endDate))

df = df[(df["Order Date"]>= date1) & (df["Order Date"] <= date2)].copy()

#SideBar
region_options = df['Region'].unique()
selected_region = st.sidebar.selectbox('Choose Region', region_options)
if selected_region != 'All':  
  filtered_df = df[df['Region'] == selected_region]
else:
  filtered_df = df.copy()

st.dataframe(filtered_df)


#Pie Chart Profits based on Region
region_profit = df.groupby('Region')['Profit'].sum()
pie_chart_data = region_profit.tolist()
pie_chart_labels = region_profit.index.tolist()
plt.figure(figsize=(8, 8))
plt.pie(pie_chart_data, labels=pie_chart_labels, autopct='%1.1f%%', startangle=140)  #
plt.title('Profit Distribution by Region')
plt.axis('equal')  
st.pyplot(plt)

#bar chart representing sales of categories filtered by segment
segment_options = df['Segment'].unique()
selected_segment = st.sidebar.selectbox('Choose Segment', segment_options)
segment_df = df[df['Segment'] == selected_segment]

plt.figure(figsize=(10, 6))
plt.bar(segment_df['Category'], segment_df['Sales'])
plt.xlabel('Category')
plt.ylabel('Sales')
plt.title(f'Sales by Category (Segment: {selected_segment})')
plt.xticks(rotation=45, ha='right')  
plt.grid(axis='y')

st.pyplot(plt)

#Pie chart displaying categories filtered by order prioity
priority_options = df['Order Priority'].unique()
selected_priority = st.sidebar.selectbox('Choose Order Priority', priority_options)
priority_df = df[df['Order Priority'] == selected_priority]
category_sales = priority_df.groupby('Category')['Sales'].sum() 

pie_chart_data = category_sales.tolist()
pie_chart_labels = category_sales.index.tolist()

plt.figure(figsize=(8, 8))
plt.pie(pie_chart_data, labels=pie_chart_labels, autopct='%1.1f%%', startangle=140)  
plt.title(f'Product Category Distribution (Order Priority: {selected_priority})')
plt.axis('equal')  
st.pyplot(plt)

#Line Chart for Discount Vs Profit filtered by categories
category_options = df['Category'].unique()
selected_category = st.sidebar.selectbox('Choose Product Category', category_options)

category_df = df[df['Category'] == selected_category]

plt.figure(figsize=(10, 6))
plt.plot(category_df['Discount'], category_df['Profit'])
plt.xlabel('Discount')
plt.ylabel('Profit')
plt.title(f'Discount vs. Profit (Category: {selected_category})')
plt.grid(True)

st.pyplot(plt)

