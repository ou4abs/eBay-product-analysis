import json
import pandas as pd
from datetime import datetime
import os
import statsmodels.api as sm
# Function to convert timestamp
def convert_timestamp(ts):
    return datetime.utcfromtimestamp(ts / 1000).strftime('%m/%d/%Y')

# Function to process a single file
def process_file(file_path, keyword):
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Initialize a dictionary to hold the extracted data
    extracted_data = {'timestamp': [], 'averageSold': [], 'quantity': [], 'quantityRegressionLine': [], 'keyword': []}

    # Extract data
    for i in range(len(data['series'][0]['data'])):
        timestamp = convert_timestamp(data['series'][0]['data'][i][0])
        average_sold = data['series'][0]['data'][i][1]
        quantity = data['series'][1]['data'][i][1]
        quantity_regression_line = float('nan')  # Default to NaN
        
        # Check if the timestamp exists in the 'quantityRegressionLine' series
        for j in range(len(data['series'][2]['data'])):
            if data['series'][2]['data'][j][0] == data['series'][0]['data'][i][0]:
                quantity_regression_line = data['series'][2]['data'][j][1]
                break
        
        # Append data to the dictionary
        extracted_data['timestamp'].append(timestamp)
        extracted_data['averageSold'].append(average_sold)
        extracted_data['quantity'].append(quantity)
        extracted_data['quantityRegressionLine'].append(quantity_regression_line)
        extracted_data['keyword'].append(keyword)

    # Convert the dictionary to a DataFrame
    df = pd.DataFrame(extracted_data)
    return df

# Directory containing the files
directory = 'product_files'

# List all files in the directory
files = os.listdir(directory)

# Initialize an empty DataFrame to store all data
product = pd.DataFrame()

# Process each file and append to the all_data DataFrame
for file_name in files:
    if file_name.endswith('.txt'):  # Ensure you're only processing .txt files
        file_path = os.path.join(directory, file_name)
        keyword = os.path.splitext(file_name)[0]  # Use the file name without extension as the keyword
        df = process_file(file_path, keyword)
        product = pd.concat([product, df], ignore_index=True)
import json
import pandas as pd
import os

# Directory containing the .txt files
directory = 'stat'

# List to hold DataFrames
df_list = []

# Process each file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.txt'):
        file_path = os.path.join(directory, filename)
        
        try:
            # Attempt to open the file with utf-8 encoding
            with open(file_path, encoding='utf-8') as file:
                data = json.load(file)
        except UnicodeDecodeError:
            # If utf-8 fails, try opening the file with a different encoding
            with open(file_path, encoding='cp1252') as file:
                data = json.load(file)
        
        # Extract the data
        listings = []
        for item in data['results']:
            listing = {
                'title': item['listing']['title']['textSpans'][0]['text'],
                'price': item.get('avgsalesprice', {}).get('avgsalesprice', {}).get('textSpans', [{}])[0].get('text', 'N/A'),
                'link': item['listing']['title'].get('action', {}).get('URL', 'N/A'),
                'image': item['listing']['image'].get('URL', 'N/A'),
                'item_id': item['listing']['itemId'].get('value', 'N/A'),
                'avgshipping': item.get('avgshipping', {}).get('avgshipping', {}).get('textSpans', [{}])[0].get('text', 'N/A'),
                'itemssold': item.get('itemssold', {}).get('textSpans', [{}])[0].get('text', 'N/A'),
                'totalsales': item.get('totalsales', {}).get('textSpans', [{}])[0].get('text', 'N/A'),
                'datelastsold': item.get('datelastsold', {}).get('textSpans', [{}])[0].get('text', 'N/A'),
                'keyword': filename.replace('.txt', '')  # Add the keyword column
            }
            listings.append(listing)
        
        # Create a DataFrame
        df = pd.DataFrame(listings)
        
        # Clean up the data
        df['price'] = df['price'].str.replace('$', '').astype(float, errors='ignore')
        df['avgshipping'] = df['avgshipping'].str.replace('$', '').astype(float, errors='ignore')
        df['itemssold'] = df['itemssold'].str.replace(',', '').astype(int, errors='ignore')
        df['totalsales'] = df['totalsales'].str.replace('$', '').str.replace(',', '').astype(float, errors='ignore')
        
        # Append to the list of DataFrames
        df_list.append(df)

