import streamlit as st

st.title("Review My Code")

ch_file = st.empty()
code_data = ch_file.file_uploader("Upload Code")


def call_api():
    f = open("result.txt", "w")
    f.write("hellon")
    return f

result = []
counter = 0

def start():
    result = call_api()
    counter = 0

def foo():
    print("Hi")


ch1 = st.empty()
ch2 = st.empty()
ch3 = st.empty()
ch4 = st.empty()
checkbox1 = ch1.checkbox("cb1")
checkbox2 = ch2.checkbox("cb2")
checkbox3 = ch3.checkbox("cb3")
checkbox4 = ch4.checkbox("cb4")

placeholder = st.empty()
start_button = placeholder.button("Start", on_click=start)
if start_button:
    placeholder.empty()
    ch1.empty()
    ch2.empty()
    ch3.empty()
    ch4.empty()
    ch_file.empty()

code = '''def hello():
    print("hello")'''


user_code = st.code(code, language='python', line_numbers=True)
accept_yours = st.button("accept yours")
accept_theirs = st.button("accept theirs")
suggested_code = st.code(code, language='python', line_numbers=True)
user_code.code("ithh")

