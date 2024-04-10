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
    addMessage('You', userInput, false); // Add user's message
    document.getElementById('search-input').value = ''; // Clear the input field
    
    // Simulate bot response after a delay
    setTimeout(() => {
        const botResponse = `The Imitation Game (2014) - This film depicts the life of Alan Turing, a British mathematician, logician, cryptanalyst, and computer scientist, who played a crucial role in cracking the Enigma code during World War II.
        \nThe Social Network (2010) - This movie tells the story of the founding of Facebook and the legal battles that followed, focusing on Mark Zuckerberg and the other co-founders.
        \nHackers (1995) - A cult classic, Hackers follows a group of high school hackers who uncover a conspiracy that threatens to exploit a major security flaw in a corporate mainframe.
     \nWarGames (1983) - This film revolves around a young computer whiz who hacks into a U.S. military supercomputer, starting a countdown to World War III.`;
        addMessage('MovieSearch', botResponse, true); // Add bot's response
    }, 800);
});