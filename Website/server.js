const express = require('express');
const app = express();
const { exec } = require('child_process');

// Set up a route to handle the request
app.get('/run-python', (req, res) => {
    // Execute the Python code using child_process.exec
    exec('python compare.py', (error, stdout, stderr) => {
        if (error) {
            console.error(`Error executing Python script: ${error}`);
            return res.status(500).send('Internal Server Error');
        }
        // Send the output of the Python script as the response
        res.send(stdout);
    });
});

// Start the server
app.listen(3000, () => {
    console.log('Server started on port 3000');
});
