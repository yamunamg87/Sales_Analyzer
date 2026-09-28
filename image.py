import streamlit as st
import google.generativeai as genai
from PIL import Image

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Sales Data Analysis",
    page_icon="📈",
    layout="wide"
)

st.title("📊 Sales Data Analyzer")
st.write("Upload a image and get insights using Gemini-3.5-Flash-lite")

# -----------------------------
# Gemini API Configuration
# -----------------------------
GOOGLE_API_KEY = "AQ.Ab8RN6KFPPeMK-pTYbLM7l2jjfoLOEOENB6LUd1z6CY01_t4-A"

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel("gemini-3.5-flash-lite")  

# -----------------------------
# Image Upload
# -----------------------------
uploaded_file = st.file_uploader(
    "Upload a Image",
    type=["jpg", "jpeg", "png"]
)

# -----------------------------
# Analyze Button
# -----------------------------
if uploaded_file is not None:

    image = Image.open(uploaded_file)

    col1, col2 = st.columns(2)

    with col1:
        st.image(image, caption="Uploaded Image", use_container_width=True)

    with col2:

        if st.button("Analyze Image"):

            with st.spinner("Analyzing image..."):

                prompt = """
                You are an AI Sales Data Analysis Assistant.

                Analyze the uploaded sales data file carefully. The data may contain information such as product names, categories, quantities sold, selling prices, revenue, dates, customers, regions, sales representatives, discounts, or other business-related fields.

                Your objective is to transform raw sales data into clear and useful business insights.

                Perform the following analysis:

                1. DATASET OVERVIEW
                - Identify the number of records and columns, if available.
                - Identify the fields/columns present.
                - Explain briefly what each important column represents.
                - Identify missing, incomplete, or inconsistent values.

                2. SALES PERFORMANCE
                Calculate or analyze, where the required data is available:
                - Total sales/revenue
                - Total quantity sold
                - Average sales per transaction
                - Average selling price
                - Number of transactions
                - Highest-value transaction
                - Lowest-value transaction

                3. PRODUCT ANALYSIS
                 Identify:
                - Best-selling products by quantity
                - Highest-revenue products
                - Lowest-performing products
                - Products with unusually high or low sales
                - Product categories contributing the most revenue

                4. TIME-BASED ANALYSIS
                If dates are available, analyze:
                - Daily sales
                - Weekly sales
                - Monthly sales
                - Quarterly sales
                - Sales growth or decline over time
                - Peak sales periods
                - Low-sales periods

                5. CUSTOMER ANALYSIS
                If customer information is available:
                - Identify major customers by revenue
                - Identify customers with the highest purchase frequency
                - Identify customers contributing significantly to total sales
                - Identify unusual purchasing patterns

                6. REGIONAL ANALYSIS
                If location information is available:
                - Compare sales across regions
                - Identify highest-performing regions
                - Identify low-performing regions
                - Explain important regional differences

                7. SALES REPRESENTATIVE ANALYSIS
                If salesperson information is available:
                - Compare sales representatives based on revenue
                - Compare quantity sold
                - Identify significant differences in performance
                - Do not assume the reason for performance differences without evidence.

                8. DISCOUNT ANALYSIS
                If discount information is available:
                - Analyze the relationship between discounts and sales.
                - Identify products or categories receiving large discounts.
                - Identify whether high-discount transactions appear to generate higher sales.
                - Clearly distinguish correlation from causation.

                9. TREND ANALYSIS
                Identify:
                - Increasing trends
                - Decreasing trends
                - Seasonal patterns
                - Sudden changes
                - Unusual values or possible outliers

                10. BUSINESS INSIGHTS
                Provide practical insights based strictly on the data.

                11. RECOMMENDATIONS
                Suggest possible actions such as:
                - Inventory planning
                - Product promotion
                - Pricing review
                - Sales strategy
                - Customer targeting
                - Regional focus
                - Discount strategy

                Recommendations must be based on observed data and should not be presented as guaranteed outcomes.

                12. MANAGEMENT SUMMARY
                End with a concise summary of the most important findings.

                OUTPUT FORMAT:

                ## 📊 Sales Data Overview

                | Metric | Value |
                | ---|---:|
                |Number of Records | |
                | Number of Columns | |
                | Total Revenue | |
                | Total Quantity Sold | |
                | Average Transaction Value | |
                | Number of Transactions | |

                ## 🏆 Product Performance

                | Product/Category | Quantity Sold | Revenue | Observation |
                |---|---:|---:|---|

                ## 📅 Time-Based Performance

                | Period | Sales | Growth/Decline |
                |---|---:|---:|

                ## 👥 Customer Analysis
                ...

                ## 🌍 Regional Analysis
                ...

                ## 👨‍💼 Sales Representative Analysis
                ...

                ## 💰 Discount Analysis
                ...

                ## 📈 Important Trends
                - ... 
                - ...
                - ...

                ## 🔎 Key Business Insights
                1. ...
                2. ...
                3. ...
                4. ...
                5. ...

                ## 💡 Recommendations
                1. ... 
                2. ...
                3. ...
                4. ...
                5. ...

                ## 📋 Management Summary 
                ...

                IMPORTANT:
                - Use only information available in the uploaded dataset.
                - Do not invent missing values.
                - If a required column is unavailable, clearly state "Not available in the dataset."
                - Distinguish calculated facts from interpretations.
                - Do not claim that correlation proves causation.
                - Clearly identify any assumptions used in calculations.
                """

                response = model.generate_content(
                    [prompt, image]
                )

                st.subheader("Analysis Result")
                st.write(response.text)
