function typeWriterEffect(text, targetElement) {
    let i = 0;
    let isNewLineNeeded = false; // Flag to check if a new line is needed

    function typing() {
        if (i < text.length) {
            // Check if the current character starts a list item and handle new line
            if (text.charAt(i) === '-' && (i === 0 || text.charAt(i - 1) === '\n')) {
                if (!isNewLineNeeded && i !== 0) { // Add a line break before the list item if not at the start and no new line before
                    targetElement.innerHTML += '<br/>';
                }
                isNewLineNeeded = false; // Reset the flag as line break is handled
            }

            targetElement.innerHTML += text.charAt(i);

            // Set isNewLineNeeded to true after a list item
            if (text.charAt(i) === '\n' && text.charAt(i - 1) === '.') {
                isNewLineNeeded = true;
            }

            i++;
            setTimeout(typing, 10); // Speed of typing can be adjusted here
        } else if (isNewLineNeeded) { // After finishing the text, check if a new line is needed
            targetElement.innerHTML += '<br/>';
        }
    }
    typing();
}



function addMessage(sender, message, isBot) {
    const messageContainer = document.getElementById('message-container');
    const messageDiv = document.createElement('div');
    
    messageDiv.classList.add('message');
    if (isBot) {
        // Create a span for the bot name with a typewriter effect
        const nameSpan = document.createElement('span');
        nameSpan.innerHTML = `<strong class='chatBot'>${sender}:</strong> `;
        messageDiv.appendChild(nameSpan);
        
        // Apply the typewriter effect to the bot's message
        typeWriterEffect(message, messageDiv);
    } else {
        // For user messages, display them directly
        messageDiv.innerHTML = `<strong class='chatBot'>${sender}:</strong> ${message}`;
    }
    messageContainer.appendChild(messageDiv);
    messageContainer.scrollTop = messageContainer.scrollHeight;
}
document.getElementById('user-input-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const userInput = document.getElementById('search-input').value;
    addMessage('You', userInput, false); // Add user's message to the chat
    document.getElementById('search-input').value = ''; // Clear the input field

    // Send a POST request to the Flask server with the user input
    fetch('/getLLMResponse', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 'userInput': userInput })
    })
    .then(response => response.json()) // Handle JSON response
    .then(data => {
        // Display the response message
        setTimeout(() => {
            addMessage('MovieSearch', data.message, true); // Assume data.message contains the response
        }, 400);

        // Handle movie titles if they exist
        const movieContainer = document.getElementById('movies-container'); // Ensure this container exists in your HTML

        if (data.titles && data.titles.length > 0) {
        	movieContainer.innerHTML = ''; // Clear previous movies
            data.titles.forEach(movie => {
                addMovieBox(movie, movieContainer); // Function to display movie titles
            });
        }
    })
    .catch(error => {
        console.error('Error fetching data:', error);
        addMessage('MovieSearch', 'Failed to fetch data.', true); // Display error message
    });
});


document.getElementById('clearButton').addEventListener('click', function() {
    const messageContainer = document.getElementById('message-container');
    const messages = messageContainer.querySelectorAll('.message'); // Use the appropriate selector for your messages

    messages.forEach(function(msg) {
        msg.remove(); // This removes each message element from the document
    });


    // Clear the message container's content

    // Optionally send a POST request to the Flask server to clear the session or server-side data
    fetch('/clear', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        // If you need to send a body with the POST request, uncomment the next line
        // body: JSON.stringify({ clear: true })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message); // Log the server's response message
    })
    .catch(error => {
        console.error('Error:', error);
    });
});


// Function to display each movie in its own box
function addMovieBox(movie, container) {
    const box = document.createElement('div');
    box.className = 'book-box';

    const img = document.createElement('img');
    img.src = movie.image; // Path to a default image
    img.alt = movie.title;
	img.style.width = '150px';	

    const titleDiv = document.createElement('div');
    titleDiv.className = 'book-title';
    titleDiv.textContent = movie.title;

    const authorDiv = document.createElement('div');
    authorDiv.className = 'book-author';
    authorDiv.textContent = 'Directed By: Unknown'; // You can dynamically set this if your API provides it

    const button = document.createElement('button');
    button.className = 'buy-now-button';
    button.textContent = 'View';
    button.addEventListener('click', function() {
    fetch('/view', { // Your server endpoint to handle the POST request
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title: movie.title}) // Send only movie.title in the POST request body
    })
    .then(response => {
        if (response.redirected) {
            window.location.href = response.url; // Redirect to the response's URL if redirected
        } else {
            // Handle any other responses here, if necessary
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});


    // Append all elements to the box
    box.appendChild(img);
    box.appendChild(titleDiv);
    box.appendChild(authorDiv);
    box.appendChild(button);

    // Append the box to the container
    container.appendChild(box);
}

