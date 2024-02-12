import {createTableFromJSON, addPagination} from './pages.js'
import {newThreadListener} from './listeners.js'

document.addEventListener('DOMContentLoaded', function () {

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

    // let currentPage = 1;
    // let rowsToShow = 10; // Default rows to show



    function displayResponse(response) {
        if (response.sql) {
            document.getElementById('sql-box').innerText = response.sql;
            document.getElementById('sql-container').style.display = 'block';
        }
        if (response.records) {

            let recs = JSON.parse(response.records)

            if (recs.length > 0) {
                var tableHTML = createTableFromJSON(recs);
                document.getElementById('records-box').innerHTML = tableHTML;
                addPagination();   
                document.getElementById('records-container').style.display = 'block';
            } else {
                alert('No records found')
            }

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

    // function createTableFromJSON(jsonData) {

    //     const data = JSON.parse(jsonData)

    //     if (data.length === 0) {
    //         return '<p>No records found.</p>';
    //     }

    //     let table = '<table class="table table-bordered"><thead><tr>';
    //     // Add headers
    //     Object.keys(data[0]).forEach(key => {
    //         table += `<th>${key}</th>`;
    //     });
    //     table += '</tr></thead><tbody>';

    //     // Add rows
    //     data.forEach(record => {
    //         table += '<tr>';
    //         Object.values(record).forEach(value => {
    //             table += `<td>${value}</td>`;
    //         });
    //         table += '</tr>';
    //     });

    //     table += '</tbody></table>';
    //     return table;
    // }


    document.getElementById('dataForm').addEventListener('submit', function (e) {
        console.log('Form submitted')
        e.preventDefault();

        var question = document.getElementById('question').value;
        showModal();
        clearResponses();

        fetch('submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question: question }),
        })
            .then(response => response.json())
            .then(data => {
                console.log("response:")
                console.log(data);
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


    document.getElementById('submit-button').addEventListener('click', function(e){
        e.preventDefault();
        let form = document.getElementById('dataForm');
        form.dispatchEvent(new Event('submit'));
    })

    document.getElementById('question').addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
            document.getElementById('submit-button').click();
        }
    });



    document.getElementById('chat-history-button').addEventListener('click', function (e) {
        console.log('chat history modal')
        e.preventDefault();
    
        const chatHistoryModal = document.getElementById('chat-history-modal');
        const chatHistoryLoadingGif = document.getElementById('chat-history-loading-gif');
        const chatHistoryContent = document.getElementById('chat-history-content');
    
        chatHistoryModal.style.display = 'block';
        chatHistoryLoadingGif.style.display = 'block';
    
        fetch('chathist', {
            method: 'GET'
        })
        .then(response => response.json())
        .then(data => {
            const chathist = data.chathist;

            console.log("chat history:", chathist);

            chatHistoryLoadingGif.style.display = 'none';
            chatHistoryContent.innerHTML = ''; // Clear previous content
            chatHistoryContent.style.display = 'flex';
            chatHistoryContent.style.flexDirection = 'column';

            const chatHistoryHeader = document.createElement('div');
            chatHistoryHeader.classList.add('chat-history-entry');
            chatHistoryHeader.innerHTML = `
                <div class="chat-history-cell chat-history-cell-header chat-timestamp">Timestamp</div>
                <div class="chat-history-cell chat-history-cell-header chat-prompt">Question/Prompt</div>
            `
            chatHistoryContent.appendChild(chatHistoryHeader);
    
            chathist.forEach(d => {
                const chatEntry = document.createElement('div');
                chatEntry.classList.add('chat-history-entry');
                chatEntry.innerHTML = `
                    <div class="chat-history-cell chat-timestamp">${new Date(d.timestamp * 1000).toLocaleString()}</div>
                    <div class="chat-history-cell chat-prompt">${d.prompt}</div>
                `;
                chatHistoryContent.appendChild(chatEntry);
            });
            
        })
        .catch((error) => {
            chatHistoryModal.style.display = 'none';
            console.error('Error:', error);
            document.getElementById('error-box').innerText = 'An error occurred.';
            document.getElementById('error-box').style.display = 'block';
        });
    });
    
    
    // close modal listeners
    document.getElementById('chat-history-modal').addEventListener('click', function(event) {
        if (event.target == this) {
            this.style.display = 'none';
        }
    });
    document.getElementById('close-modal').addEventListener('click', function() {
        document.getElementById('chat-history-modal').style.display = 'none';
    });
    
    

    document.getElementById('api-key-form')?.addEventListener('submit', function(e){
        e.preventDefault();
        fetch('update-api-key', {
            method: 'POST',
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify( { api_key: document.getElementById('api-key').value } )
        })
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                // the server should return a 500 status code so i'm not sure if it would ever reach this point
                console.error(data.devmessage)
            }
            alert(data.message)
        })
        .catch((error) => {
            console.error(error);
        });
    })
    
    document.getElementById('model-select').addEventListener('change', function(e){
        e.preventDefault();
        fetch('update-model', {
            method: 'POST',
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify( { model: document.getElementById('model-select').value } )
        })
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                // the server should return a 500 status code so i'm not sure if it would ever reach this point
                console.error(data.devmessage)
            }
            alert(data.message)
        })
        .catch((error) => {
            console.error(error);
        });
    })
    
    document.getElementById('new-thread-button').addEventListener('click', newThreadListener)

});
