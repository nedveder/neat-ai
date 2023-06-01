import streamlit as st

st.title("Review My Code")

code_data = st.file_uploader("Upload Code")


def call_api():
    f = open("result.txt", "w")
    f.write("hellon")
    return f


def start():
    result_obj = call_api()
    for function in result_obj.functions:
        for change in function.changes:
            while not accept_yours and not accept_theirs:
                continue
            if accept_theirs:
                function.accepted








checkbox1 = st.checkbox("cb1")
checkbox2 = st.checkbox("cb2")
checkbox3 = st.checkbox("cb3")
checkbox4 = st.checkbox("cb4")


start_button = st.button("Start", on_click=start)

code = '''def hello():
    print("hello")'''


user_code = st.code(code, language='python', line_numbers=True)
accept_yours = st.button("accept yours")
accept_theirs = st.button("accept theirs")
suggested_code = st.code(code, language='python', line_numbers=True)
user_code.code("ithh")

