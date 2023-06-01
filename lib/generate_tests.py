import json
import gpt_api
import subprocess


TEST_PROMPTS_FILE = "prompts/test_prompts.json"
TEST_CODE_FILE = "tests.py"
MY_MODULE_FILE = "mymodule.py"


def test_code(source_code, language='python'):
    """Generate tests for the python function given in source-code,
    where the documentations of the functions it depends on are listed in
    'dependencies_documentations', and are assumed to be valid and working. """
    GPT = gpt_api.GPT()
    function_codes_generator = get_sources(source_code)
    with open(TEST_PROMPTS_FILE) as f:
        prompt = json.load(fp=f).get('test_case')[0].replace('{LANGUAGE}', language)
        GPT.add_system_message(prompt)
    with open(MY_MODULE_FILE, 'w') as f:
        f.write(source_code)
    for function_code in function_codes_generator:
        response = GPT.chat(function_code)
        code_response = response[response.find(r"```python") + 9:response.rfind(r"```")]
        with open(TEST_CODE_FILE, 'w') as f:
            f.write(code_response)

        p = subprocess.Popen(f"python3 {TEST_CODE_FILE}", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = p.communicate()
        error = err.decode('utf-8')
        if len(error) == 0:
            print(f"Function tested successfully!")
        else:
            print(f"There were some failed tests... AI creating tests review.")
            print(error)
            response = GPT.chat(error)
            print(response)
            exit()



if __name__ == '__main__':
    file = r"C:\Users\alonv\PycharmProjects\ex8_(1)\nonogram.py"
    with open(file, 'r') as f:
        code = f.read()
    test_code(code)
