export function newThreadListener(e) {
    e.preventDefault();
    fetch('newthread', {
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify( { actionItem: "Make me a new thread!" } )
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
}