# Concatenate all DataFrames into one
all_data_df = pd.concat(df_list, ignore_index=True)
df_any_na=all_data_df.replace('N/A', pd.NA, inplace=True)
all_data_df = all_data_df.dropna()
import json
import pandas as pd
import os

# Directory containing the text files
directory = 'agg_files'

# Initialize an empty list to hold data from all files
all_data = []

# Check if directory exists
if not os.path.isdir(directory):
    print(f"Directory does not exist: {directory}")
else:
    # Iterate over all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            keyword = os.path.splitext(filename)[0]  # Get filename without extension
            
            print(f"Processing file: {filename}")  # Debug: Print the current file being processed
            
            try:
                # Load JSON data from the file
                with open(file_path, encoding='utf-8') as file:
                    data = json.load(file)
                
                # Extract the relevant information
                if 'sections' in data:
                    for section in data['sections']:
                        if 'dataItems' in section:
                            for item in section['dataItems']:
                                header = item['header']['textSpans'][0].get('text', 'N/A')
                                value = item['value']['textSpans'][0].get('text', 'N/A')
                                all_data.append({"Header": header, "Value": value, "Keyword": keyword})
                        else:
                            print(f"No 'dataItems' key found in section of {filename}")
                else:
                    print(f"No 'sections' key found in {filename}")

            except Exception as e:
                print(f"Error processing file {filename}: {e}")

    # Convert the list of data to a DataFrame
    agg = pd.DataFrame(all_data)

import streamlit as st
import pandas as pd
import plotly.express as px

# Set page config
st.set_page_config(layout="wide", page_title="Product Analysis Dashboard")

# Custom CSS to enhance the appearance
st.markdown("""
<style>
    /* Main page styling */
    .reportview-container {
        background: #0e1117;
        color: #ffffff;
    }
    .main {
        background: #0e1117;
    }
    
    /* Typography */
    .big-font {
        font-size: 36px !important;
        font-weight: bold;
        color: #7055bb;
        text-align: center;
        margin-bottom: 30px;
    }
    .medium-font {
        font-size: 24px !important;
        font-weight: bold;
        color: #f36219;
        margin-top: 30px;
        margin-bottom: 20px;
    }
    .small-font {
        font-size: 16px !important;
        color: #293b76;
        font-style: italic;
    }
    
    /* Updated styles for the sidebar and navigation */
    .sidebar .sidebar-content {
        background-color: #0e1117;
        color: #ffffff;
    }
    .sidebar .sidebar-content .big-font {
        color: #7055bb;
        font-size: 28px !important;
        margin-bottom: 20px;
    }
    
    /* Custom styles for radio buttons */
    .stRadio > div {
        background-color: #ebf0e9 !important;
        padding: 0 !important;
    }
    .stRadio > div > label {
        background-color: #ebf0e9 !important;
        color: white !important;
        padding: 10px !important;
        border-radius: 80px !important;
        cursor: pointer;
    }
    .stRadio > div > label:hover {
        background-color: #1e2130 !important;
    }
    .stRadio > div[role="radiogroup"] > label[data-checked="true"] {
        background-color: #293b76 !important;
        border: 1px solid #7055bb !important;
    }

    /* Remove any unwanted backgrounds or borders */
    .sidebar .sidebar-content [data-testid="stVerticalBlock"] {
        background-color: transparent !important;
        border: none !important;
    }
    
    /* Dataframe styling */
    .dataframe {
        font-size: 14px !important;
    }
    .dataframe th {
        background-color: #293b76;
        color: white;
    }
    .dataframe td {
        background-color: #1e2130;
    }
    
    /* Remove padding and gap between charts and titles */
    .stPlotlyChart {
        padding: 0 !important;
        margin-bottom: -30px !important;
    }

    /* Custom styles for select box */
    div[data-baseweb="select"] > div {
        background-color: #95a5db !important;  /* Background color of the select box */
        border-color: #95a5db !important;  /* Border color of the select box */
    }
    
    /* Text color inside the select box */
    div[data-baseweb="select"] {
        color: #ffffff !important;
    }

    /* Dropdown menu styling */
    div[data-baseweb="menu"] {
        background-color: #293b76 !important;  /* Background color of the dropdown */
        color: #ffffff !important;  /* Text color of the options */
    }

</style>

<script>
    // JavaScript to change select box arrow color
    const intervalId = setInterval(() => {
        const selectArrow = document.querySelector('div[data-baseweb="select"] svg');
        if (selectArrow) {
            selectArrow.style.fill = 'white';
            clearInterval(intervalId);
        }
    }, 100);
</script>
""", unsafe_allow_html=True)


