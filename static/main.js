document.addEventListener('DOMContentLoaded', function() {

    function showModal() {
        document.getElementById('loadingModal').style.display = 'block';
    }

    function hideModal() {
        document.getElementById('loadingModal').style.display = 'none';
    }

    document.getElementById('submit').addEventListener('click', function() {
        var question = document.getElementById('question').value;
        showModal();

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
            document.getElementById('response').innerText = data.message;
        })
        .catch((error) => {
            hideModal();
            console.error('Error:', error);
            document.getElementById('response').innerText = 'An error occurred.';
        });
    });

    document.getElementById('question').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            document.getElementById('submit').click();
        }
    });
});
