

**Flask UI Documentation**
=======================

**Overview**
------------

This Flask UI folder contains the front-end code for our application. It includes the HTML, CSS, and JavaScript files that make up the user interface.

**Files**
--------

### `index.html`

* **Description:** The main HTML file for the application.

* **Explanation:** This HTML file sets up the basic structure of the chat application, including the chat container, header, body, and form.

### `chat.js`

* **Description:** The JavaScript file that handles the chat functionality.

* **Explanation:** This JavaScript file sets up an event listener for the chat form submission. When the form is submitted, it sends a POST request to the server with the message, and then adds the message to the chat log.

### `styles.css`

* **Description:** The CSS file that styles the chat application.

* **Explanation:** This CSS file styles the chat application, including the container, chat header, chat body, and form.

**Notes**
-------

* This Flask UI folder is designed to be used with the API folder, which provides the back-end functionality for the chat application.
* The chat application uses a simple text-based interface, where users can type messages and send them to the server.
* The server responds with the message and adds it to the chat log.
* The chat log is displayed in real-time, with new messages appearing at the bottom of the log.