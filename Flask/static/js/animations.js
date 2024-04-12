function typeWriterEffect(text, targetElement) {
    let i = 0;
    function typing() {
        if (i < text.length) {
            targetElement.innerHTML += text.charAt(i);
            i++;
            setTimeout(typing, 20); // Speed of typing
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
        movieContainer.innerHTML = ''; // Clear previous movies
        if (data.titles && data.titles.length > 0) {
            data.titles.forEach(title => {
                addMovieBox(title, movieContainer); // Function to display movie titles
            });
        }
    })
    .catch(error => {
        console.error('Error fetching data:', error);
        addMessage('MovieSearch', 'Failed to fetch data.', true); // Display error message
    });
});

// Function to display each movie in its own box
function addMovieBox(title, container) {
    const box = document.createElement('div');
    box.className = 'book-box';

    const img = document.createElement('img');
    img.src = '/images/site/default-movie.png'; // Path to a default image
    img.alt = title;

    const titleDiv = document.createElement('div');
    titleDiv.className = 'book-title';
    titleDiv.textContent = title;

    const authorDiv = document.createElement('div');
    authorDiv.className = 'book-author';
    authorDiv.textContent = 'Directed By: Unknown'; // You can dynamically set this if your API provides it

    const button = document.createElement('button');
    button.className = 'buy-now-button';
    button.textContent = 'View';

    // Append all elements to the box
    box.appendChild(img);
    box.appendChild(titleDiv);
    box.appendChild(authorDiv);
    box.appendChild(button);

    // Append the box to the container
    container.appendChild(box);
}

