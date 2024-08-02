import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the Excel file
df = pd.read_excel('yoga.xlsx')

# Format Store IDs to avoid comma separation
df['name'] = df['name'].astype(str)

# Define pages
def store_details():
    st.sidebar.header('Select Yoga Studio')
    store_id = st.sidebar.selectbox('Name', df['name'].unique())

    # Filter data for the selected studio
    store_data = df[df['name'] == store_id].iloc[0]

    # Display store attributes
    st.header(f'Yoga Studio: {store_id}')
    st.write('### Store Details')
    st.write(f"*Address:* {store_data['address']}")
    st.write(f"*Phone:* {store_data['phone']}")
    st.write(f"*Email:* {store_data['email']}")
    st.write(f"*Total Population:* {store_data['Total population']}")
    st.write(f"*Male Population:* {store_data['Male population']}")
    st.write(f"*Female Population:* {store_data['Female Population']}")
    st.write(f"*Median Income:* {store_data['Median Income']}")
    st.write(f"*Mean Income:* {store_data['Mean Income']}")
    st.write(f"*URL:* [Link]({store_data['url']})")
    st.write(f"*Star Count:* {store_data['star_count']}")
    st.write(f"*Rating Count:* {store_data['rating_count']}")
    st.write(f"*Primary Category:* {store_data['primary_category_name']}")
    st.write(f"*Category:* {store_data['category_name']}")
    st.write(f"*Facebook Profile:* [Link]({store_data['Facebook Profile']})")
    st.write(f"*Instagram Handle:* {store_data['Instagram Handle']}")
    st.write(f"*LinkedIn:* [Link]({store_data['LinkedIn']})")
    st.write(f"*Twitter:* {store_data['Twitter']}")
    st.write(f"*YouTube:* [Link]({store_data['YouTube']})")
    st.write(f"*Grading Score:* {store_data['Grading score']}")
    st.write(f"*Radius:* {int(store_data['Radius'])} km")
    st.write(f"*What to Sell:* {store_data['What to sell']}")
    st.write(f"*Insight:* {store_data['Insight']}")
    st.write(f"*Summary:* {store_data['Summary']}")

    # Pie chart for Male/Female Population
    st.write('### Population Distribution')
    labels = ['Male Population', 'Female Population']
    sizes = [store_data['Male population'], store_data['Female Population']]
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
    summary = df[['name', 'address', 'zip', 'phone', 'email', 'Total population', 'Male population', 'Female Population', 'Median Income', 'Mean Income', 'Grading score', 'Radius', 'What to sell', 'Insight', 'Summary']]
    st.dataframe(summary)

def store_comparison():
    st.sidebar.header('Select Stores to Compare')
    selected_stores = st.sidebar.multiselect('Yoga Studios', df['name'].unique())

    if len(selected_stores) > 1:
        st.header('Store Comparison')
        st.write('### Comparison of Selected Stores')

        store_data_list = []
        for store_id in selected_stores:
            store_data = df[df['name'] == store_id].T
            store_data.columns = [store_id]
            store_data_list.append(store_data)

        # Display the stores' data side by side
        comparison_df = pd.concat(store_data_list, axis=1)
        st.dataframe(comparison_df)

# Create a navigation menu
st.sidebar.title('Navigation')
page = st.sidebar.radio('Go to', ['Store Details', 'Summary Statistics', 'Store Comparison'])

# Render the selected page
if page == 'Store Details':
    store_details()
elif page == 'Summary Statistics':
    summary_statistics()
elif page == 'Store Comparison':
    store_comparison()
