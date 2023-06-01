from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/compare', methods=['POST'])
def compare_files():
    file1 = request.files['file1']
    file2 = request.files['file2']

    # Save the uploaded files to the server
    file1.save('file1.txt')
    file2.save('file2.txt')

    # Execute the Python script using subprocess
    result = subprocess.run(['python', 'compare.py', 'file1.txt', 'file2.txt'], capture_output=True, text=True)

    # Retrieve the output from the Python script
    output = result.stdout

    # Return the output as the response
    return jsonify({'output': output})

if __name__ == '__main__':
    app.run()