# Sidebar
st.sidebar.markdown('<p class="big-font">Navigation</p>', unsafe_allow_html=True)
page = st.sidebar.radio("Go to", ("Overall Analysis", "Single Keyword Analysis", "Product Details"), key="navigation")

if page == "Overall Analysis":
    st.markdown('<p class="big-font">Overall Keyword Analysis</p>', unsafe_allow_html=True)

    # 1. Total Sales by Keyword
    st.markdown('<p class="medium-font">Total Sales by Keyword</p>', unsafe_allow_html=True)
    keyword_totals = product.groupby('keyword')['quantity'].sum().sort_values(ascending=False)
    fig = px.bar(keyword_totals, x=keyword_totals.index, y=keyword_totals.values, 
                 color=keyword_totals.values, color_continuous_scale='Blues')
    fig.update_layout(
        xaxis_title="Keyword", yaxis_title="Total Quantity Sold",
        plot_bgcolor='#0e1117', paper_bgcolor='#0e1117',
        font=dict(size=16, color="#ffffff"),
        xaxis=dict(gridcolor="#3b3f5c", title_font=dict(color="#14e2b7")),
        yaxis=dict(gridcolor="#3b3f5c", title_font=dict(color="#14e2b7"))
    )
    st.plotly_chart(fig, use_container_width=True)

    # 2. Average Price Trend
    st.markdown('<p class="medium-font">Average Price Trend</p>', unsafe_allow_html=True)
    avg_price = product.groupby('timestamp')['averageSold'].mean().reset_index()
    fig = px.line(avg_price, x='timestamp', y='averageSold', line_shape='spline', 
                  color_discrete_sequence=['#14e2b7'])
    fig.update_layout(
        xaxis_title="Date", yaxis_title="Average Sold Price",
        plot_bgcolor='#0e1117', paper_bgcolor='#0e1117',
        font=dict(size=16, color="#ffffff"),
        xaxis=dict(gridcolor="#3b3f5c", title_font=dict(color="#14e2b7")),
        yaxis=dict(gridcolor="#3b3f5c", title_font=dict(color="#14e2b7"))
    )
    st.plotly_chart(fig, use_container_width=True)

    # 3. Heatmap of Daily Sales
    st.markdown('<p class="medium-font">Heatmap of Daily Sales</p>', unsafe_allow_html=True)
    pivot = product.pivot(index='keyword', columns='timestamp', values='quantity')
    fig = px.imshow(pivot, aspect="auto", color_continuous_scale='YlGnBu')
    fig.update_layout(
        xaxis_title="Date", yaxis_title="Keyword",
        plot_bgcolor='#0e1117', paper_bgcolor='#0e1117',
        font=dict(size=16, color="#ffffff"),
        xaxis=dict(title_font=dict(color="#14e2b7")),
        yaxis=dict(title_font=dict(color="#14e2b7"))
    )
    st.plotly_chart(fig, use_container_width=True)

