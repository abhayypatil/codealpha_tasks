# Alpha ChatBot

A modern graphical user interface chatbot built with Python and Tkinter that responds to user inputs based on predefined rules and patterns.

## 🎯 Overview

This is a rule-based chatbot with a sleek dark-themed GUI that features chat bubbles, user avatars, persistent chat history, and real-time conversation capabilities. Built as part of CodeSoft Task 1 for demonstrating natural language processing concepts and conversation flow.

## ✨ Features

### 🖥️ Modern GUI Interface
- **Dark Theme**: Elegant dark color scheme for comfortable viewing
- **Chat Bubbles**: WhatsApp-style message bubbles for bot and user
- **Avatar Support**: Custom profile pictures for both user and bot
- **Auto-scrolling**: Automatically scrolls to show latest messages
- **Responsive Layout**: Clean and intuitive user interface

### 🧠 Smart Response System
- **Greeting Recognition**: Responds to various greetings (hi, hello, hey, namaste)
- **Time & Date**: Provides current time and date information
- **Identity Awareness**: Bot can introduce itself when asked
- **Gratitude Handling**: Responds appropriately to thank you messages
- **Weather Queries**: Placeholder responses for weather-related questions
- **Web Integration**: Opens YouTube when requested
- **Farewell Messages**: Proper goodbye handling

### 💾 Data Persistence
- **Chat History**: Automatically saves conversation history to [`chat_history.txt`](chat_history.txt)
- **History Loading**: Restores previous conversations on startup
- **Clear Chat**: Option to clear chat history with confirmation dialog

## 🚀 Getting Started

### Prerequisites

```bash
pip install nltk
pip install pillow
pip install tkinter  # Usually comes with Python
```

## 📝 Usage & Commands

Here is a list of commands you can use with Alpha chatbot:

| Command Category      | Example Command                               | Description                                                 |
| :-------------------- | :-------------------------------------------- | :---------------------------------------------------------- |
| **Open Website(s)** | `open google` or `open youtube and wikipedia` | Opens one or more websites in your default browser.         |
| **Google Search** | `google search history of python`             | Performs a search on Google.                                |
| **Youtube** | `Youtube funny cat videos`             | Searches for videos on YouTube.                             |
| **Play on YouTube** | `play never gonna give you up`                | Plays the first video result for the query on YouTube.      |
| **Open Application** | `open chrome` or `open notepad`               | Opens a local application installed on your computer.       |
| **Close Application** | `close chrome`                                | Closes the specified application if it's running.           |
| **System Control** | `system volume up` or `system mute`           | Controls your computer's master volume.                     |
| **Get Time/Date** | `what's the time?` or `today's date`          | Provides the current system time or date.                   |
| **Exit Assistant** | `bye`, `exit`, `quit`                         | Terminates the assistant.                                   |



## 🔧 Technical Specifications

- **GUI Framework**: Tkinter with Canvas and Scrollbar
- **NLP Library**: NLTK for tokenization
- **Image Processing**: PIL (Pillow) for avatar handling
- **Pattern Matching**: Regular expressions (re module)
- **Data Format**: Pipe-delimited text file storage


# 👨‍💻 Author

Developed by Vaibhav Singh ✨
