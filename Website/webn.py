import streamlit as st

st.title("Review My Code")

code_data = st.file_uploader("Upload Code")


def call_api():
    f = open("result.txt", "w")
    f.write("hellon")
    return f


def foo():
    call_api()
    result = open("result.txt", "r")
    st.write(result.read())


checkbox1 = st.checkbox("cb1")
checkbox2 = st.checkbox("cb2")
checkbox3 = st.checkbox("cb3")
checkbox4 = st.checkbox("cb4")


start_button = st.button("Start", on_click=foo)
