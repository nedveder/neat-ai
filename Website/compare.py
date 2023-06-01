from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/compare', methods=['POST'])
def compare_files():
    print("HI")
    file1 = request.files['file1']
    file2 = request.files['file2']

    # Process the files, perform comparison logic, and generate a result file

    # Example: Concatenate the contents of file1 and file2
    content1 = file1.read().decode('utf-8')
    content2 = file2.read().decode('utf-8')
    result_content = content1 + content2

    # Save the result to a file
    result_file = 'result.txt'
    with open(result_file, 'w') as f:
        f.write(result_content)

    # Return the result file to the client
    return jsonify({'result_file': result_file})

if __name__ == '__main__':
    app.run()
