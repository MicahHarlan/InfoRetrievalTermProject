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
        // Simulate bot response after a delay
        setTimeout(() => {
            addMessage('MovieSearch', data.message, true); // Assume data.message contains the response
        }, 800);
    })
    .catch(error => {
        console.error('Error fetching data:', error);
        addMessage('MovieSearch', 'Failed to fetch data.', true); // Display error message
    });
});

