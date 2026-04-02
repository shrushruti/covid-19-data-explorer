import streamlit as st
import pandas as pd

st.set_page_config(page_title="COVID-19 Data Explorer", layout="wide")

st.title("COVID-19 Data Explorer")

url = "https://raw.githubusercontent.com/datasets/covid-19/main/data/countries-aggregated.csv"
df = pd.read_csv(url)

df["Date"] = pd.to_datetime(df["Date"])
df["YearMonth"] = df["Date"].dt.to_period("M").astype(str)

st.header("Single Country Analysis")

country = st.selectbox("Choose Country", sorted(df["Country"].unique()), index=77 if "India" in sorted(df["Country"].unique()) else 0)

df_country = df[df["Country"] == country].copy()

st.subheader("COVID Data Preview (After Cases Started)")
df_non_zero = df_country[df_country["Confirmed"] > 0]
st.write(df_non_zero.head())

st.subheader("Confirmed Cases Over Time")
st.line_chart(df_country.set_index("Date")["Confirmed"])

st.subheader("Deaths Over Time")
st.line_chart(df_country.set_index("Date")["Deaths"])

st.subheader("Recovered Over Time")
st.line_chart(df_country.set_index("Date")["Recovered"])

st.info("Note: Recovered values may drop or become zero in some countries because of dataset limitations.")

st.header("Multi-Country Comparison")

countries = st.multiselect(
    "Choose one or more countries",
    sorted(df["Country"].unique()),
    default=["India", "US"] if "India" in df["Country"].values and "US" in df["Country"].values else None
)

metric = st.selectbox("Choose Metric", ["Confirmed", "Deaths", "Recovered"])

view_type = st.radio("Choose View Type", ["Daily", "Monthly"], horizontal=True)

if countries:
    df_compare = df[df["Country"].isin(countries)].copy()

    st.subheader("Comparison Data Preview (After Cases Started)")
    df_compare_non_zero = df_compare[df_compare["Confirmed"] > 0]
    st.write(df_compare_non_zero.head())

    if view_type == "Daily":
        st.subheader(f"{metric} Daily Comparison Over Time")
        pivot_df = df_compare.pivot(index="Date", columns="Country", values=metric)
        st.line_chart(pivot_df)

        st.subheader("Comparison Table")
        st.write(pivot_df.head())

    else:
        st.subheader(f"{metric} Monthly Comparison Over Time")
        pivot_df = df_compare.groupby(["YearMonth", "Country"])[metric].max().unstack()
        st.line_chart(pivot_df)

        st.subheader("Monthly Comparison Table")
        st.write(pivot_df.head())

else:
    st.warning("Please select at least one country.")