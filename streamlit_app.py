import streamlit as st

st.set_page_config(page_title="Simple Streamlit App", layout="centered")

st.title("Hello Streamlit! 👋")

st.write("This is a really simple Streamlit application.")

st.button("Click Me!")

st.checkbox("Check this out")

st.slider("Select a value", 0, 100, 25)

st.text_input("Enter your name", "John Doe")

st.markdown(
    """
    <style>
    .stApp {
        background-color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True
)
