function handleFile1(event) {
    const file1 = event.target.files[0];
    const reader = new FileReader();

    reader.onload = function (e) {
        document.getElementById("content1").textContent = e.target.result;
    };

    reader.readAsText(file1);
}

function handleFile2(event) {
    const file2 = event.target.files[0];
    const reader = new FileReader();

    reader.onload = function (e) {
        document.getElementById("content2").textContent = e.target.result;
    };

    reader.readAsText(file2);
}

function compareFiles() {
    console.log("Got to compare files");
    const file1 = document.getElementById("file1").files[0];
    const file2 = document.getElementById("file2").files[0];

    const formData = new FormData();
    formData.append("file1", file1);
    formData.append("file2", file2);

    fetch('http://localhost:3000/run-python')
        .then(response => response.text())
        .then(output => {
            console.log(output); // Log the output of the Python script
        })
        .catch(error => {
            console.error('Error:', error);
        });

}
