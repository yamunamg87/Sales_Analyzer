import streamlit as st
import requests
import base64
import os
from PIL import Image

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Sales Data Analyser",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Sales Data Analyser")
st.write("Upload a sales data image and get AI-powered insights.")

# -----------------------------
# Gemini API Configuration
# -----------------------------
GOOGLE_API_KEY = os.environ.get("GEMINI_KEY")

if not GOOGLE_API_KEY:
    st.error("GEMINI_KEY is not available.")
    st.stop()

API_URL = (
    "https://generativelanguage.googleapis.com/v1beta/" 
    "models/gemini-3.5-flash-lite:generateContent" 
) 
 
# ----------------------------- 
# Image Upload 
# ----------------------------- 
uploaded_file = st.file_uploader( 
    "Upload an Image", 
    type=["jpg", "jpeg", "png"] 
) 
 
if uploaded_file is not None: 
 
    image = Image.open(uploaded_file) 
 
    col1, col2 = st.columns(2) 
 
    with col1: 
        st.image( 
            image, 
            caption="Uploaded Image", 
            use_container_width=True 
        ) 
 
    with col2: 
 
        if st.button("Analyze Image"): 
 
            with st.spinner("Analyzing sales data..."): 
 
                # ----------------------------- 
                # Read Image 
                # ----------------------------- 
                uploaded_file.seek(0) 
                image_bytes = uploaded_file.read() 
 
                image_base64 = base64.b64encode( 
                    image_bytes 
                ).decode("utf-8") 
 
                mime_type = uploaded_file.type or "image/jpeg" 
 
                # ----------------------------- 
                # Prompt 
                # ----------------------------- 
                prompt = """
You are an expert Sales Data Analyst.

IMPORTANT:
The uploaded image contains a sales table.
You MUST READ THE VALUES FROM THE TABLE AND CALCULATE THE RESULTS.

DO NOT say:
"Not available because it requires summation"
when the required values are visible in the image.

You are required to perform arithmetic calculations yourself.

The table may contain columns such as:
- Order No
- Order Date
- Customer Name
- Ship Date
- Retail Price (USD)
- Order Quantity
- Tax (USD)
- Total (USD)

==================================================
1. DATASET OVERVIEW
==================================================

Identify:

- Total number of records/rows
- Total number of columns
- Names of all columns
- Date range
- Missing values if visible

==================================================
2. SALES PERFORMANCE
==================================================

READ THE NUMBERS FROM THE IMAGE AND CALCULATE:

- Total Revenue = SUM of all values in the Total (USD) column
- Total Quantity Sold = SUM of all values in Order Quantity
- Average Transaction Value = Total Revenue / Number of Transactions
- Average Order Quantity
- Average Retail Price
- Highest Transaction Value
- Lowest Transaction Value
- Number of Transactions

IMPORTANT:
If a value can be calculated from visible numbers in the image,
CALCULATE IT.

Do NOT write:
"Not available in the dataset (requires summation)."

==================================================
3. PRODUCT ANALYSIS
==================================================

If product/category information exists:

- Best-selling product
- Highest-revenue product
- Lowest-performing product
- Quantity sold by product
- Revenue by product
- Top product/category

If product information does NOT exist in the image, write:

"Product information is not available in the uploaded dataset."

==================================================
4. DATE ANALYSIS
==================================================

If Order Date is available:

- Earliest order date
- Latest order date
- Sales by date
- Highest-sales date
- Lowest-sales date
- Sales trend
- Growth or decline if enough data is available

==================================================
5. CUSTOMER ANALYSIS
==================================================

Use Customer Name if available.

Calculate:

- Number of unique customers
- Customer with highest revenue
- Customer with highest number of orders
- Revenue by major customers
- Purchase frequency

==================================================
6. TAX ANALYSIS
==================================================

If Tax (USD) exists:

Calculate:

- Total tax
- Average tax per transaction
- Highest tax
- Lowest tax

==================================================
7. ORDER QUANTITY ANALYSIS
==================================================

Calculate:

- Total quantity sold
- Average quantity per order
- Highest quantity in one order
- Lowest quantity in one order

==================================================
8. PRICE ANALYSIS
==================================================

Using Retail Price (USD):

Calculate:

- Average retail price
- Highest retail price
- Lowest retail price

==================================================
9. BUSINESS INSIGHTS
==================================================

Give 5 useful business insights based ONLY on the
numbers visible in the image.

==================================================
10. RECOMMENDATIONS
==================================================

Give 5 practical recommendations based on the calculated results.

==================================================
OUTPUT FORMAT
==================================================

## 📊 Sales Data Overview

| Metric | Value |
|---|---:|
| Number of Records | calculated value |
| Number of Columns | calculated value |
| Date Range | calculated value |
| Total Revenue | calculated value |
| Total Quantity Sold | calculated value |
| Average Transaction Value | calculated value |
| Average Order Quantity | calculated value |
| Average Retail Price | calculated value |
| Highest Transaction Value | calculated value |
| Lowest Transaction Value | calculated value |
| Total Tax | calculated value |
| Number of Transactions | calculated value |

## 🏆 Top Sales Performance

| Metric | Result |
|---|---|
| Highest Value Order | |
| Lowest Value Order | |
| Highest Quantity Order | |
| Highest Revenue Customer | |

## 👥 Customer Analysis

| Customer | Orders | Revenue |
|---|---:|---:|

## 📅 Date Analysis

| Metric | Result |
|---|---|
| Earliest Order | |
| Latest Order | |
| Highest Sales Date | |
| Lowest Sales Date | |

## 💰 Tax Analysis

| Metric | Value |
|---|---:|
| Total Tax | |
| Average Tax | |
| Highest Tax | |
| Lowest Tax | |

## 📦 Quantity Analysis

| Metric | Value |
|---|---:|
| Total Quantity | |
| Average Quantity per Order | |
| Highest Quantity | |
| Lowest Quantity | |

## 📈 Key Business Insights

1. 
2. 
3. 
4. 
5. 

## 💡 Recommendations

1.
2.
3.
4.
5.

## 📋 Management Summary

Write a short summary of the overall sales performance.

==================================================
VERY IMPORTANT
==================================================

1. READ the numbers from the uploaded image.
2. PERFORM calculations using those numbers.
3. Do NOT refuse to calculate.
4. Do NOT say "requires summation" if the numbers are visible.
5. Do NOT invent numbers.
6. If the image genuinely does not contain the required information,
   say "Not available in the uploaded image."
7. Clearly identify any value that could not be calculated because
   the image quality prevented reading the numbers.
8. Use USD for monetary values.
"""
 
                # ----------------------------- 
                # API Payload 
                # ----------------------------- 
                payload = { 
                    "contents": [ 
                        { 
                            "parts": [ 
                                { 
                                    "text": prompt 
                                }, 
                                { 
                                    "inline_data": { 
                                        "mime_type": mime_type, 
                                        "data": image_base64 
                                    } 
                                } 
                            ] 
                        } 
                    ] 
                } 
 
                # ----------------------------- 
                # API Headers 
                # ----------------------------- 
                headers = { 
                    "Content-Type": "application/json", 
                    "x-goog-api-key": GOOGLE_API_KEY 
                } 
 
                # ----------------------------- 
                # API Request 
                # ----------------------------- 
                try: 
 
                    response = requests.post( 
                        API_URL, 
                        headers=headers, 
                        json=payload, 
                        timeout=120 
                    ) 
 
                    if response.status_code != 200: 
                        st.error( 
                            f"Gemini API Error: {response.status_code}" 
                        ) 
                        st.code(response.text) 
                        st.stop() 
 
                    # ----------------------------- 
                    # Parse Response 
                    # ----------------------------- 
                    result = response.json() 
 
                    candidates = result.get("candidates", []) 
 
                    if not candidates: 
                        st.error("Gemini returned no result.") 
                        st.json(result) 
                        st.stop() 
 
                    parts = candidates[0].get( 
                        "content", {} 
                    ).get("parts", []) 
 
                    analysis = "" 
 
                    for part in parts: 
                        if "text" in part: 
                            analysis += part["text"] 
 
                    if not analysis: 
                        st.error("No analysis was returned.") 
                        st.json(result) 
                        st.stop() 
 
                    # ----------------------------- 
                    # Display Result 
                    # ----------------------------- 
                    st.subheader("📊 Analysis Result") 
                    st.markdown(analysis) 
 
                except requests.exceptions.Timeout: 
                    st.error( 
                        "The request timed out. Please try again." 
                    ) 
 
                except requests.exceptions.RequestException as e: 
                    st.error( 
                        f"Connection error: {e}" 
                    ) 
 
                except Exception as e: 
                    st.error( 
                        f"Unexpected error: {e}" 
                    )