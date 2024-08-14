# Product Analysis Dashboard

## Overview

This project provides a comprehensive analysis of product data collected from various sources. It includes data processing scripts and a Streamlit application for interactive data visualization. The project is designed to handle and analyze data from JSON files, including sales and product details, and to present this data through insightful visualizations.

## Project Structure

The project consists of the following main components:

1. **Data Processing Scripts**:
   - **`data_processing.py`**: Contains scripts for processing JSON data files, extracting relevant information, and creating DataFrames.
   - **`data_processing_additional.py`**: Handles additional data processing tasks, such as cleaning and aggregating data from multiple sources.
   
2. **Streamlit Application**:
   - **`app.py`**: The main script for running the Streamlit application. It provides a user-friendly interface for data analysis and visualization.

## Features

- **Overall Analysis**: Visualize total sales by keyword, average price trends, and daily sales heatmaps.
- **Single Keyword Analysis**: Analyze sales trends, price trends, quantity vs. price scatter plots, and cumulative sales for a selected keyword.
- **Product Details**: View detailed information about products, including titles, prices, images, and sales data.

## Customization

- **CSS Customization**: The Streamlit app includes custom CSS for styling the dashboard. Modify the CSS in `app.py` to adjust colors, fonts, and other styles to match your preferences.
- **Data Sources**: Ensure that your JSON files are correctly formatted and placed in the designated directories for proper processing.

## Contributing

Feel free to fork the repository and submit pull requests for any improvements or additional features. Please ensure that your contributions align with the project's goals and follow the coding standards established in the repository.

## Contact

For any questions or issues, please reach out to [elabass.oussama@gmail.com] or create an issue on the GitHub repository.
