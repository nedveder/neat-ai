import streamlit as st
import time
import pandas as pd


class FunctionImprovements:
    def __init__(self, old_code, new_code, comment):
        self.old_code = old_code
        self.new_code = new_code
        self.comment = comment

class TestResponse:
    def __init__(self, name, source_code, error=None, explanation=None):
        self.name = name
        self.source_code = source_code
        self.error = error
        self.explanation = explanation

if 'key' not in st.session_state:
    st.session_state["returned_data"] = None
    st.session_state["keys"] = None
    st.session_state["new_code_data"] = None
    st.session_state.key = 'UploadFile'



def call_api_improve():
    return {"1": FunctionImprovements("old", "new", "your code is bad"),
            "2": FunctionImprovements("old1", "new2", "your code is bad2")}


def call_api_test():
    return [TestResponse("testfffffffffffffff1", "cofffffffffffffffsssde1", "errosssssssssssssssssssssr1", "explansssssssssssssssss\nsssssssssssss\nssssss\nsssssssssssssssssssssssssssssssssssssssssation1"), TestResponse("test2", "code2", None, "explanation2")]



def run_improve():
    loading = st.empty()
    loading.write('Loading...')
    time.sleep(2)
    st.session_state["returned_data"] = call_api_improve()
    st.session_state["keys"] = list(st.session_state["returned_data"].keys())
    loading.empty()
    st.session_state.key = 'Improve'



def run_testing():
    loading = st.empty()
    loading.write('Loading...')
    time.sleep(2)
    st.session_state["returned_data"] = call_api_test()
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
            st.session_state.count = 0
        else:
            run_testing()

if st.session_state.key == 'runningApi':
    # Define the initial code string
    pass

if st.session_state.key == 'Improve':
    returned_data = st.session_state["returned_data"]
    keys = st.session_state["keys"]
    # Create empty placeholders for the 'accept yours' and 'accept theirs' buttons
    ch_accept_yours = st.empty()
    ch_accept_theirs = st.empty()

    # Create the 'accept yours' and 'accept theirs' buttons
    accept_yours = ch_accept_yours.button("Accept Yours")
    accept_theirs = ch_accept_theirs.button("Accept Theirs")
    if accept_yours:
        # ch_accept_yours.empty()
        # ch_accept_theirs.empty()
        st.session_state.count += 1
        # if st.session_state.count == len(keys):
        #     #todo remove everything and add download button to new code
        #     st.session_state.key = 'finished'
    if accept_theirs:
        st.session_state.count += 1
        # if st.session_state.count == len(keys):
        #     #todo remove everything and add download button to new code
        #     st.session_state.key = 'finished'
    print("i is equals to " + str(st.session_state.count))
    user_code = st.code(returned_data[keys[st.session_state.count]].old_code, language='python', line_numbers=True)
    # Display the user's code with syntax highlighting
    improved_code = st.code(returned_data[keys[st.session_state.count]].new_code, language='python', line_numbers=True)

    explanation = st.code(returned_data[keys[st.session_state.count]].comment, language='python', line_numbers=True)

if st.session_state.key == 'TestResults':

    to_add = []
    for i in st.session_state["returned_data"]:
        status = "✔️"
        if i.error == None:
            status = "❌"
        to_add.append({"Test name":i.name,"Test":i.source_code,"Error": i.error,"Description (Expendable)": i.explanation,"Status":status})
    df = pd.DataFrame(
        to_add
    )
    edited_df = st.experimental_data_editor(df)
