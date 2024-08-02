import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Load the Excel file
df = pd.read_excel('yogabar.final.xlsx')

# Format Store IDs to avoid comma separation
df['Store ID'] = df['Store ID'].astype(str)

# Define pages
def store_details():
    st.sidebar.header('Select Store ID')
    store_id = st.sidebar.selectbox('Store ID', df['Store ID'].unique())

    # Filter data for the selected Store ID
    store_data = df[df['Store ID'] == store_id].iloc[0]

    # Display store attributes
    st.header(f'Store ID: {store_id}')
    st.write('### Store Details')
    st.write(f"*Seller Name:* {store_data['Seller Name']}")
    st.write(f"*Address:* {store_data['Address']}")
    st.write(f"*Pincode:* {store_data['Pincode']}")
    st.write(f"*Sales:* {store_data['Sales']}")
    st.write(f"*Area of Pincode:* {store_data['Area of pincode']} km²")
    st.write(f"*Population Density:* {store_data['Population Density']}")
    st.write(f"*Prosperity Index:* {store_data['Prosperity Index']}")
    st.write(f"*Market Penetration:* {store_data['Market Penetration']}")
    st.write(f"*Expansion Score:* {store_data['Expansion Score']}")
    st.write(f"*What to Sell:* {store_data['What to Sell']}")
    st.write(f"*Where What How (WWH):* {store_data['WWH']}")
    st.write(f"*Summary:* {store_data['Summary']}")
    st.write(f"*Outliers:* {store_data['Outliers']}")
    st.write(f"*Segment:* {store_data['Segment']}")

    # Pie chart for Male/Female Population
    st.write('### Population Distribution')
    labels = ['Male Population', 'Female Population']
    sizes = [store_data['Male Population'], store_data['Female Population']]
    colors = ['#ff9999', '#66b3ff']
    explode = (0.1, 0)  # explode the 1st slice

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    st.pyplot(fig1)

def summary_statistics():
    st.header('Summary Statistics')

    st.write('### All Stores Summary')
    summary = df[['Store ID', 'Seller Name', 'Expansion Score', 'What to Sell', 'Market Penetration', 'Summary', 'Outliers', 'Segment']]
    st.dataframe(summary)

    # Sort the DataFrame by Sales in descending order
    df_sales_sorted = df.sort_values(by='Sales', ascending=False)

    # Sort the DataFrame by Market Penetration in descending order
    df_penetration_sorted = df.sort_values(by='Market Penetration', ascending=False)

    # Create interactive bar graph for Sales
    st.header('Sales by Store ID (Descending Order)')
    sales_fig = px.bar(df_sales_sorted, x='Store ID', y='Sales', hover_data=['Seller Name'],
                   labels={'Sales': 'Sales', 'Store ID': 'Store ID'},
                   title='Sales by Store ID (Descending Order)')
    sales_fig.update_xaxes(categoryorder='array', categoryarray=df_sales_sorted['Store ID'])
    sales_fig.update_traces(marker_line_width=2)
    sales_fig.update_layout(
    xaxis={'categoryorder': 'total descending', 'type': 'category', 'tickangle': -45},
    height=600,
    width=1000,
    margin=dict(l=0, r=0, t=50, b=100),
    bargap=0.2,
    bargroupgap=0.5
    )
    st.plotly_chart(sales_fig, use_container_width=True)

    # Create interactive bar graph for Market Penetration
    st.header('Market Penetration by Store ID (Descending Order)')
    penetration_fig = px.bar(df_penetration_sorted, x='Store ID', y='Market Penetration', hover_data=['Seller Name'],
                         labels={'Market Penetration': 'Market Penetration', 'Store ID': 'Store ID'},
                         title='Market Penetration by Store ID (Descending Order)')
    penetration_fig.update_xaxes(categoryorder='array', categoryarray=df_penetration_sorted['Store ID'])
    penetration_fig.update_traces(marker_line_width=2)
    penetration_fig.update_layout(
    xaxis={'categoryorder': 'total descending', 'type': 'category', 'tickangle': -45},
    height=600,
    width=1000,
    margin=dict(l=0, r=0, t=50, b=100),
    bargap=0.2,
    bargroupgap=0.5
    )
    st.plotly_chart(penetration_fig, use_container_width=True)
 

def store_comparison():
    st.sidebar.header('Select Stores to Compare')
    selected_stores = st.sidebar.multiselect('Store IDs', df['Store ID'].unique())

    if len(selected_stores) > 1:
        st.header('Store Comparison')
        st.write('### Comparison of Selected Stores')

        store_data_list = []
        for store_id in selected_stores:
            store_data = df[df['Store ID'] == store_id].T
            store_data.columns = [store_id]
            store_data_list.append(store_data)

        # Display the stores' data side by side
        for i, store_data in enumerate(store_data_list):
            if i == 0:
                comparison_df = store_data
            else:
                comparison_df = pd.concat([comparison_df, store_data], axis=1)

        st.dataframe(comparison_df)

# Create a navigation menu
st.sidebar.title('Navigation')
page = st.sidebar.radio('Go to', ['Store Details', 'Summary Statistics', 'Store Comparison'])

st.markdown(
                """
                <style>
                [data-testid="stElementToolbar"] {
                    display: none;
                }
                </style>
                """,
                unsafe_allow_html=True)

# Render the selected page
if page == 'Store Details':
    store_details()
elif page == 'Summary Statistics':
    summary_statistics()
elif page == 'Store Comparison':
    store_comparison()