elif page == "Single Keyword Analysis":
    st.markdown('<p class="big-font">Single Keyword Analysis</p>', unsafe_allow_html=True)

    # Keyword selection
    keyword = st.selectbox("Select a keyword", options=product['keyword'].unique(), key="keyword_select")
    keyword_data = product[product['keyword'] == keyword]

    col1, col2 = st.columns(2)

    with col1:
        # 3. Quantity vs Price Scatter Plot
    st.markdown('<p class="medium-font">Quantity vs Price</p>', unsafe_allow_html=True)
    fig = px.scatter(keyword_data, x='averageSold', y='quantity', trendline="ols", 
                     color='quantity', color_continuous_scale='RdBu')
    fig.update_layout(
        xaxis_title="Average Sold Price", yaxis_title="Quantity Sold",
        plot_bgcolor='#0e1117', paper_bgcolor='#0e1117',
        font=dict(size=16, color="#ffffff"),
        xaxis=dict(title_font=dict(color="#14e2b7")),
        yaxis=dict(title_font=dict(color="#14e2b7"))
    )
    st.plotly_chart(fig, use_container_width=True)

    with col2:
        # 2. Price Trend
        st.markdown('<p class="medium-font">Price Trend</p>', unsafe_allow_html=True)
        fig = px.line(keyword_data, x='timestamp', y='averageSold', line_shape='spline', 
                      color_discrete_sequence=['#e74c3c'])
        fig.update_layout(
            xaxis_title="Date", yaxis_title="Average Sold Price",
            plot_bgcolor='#0e1117', paper_bgcolor='#0e1117',
            font=dict(size=16, color="#ffffff"),
            xaxis=dict(gridcolor="#3b3f5c", title_font=dict(color="#14e2b7")),
            yaxis=dict(gridcolor="#3b3f5c", title_font=dict(color="#14e2b7"))
        )
        st.plotly_chart(fig, use_container_width=True)
    # 3. Sales Trend
        st.markdown('<p class="medium-font">Sales Trend</p>', unsafe_allow_html=True)
        fig = px.scatter(keyword_data, x='averageSold', y='quantity', trendline="lowess", 
                         color='quantity', color_continuous_scale='RdBu')
        fig.update_layout(
            xaxis_title="Average Sold Price", yaxis_title="Quantity Sold",
            plot_bgcolor='#0e1117', paper_bgcolor='#0e1117',
            font=dict(size=16, color="#ffffff"),
            xaxis=dict(gridcolor="#3b3f5c", title_font=dict(color="#14e2b7")),
            yaxis=dict(gridcolor="#3b3f5c", title_font=dict(color="#14e2b7"))
        )
        st.plotly_chart(fig, use_container_width=True)
    # 4. Cumulative Sales
    st.markdown('<p class="medium-font">Cumulative Sales</p>', unsafe_allow_html=True)
    keyword_data['cumulative_sales'] = keyword_data['quantity'].cumsum()
    fig = px.line(keyword_data, x='timestamp', y='cumulative_sales', line_shape='spline', 
                  color_discrete_sequence=['#9b59b6'])
    fig.update_layout(
        xaxis_title="Date", yaxis_title="Cumulative Sales",
        plot_bgcolor='#0e1117', paper_bgcolor='#0e1117',
        font=dict(size=16, color="#ffffff"),
        xaxis=dict(gridcolor="#3b3f5c", title_font=dict(color="#14e2b7")),
        yaxis=dict(gridcolor="#3b3f5c", title_font=dict(color="#14e2b7"))
    )
    st.plotly_chart(fig, use_container_width=True)

    # 5. Summary Statistics
    st.markdown('<p class="medium-font">Summary Statistics</p>', unsafe_allow_html=True)
    summary = keyword_data[['averageSold', 'quantity']].describe()
    st.dataframe(summary, use_container_width=True)
