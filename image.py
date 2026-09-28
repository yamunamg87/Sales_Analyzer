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
You are an AI Sales Data Analysis Assistant.

Analyze the uploaded sales data image carefully and provide clear
and useful business insights.

Analyze the following whenever the information is available:

1. DATASET OVERVIEW
- Number of records
- Number of columns
- Important fields
- Missing or inconsistent values

2. SALES PERFORMANCE
- Total revenue
- Total quantity sold
- Average transaction value
- Average selling price
- Number of transactions
- Highest-value transaction
- Lowest-value transaction

3. PRODUCT ANALYSIS
- Best-selling products
- Highest-revenue products
- Lowest-performing products
- Top product categories

4. TIME-BASED ANALYSIS
If dates are available:
- Daily sales
- Weekly sales
- Monthly sales
- Sales growth or decline
- Peak sales periods
- Low-sales periods

5. CUSTOMER ANALYSIS
If customer information is available:
- Major customers
- Purchase frequency
- Important customers by revenue

6. REGIONAL ANALYSIS
If regional information is available:
- Highest-performing regions
- Lowest-performing regions
- Regional differences

7. SALES REPRESENTATIVE ANALYSIS
If salesperson information is available:
- Revenue by salesperson
- Quantity sold
- Performance differences

8. DISCOUNT ANALYSIS
If discount information is available:
- Discount patterns
- Products with large discounts
- Relationship between discounts and sales

9. TREND ANALYSIS
Identify:
- Increasing trends
- Decreasing trends
- Seasonal patterns
- Sudden changes
- Possible outliers

10. BUSINESS INSIGHTS
Give practical insights based strictly on the data.

11. RECOMMENDATIONS
Give practical recommendations for:
- Inventory
- Products
- Pricing
- Sales strategy
- Customers
- Regions
- Discounts

12. MANAGEMENT SUMMARY
Give a short final summary.

OUTPUT FORMAT:

## 📊 Sales Data Overview

| Metric | Value |
|---|---:|
| Number of Records | |
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

Provide findings if available.

## 🌍 Regional Analysis

Provide findings if available.

## 👨‍💼 Sales Representative Analysis

Provide findings if available.

## 💰 Discount Analysis

Provide findings if available.

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
- Use only information visible in the uploaded image.
- Do not invent values.
- If information is unavailable, say "Not available in the dataset."
- Clearly distinguish facts from interpretations.
- Do not claim correlation proves causation.
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
                               