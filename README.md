# Autosending-messages-via-wpp-web-with-python-code-automations

# WhatsApp Message Automation

This GitHub repository contains a Python script for automating the process of sending WhatsApp messages to a list of contacts stored in a Google Sheets spreadsheet. This automation is particularly useful for sending messages to students' parents or guardians for communication purposes.

## Prerequisites

Before running this script, you'll need the following:

1. **Python**: Make sure you have Python installed on your system.

2. **Chrome WebDriver**: You need to have the Chrome WebDriver installed and its executable path configured. This WebDriver allows the script to interact with the WhatsApp web interface. You can download it from the official website: https://sites.google.com/chromium.org/driver/

3. **Google Sheets API Key**: You should have a Google Sheets API key in the form of a JSON file (key.json). This key is necessary for accessing the Google Sheets spreadsheet containing your contact information.

## How the Script Works

The script performs the following steps:

1. **Google Sheets Connection**: It connects to Google Sheets using the Google Sheets API and loads the contact information, including the student's name, responsible person, phone number, message status, and a custom message.

2. **Message Customization**: For each student, it customizes the message by inserting their name and responsible person's name into a predefined message template. It also checks if the message has already been sent (based on the "Enviada" column in the spreadsheet) and prepares the data accordingly.

3. **WhatsApp Web Link Generation**: It generates a custom WhatsApp Web link for each message, which includes the recipient's phone number and the encoded message text. This link allows the script to open a WhatsApp chat window with the contact and automatically populate the message.

4. **Sending Messages**: It uses Selenium to automate the process of opening WhatsApp Web, pasting the custom link, and sending the message. It also waits for the message to be sent successfully, indicated by the absence of a clock icon.

5. **Updating Google Sheets**: After sending a message, the script updates the "Enviada" column in the Google Sheets spreadsheet to mark that the message has been sent.

## Usage

To use this script, follow these steps:

1. Set up the prerequisites mentioned above.

2. Clone this repository to your local machine.

3. Place your `key.json` (Google Sheets API key) in the same directory as the script.

4. Update the predefined message template in the `message` class if needed.

5. Run the script. It will read the contact information from the Google Sheets spreadsheet and start sending messages to contacts who haven't received a message yet.

Please ensure that you use this script responsibly and in compliance with WhatsApp's terms of service and any applicable laws regarding messaging and automation.