elif page == "Product Details":
    st.markdown('<p class="big-font">Product Details</p>', unsafe_allow_html=True)

    # Keyword selection
    keyword = st.selectbox("Select a keyword", options=all_data_df['keyword'].unique(), key="product_keyword_select")
    keyword_data = all_data_df[all_data_df['keyword'] == keyword]

    # Filter the mini table data based on the selected keyword
    filtered_agg = agg[agg['Keyword'] == keyword]

    # Extract specific summary values
    summary_values = {
        'Free shipping': filtered_agg[filtered_agg['Header'] == 'Free shipping']['Value'].values[0] if 'Free shipping' in filtered_agg['Header'].values else 'N/A',
        'Total sellers': filtered_agg[filtered_agg['Header'] == 'Total sellers']['Value'].values[0] if 'Total sellers' in filtered_agg['Header'].values else 'N/A',
        'Sell-through': filtered_agg[filtered_agg['Header'] == 'Sell-through']['Value'].values[0] if 'Sell-through' in filtered_agg['Header'].values else 'N/A'
    }

    # Display the summary information as columns
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<p class="metric-title">Free Shipping</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="metric-value">{summary_values["Free shipping"]}</p>', unsafe_allow_html=True)
    with col2:
        st.markdown('<p class="metric-title">Total Sellers</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="metric-value">{summary_values["Total sellers"]}</p>', unsafe_allow_html=True)
    with col3:
        st.markdown('<p class="metric-title">Sell-through</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="metric-value">{summary_values["Sell-through"]}</p>', unsafe_allow_html=True)

    # Sort the DataFrame by 'itemssold' and 'totalsales'
    keyword_data = keyword_data.sort_values(by=['itemssold', 'totalsales'], ascending=[False, False])

    # Optionally, add some visualizations
    st.markdown('<p class="medium-font">Price Distribution</p>', unsafe_allow_html=True)
    fig = px.histogram(keyword_data, x='price', nbins=20, color_discrete_sequence=['#14e2b7'])
    fig.update_layout(
        xaxis_title="Price", yaxis_title="Count",
        plot_bgcolor='#0e1117', paper_bgcolor='#0e1117',
        font=dict(size=16, color="#ffffff"),
        xaxis=dict(gridcolor="#3b3f5c", title_font=dict(color="#14e2b7")),
        yaxis=dict(gridcolor="#3b3f5c", title_font=dict(color="#14e2b7"))
    )
    st.plotly_chart(fig, use_container_width=True)

    # Now, display the title for the table
    st.markdown('<p class="medium-font">Product Listings</p>', unsafe_allow_html=True)

    # Custom CSS for the page
    custom_css = """
    <style>
    .big-font {
        font-size: 24px;
        color: #7055bb;
    }
    .medium-font {
        font-size: 18px;
        color: #f36219;
    }
    .metric-title {
        font-size: 16px;
        color: #829f0d;
        font-weight: bold;
    }
    .metric-value {
        font-size: 20px;
        color: #14e2b7;
        font-weight: bold;
    }
    table {
        color: #ffffff;
        font-size: 14px;
        border-collapse: collapse;
        width: 100%;
    }
    th {
        background-color: #293b76;
        color: white;
        font-weight: bold;
        padding: 10px;
        text-align: left;
        border-bottom: 2px solid #7055bb;
    }
    td {
        background-color: #1e2130;
        padding: 8px;
        border-bottom: 1px solid #3b3f5c;
    }
    tr:hover {
        background-color: #2c3154;
    }
    img {
        max-width: 100px;
        max-height: 100px;
    }
    a {
        color: #14e2b7;
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
    }
    </style>
    """
    
    # Apply custom CSS
    st.markdown(custom_css, unsafe_allow_html=True)

    # Function to create clickable title with link
    def make_clickable(title, link):
        return f'<a href="{link}" target="_blank">{title}</a>'

    # Function to display image with link
    def image_with_link(image_url, link):
        return f'<a href="{link}" target="_blank"><img src="{image_url}" alt="Product Image"></a>'

    # Prepare the DataFrame for display
    display_df = keyword_data[['title', 'price', 'avgshipping', 'itemssold', 'totalsales', 'datelastsold', 'image', 'link']]
    display_df['title'] = display_df.apply(lambda x: make_clickable(x['title'], x['link']), axis=1)
    display_df['image'] = display_df.apply(lambda x: image_with_link(x['image'], x['link']), axis=1)
    display_df = display_df.drop(columns=['link'])  # Remove the link column as it's now integrated
    
    # Convert DataFrame to HTML and apply custom styling
    table_html = display_df.to_html(escape=False, index=False)
    table_style = """
    <style>
    table {
        color: #ffffff;
        font-size: 14px;
        border-collapse: collapse;
        width: 100%;
    }
    th {
        background-color: #293b76;
        color: white;
        font-weight: bold;
        padding: 10px;
        text-align: left;
        border-bottom: 2px solid #7055bb;
    }
    td {
        background-color: #1e2130;
        padding: 8px;
        border-bottom: 1px solid #3b3f5c;
    }
    tr:hover {
        background-color: #2c3154;
    }
    img {
        max-width: 100px;
        max-height: 100px;
    }
    a {
        color: #14e2b7;
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
    }
    </style>
    """
    styled_table = f"{table_style}\n{table_html}"
    
    # Display the styled table
    st.markdown(styled_table, unsafe_allow_html=True)

# Footer
st.markdown('<p class="small-font">Ebay July History</p>', unsafe_allow_html=True)
