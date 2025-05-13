
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Streamlit app title
st.title("🚀 Startup Investment Analysis Dashboard")
st.markdown("Upload a startup funding dataset (CSV) to begin analysis.")

# Upload data
uploaded_file = st.file_uploader("Upload CSV file", type="csv")

if uploaded_file is not None:
    # Read uploaded file directly
    df = pd.read_csv(uploaded_file)

    # Basic Data Overview
    st.subheader("📊 Raw Data")
    st.dataframe(df.head())

    # Preprocessing
    df.columns = df.columns.str.lower()
    df.rename(columns={
        'startup': 'startup_name',
        'city': 'city',
        'industry': 'sector',
        'investment_amount': 'amount',
        'date': 'date'
    }, inplace=True)

    df = df.dropna(subset=['amount'])

    # Convert date
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df = df.dropna(subset=['date'])

    # Convert amount to numeric
    df['amount'] = df['amount'].replace('[\$,]', '', regex=True).astype(float)

    # Summary Metrics
    st.subheader("📈 Summary Metrics")
    total_invested = df['amount'].sum()
    average_investment = df['amount'].mean()
    top_startup = df.groupby('startup_name')['amount'].sum().idxmax()

    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Total Investment", f"${total_invested:,.0f}")
    col2.metric("📈 Average Investment", f"${average_investment:,.0f}")
    col3.metric("🏆 Top Funded Startup", top_startup)

    # Top Funded Startups
    st.subheader("🏢 Top Funded Startups")
    top_startups = df.groupby('startup_name')['amount'].sum().sort_values(ascending=False).head(10)
    st.bar_chart(top_startups)

    # Top Sectors
    if 'sector' in df.columns:
        st.subheader("📌 Top Funded Sectors")
        top_sectors = df.groupby('sector')['amount'].sum().sort_values(ascending=False).head(10)
        fig, ax = plt.subplots()
        sns.barplot(x=top_sectors.values, y=top_sectors.index, ax=ax)
        st.pyplot(fig)

    # Investment Timeline
    st.subheader("📅 Investment Timeline")
    monthly_funding = df.resample('M', on='date')['amount'].sum()
    st.line_chart(monthly_funding)

    # Top Investment Cities
    if 'city' in df.columns:
        st.subheader("📍 Top Investment Cities")
        top_cities = df.groupby('city')['amount'].sum().sort_values(ascending=False).head(10)
        st.bar_chart(top_cities)

    # Filter
    with st.expander("🔍 Filter Data"):
        min_amount = st.slider("Minimum Funding Amount", 0, int(df['amount'].max()), 1000000)
        filtered_df = df[df['amount'] >= min_amount]
        st.write(f"Showing {filtered_df.shape[0]} records with amount ≥ ${min_amount}")
        st.dataframe(filtered_df.head())

else:
    st.warning("📂 Please upload a CSV file to start analysis.")
