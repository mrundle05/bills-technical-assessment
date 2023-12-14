fetch('https://mrundle05.github.io/bills-technical-assessment/api/data')
    .then(response => response.json())
    .then(data => {
        console.log(data);
        document.getElementById('data-display').innerHTML = `<p>${data.message}</p>`;
    })
    .catch(error => console.error('Error:', error));