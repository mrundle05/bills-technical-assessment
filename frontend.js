fetch('/api/data')
    .then(response => response.json())
    .then(data => {
        console.log(data);
        // Use the data as needed in your frontend
    })
    .catch(error => console.error('Error:', error));