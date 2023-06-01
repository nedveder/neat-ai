import streamlit as st
import time


global code_data

if 'key' not in st.session_state:
    st.session_state.key = 'UploadFile'


def call_api_improve():
    pass


def call_api_test():
    pass


def run_improve():
    loading = st.empty()
    loading.write('Loading...')
    time.sleep(2)
    call_api_improve()
    loading.empty()
    st.session_state.key = 'Improve'


def run_testing():
    loading = st.empty()
    loading.write('Loading...')
    time.sleep(2)
    call_api_test()
    loading.empty()
    st.session_state.key = 'TestResults'


st.title("Review :blue[Your] Code")

if st.session_state.key == 'UploadFile':
    ch_text = st.empty()
    ch_text.write("First We need to see your code")
    ch_upload = st.empty()
    code_data = ch_upload.file_uploader("Upload Code")
    if code_data:
        st.session_state.key = 'ChooseOperation'
        ch_text.empty()
        ch_upload.empty()


if st.session_state.key == 'ChooseOperation':

    # Create an empty placeholder for the start button
    ch_improve_button = st.empty()
    ch_test_button = st.empty()

    # Create the start button and assign the 'start' function to its 'on_click' parameter
    improve_button = ch_improve_button.button("Improve My Code")
    test_button = ch_test_button.button("Test My Code")

    # If the start button is clicked, clear the placeholders
    if improve_button or test_button:
        ch_improve_button.empty()
        ch_test_button.empty()
        st.session_state.key = 'loading'
        if improve_button:
            run_improve()
        else:
            run_testing()



if st.session_state.key == 'runningApi':
    # Define the initial code string
    pass


if st.session_state.key == 'Improve':
    code = '''def hello():
            print("hello")'''
    # Display the user's code with syntax highlighting
    user_code = st.code(code, language='python', line_numbers=True)

    # Create empty placeholders for the 'accept yours' and 'accept theirs' buttons
    ch_accept_yours = st.empty()
    ch_accept_theirs = st.empty()

    # Create the 'accept yours' and 'accept theirs' buttons
    accept_yours = ch_accept_yours.button("Accept Yours")
    accept_theirs = ch_accept_theirs.button("Accept Theirs")

    # Display the suggested code with syntax highlighting
    suggested_code = st.code(code, language='python', line_numbers=True)

if st.session_state.key == 'TestResults':
    pass







