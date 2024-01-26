document.addEventListener('DOMContentLoaded', function() {

    function showModal() {
        document.getElementById('loadingModal').style.display = 'block';
    }

    function hideModal() {
        document.getElementById('loadingModal').style.display = 'none';
    }

    function clearResponses() {
        Array.from(document.getElementsByClassName('response-box-container')).forEach(b => {
            b.style.display = 'none';
        })
        // document.getElementById('sql-box').innerText = '';
        // document.getElementById('records-box').innerText = '';
        // document.getElementById('message-box').innerText = '';
        // document.getElementById('error-box').innerText = '';
    }

    function displayResponse(response) {
        if (response.sql) {
            document.getElementById('sql-box').innerText = response.sql;
            document.getElementById('sql-container').style.display = 'block';
        }
        if (response.records) {
            var tableHTML = createTableFromJSON(response.records);
            document.getElementById('records-box').innerHTML = tableHTML;
            document.getElementById('records-container').style.display = 'block';
        }
        if (response.message) {
            document.getElementById('message-box').innerText = response.message;
            document.getElementById('message-container').style.display = 'block';
        }
        if (response.error) {
            document.getElementById('error-box').innerText = response.error;
            document.getElementById('error-container').style.display = 'block';
        }
    }

    function createTableFromJSON(jsonData) {

        const data = JSON.parse(jsonData)

        if (data.length === 0) {
            return '<p>No records found.</p>';
        }

        let table = '<table class="table table-bordered"><thead><tr>';
        // Add headers
        Object.keys(data[0]).forEach(key => {
            table += `<th>${key}</th>`;
        });
        table += '</tr></thead><tbody>';

        // Add rows
        data.forEach(record => {
            table += '<tr>';
            Object.values(record).forEach(value => {
                table += `<td>${value}</td>`;
            });
            table += '</tr>';
        });

        table += '</tbody></table>';
        return table;
    }


    document.getElementById('dataForm').addEventListener('submit', function(e) {
        e.preventDefault();

        var question = document.getElementById('question').value;
        showModal();
        clearResponses();

        fetch('/ai-search-tool/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question: question }),
        })
        .then(response => response.json())
        .then(data => {
            hideModal();
            displayResponse(data);
        })
        .catch((error) => {
            hideModal();
            console.error('Error:', error);
            document.getElementById('error-box').innerText = 'An error occurred.';
            document.getElementById('error-box').style.display = 'block';
        });
    });

    document.getElementById('question').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            document.getElementById('submit').click();
        }
    });
});
