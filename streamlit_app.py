import streamlit as st
import requests

def get_exchange_rates():
    """Fetches the latest exchange rates from the Frankfurter API."""
    try:
        response = requests.get("https://api.frankfurter.dev/latest")
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        return data.get("rates", {})
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching exchange rates: {e}. Please try again later.")
        return {}

def convert_currency(amount, from_currency, to_currency, rates):
    """Converts the amount from one currency to another."""
    if not rates:
        return None

    if from_currency == to_currency:
        return amount

    # Frankfurter API's base currency is EUR by default.
    # We need to convert to EUR first if from_currency is not EUR,
    # then from EUR to the target currency.
    if from_currency != "EUR" and from_currency in rates:
        amount_in_eur = amount / rates[from_currency]
    elif from_currency == "EUR":
        amount_in_eur = amount
    else:
        st.warning(f"Exchange rate for {from_currency} not available.")
        return None

    if to_currency != "EUR" and to_currency in rates:
        converted_amount = amount_in_eur * rates[to_currency]
    elif to_currency == "EUR":
        converted_amount = amount_in_eur
    else:
        st.warning(f"Exchange rate for {to_currency} not available.")
        return None

    return converted_amount

st.set_page_config(page_title="Currency Converter to INR", layout="centered")

st.title("Currency Converter to INR 💱🇮🇳")

st.write("Convert your money to Indian Rupees (INR) using the latest exchange rates.")

rates = get_exchange_rates()

if rates:
    currency_options = sorted(list(rates.keys()) + ["EUR"]) # Add EUR as it's the base for Frankfurter
    
    col1, col2 = st.columns(2)

    with col1:
        amount = st.number_input("Amount", min_value=0.01, value=1.00, step=0.01)
    
    with col2:
        from_currency = st.selectbox("From Currency", currency_options, index=currency_options.index("USD") if "USD" in currency_options else 0)

    st.write(f"Converting to: **INR**")

    if st.button("Convert"):
        if from_currency and amount:
            converted_value = convert_currency(amount, from_currency, "INR", rates)
            if converted_value is not None:
                st.success(f"{amount:,.2f} {from_currency} is equal to **{converted_value:,.2f} INR**")
        else:
            st.warning("Please enter an amount and select a currency.")
else:
    st.info("Unable to fetch exchange rates. Please check your internet connection or try again later.")

st.markdown(
    """
    <style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 8px;
        border: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.caption("Exchange rates provided by Frankfurter API (api.frankfurter.dev)")
