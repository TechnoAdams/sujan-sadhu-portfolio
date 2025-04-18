// Wait until the HTML document is fully loaded and parsed
document.addEventListener('DOMContentLoaded', function() {

    // --- Get references to the HTML elements we need to interact with ---

    // Start Screen Elements
    const startScreen = document.getElementById('startScreen');
    const startButton = document.getElementById('startButton'); // Needs ID in HTML

    // Chat Interface Elements
    const chatInterface = document.getElementById('chatInterface'); // Needs ID in HTML

    // Message Input Elements
    const messageInput = document.getElementById('messageInput');   // Needs ID in HTML
    const sendButton = document.getElementById('sendButton');       // Needs ID in HTML
    const messageList = document.getElementById('messageList');     // Needs ID in HTML

    // --- Check if all essential elements were found ---
    if (!startScreen || !startButton || !chatInterface || !messageInput || !sendButton || !messageList) {
        console.error("Error: One or more required elements not found in the HTML. Make sure IDs are set correctly.");
        // Display error to user if elements are missing
        alert("There was an error loading the chat interface elements. Please check the HTML structure and IDs.");
        return; // Stop script execution if elements are missing
    }

    // --- Event Listener for the "Start" Button ---
    startButton.addEventListener('click', function() {
        console.log("Start button clicked!"); // For debugging
        startScreen.style.display = 'none';       // Hide the start screen
        chatInterface.style.display = 'flex';      // Show the main chat interface (using flex as defined in CSS)
    });

    // --- Function to Add a Message to the Chat Window ---
    function addMessage(sender, text) {
        // Basic check to prevent adding empty messages
        if (!text.trim()) {
            return;
        }

        // Create the necessary HTML elements for a new message
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message'); // Add the base 'message' class

        const avatarDiv = document.createElement('div');
        avatarDiv.classList.add('message-avatar');
        // You could customize the avatar later based on sender, maybe different color/icon
        // For now, it uses the default style

        const contentDiv = document.createElement('div');
        contentDiv.classList.add('message-content');

        const senderSpan = document.createElement('span');
        senderSpan.classList.add('message-sender');
        senderSpan.textContent = sender; // Set the sender's name

        const textSpan = document.createElement('span');
        textSpan.classList.add('message-text');
        textSpan.textContent = text; // Set the message text

        // Assemble the message structure:
        contentDiv.appendChild(senderSpan);
        contentDiv.appendChild(textSpan);
        messageDiv.appendChild(avatarDiv);
        messageDiv.appendChild(contentDiv);

        // Add the complete message element to the message list container
        messageList.appendChild(messageDiv);

        // Scroll to the bottom of the message list to show the new message
        messageList.scrollTop = messageList.scrollHeight;
    }

    // --- Event Listener for the "Send" Button ---
    sendButton.addEventListener('click', function() {
        const messageText = messageInput.value;
        console.log("Send button clicked! Message:", messageText); // For debugging

        // Add the message to the chat window (simulate sending as "You")
        addMessage("You", messageText);

        // Clear the input field after sending
        messageInput.value = '';

        // Keep focus on the input field for easy typing of the next message
        messageInput.focus();
    });

    // --- Optional: Allow Sending by Pressing Enter Key in Input Field ---
    messageInput.addEventListener('keypress', function(event) {
        // Check if the key pressed was 'Enter'
        if (event.key === 'Enter') {
            // Prevent the default Enter behavior (like adding a new line in some cases)
            event.preventDefault();
            // Trigger a click on the send button
            sendButton.click();
        }
    });

    // --- Initial Setup ---
    // Make sure the chat interface is hidden initially (can also be done via CSS/inline style)
    // chatInterface.style.display = 'none'; // This is now handled by inline style in HTML for clarity

    console.log("Chat script loaded and initialized."); // For debugging
});